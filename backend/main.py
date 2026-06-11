# -*- coding: utf-8 -*-
from fastapi import FastAPI, HTTPException, BackgroundTasks, Response, Cookie
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import re
from . import db, scanner

db.init_db()

import threading
import time
from datetime import datetime

def periodic_sync_thread():
    # Sleep 30 seconds after startup to allow systems to initialize
    time.sleep(30)
    while True:
        print("Automatic periodic background sync starting...")
        try:
            scanner.run_sync_all()
            print("Automatic periodic background sync completed successfully.")
        except Exception as e:
            print(f"Error in automatic periodic background sync: {e}")
        # Sleep for 10 minutes (600 seconds)
        time.sleep(600)

app = FastAPI(title="Smart Stock Recommendation API")

@app.on_event("startup")
def startup_event():
    # Start the daemon thread for periodic updates
    threading.Thread(target=periodic_sync_thread, daemon=True).start()

# Enable CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root(visited: str = Cookie(None)):
    index_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static", "index.html")
    if os.path.exists(index_path):
        response = FileResponse(index_path)
        if not visited:
            try:
                db.increment_visitor_count()
                # Set cookie to expire at midnight tonight
                now = datetime.now()
                seconds_until_midnight = ((24 - now.hour - 1) * 3600) + ((60 - now.minute - 1) * 60) + (60 - now.second)
                response.set_cookie(key="visited", value="1", max_age=max(1, seconds_until_midnight), httponly=True, path="/")
            except Exception as e:
                print(f"Error incrementing visitor count: {e}")
        return response
    return {"message": "Welcome to Smart Stock Recommendation API. Static frontend files not found yet."}

# Get Top 10 Buy and Top 10 Sell Stocks
@app.get("/api/top10")
def get_top10(market: str = "US"):
    market = market.upper()
    if market not in ["US", "KR", "ETF_US", "ETF_KR"]:
        raise HTTPException(status_code=400, detail="Invalid market. Use 'US', 'KR', 'ETF_US', or 'ETF_KR'.")
        
    buys = db.get_top10(market, order_by_buy=True)
    sells = db.get_top10(market, order_by_buy=False)
    
    return {
        "market": market,
        "buys": buys,
        "sells": sells
    }

# Search Stock by Name or Ticker (US / KR)
@app.get("/api/search")
def search_stock(q: str):
    if not q or not q.strip():
        raise HTTPException(status_code=400, detail="Search query cannot be empty.")
        
    query = q.strip()
    ticker_to_fetch = None
    name_override = None
    market = None
    
    # 1. Check if it matches a US stock Korean name mapping (e.g. "애플")
    mapped_us_ticker = db.get_us_ticker_by_korean_name(query)
    if mapped_us_ticker:
        ticker_to_fetch = mapped_us_ticker
        market = "ETF_US" if (mapped_us_ticker in scanner.TOP_US_ETFS) else "US"
    # 2. Determine if it is a US Ticker (alphabetic only, e.g. AAPL, PLTR, BRK-B)
    elif re.match(r"^[a-zA-Z\.\-]+$", query):
        ticker_to_fetch = query.upper()
        market = "ETF_US" if (ticker_to_fetch in scanner.TOP_US_ETFS) else "US"
    # 3. Determine if it is a 6-digit Korean Ticker (e.g. 005930)
    elif re.match(r"^\d{6}$", query):
        mapped = db.search_krx_ticker(query)
        if mapped:
            ticker_to_fetch, name_override = mapped
            ticker_clean = ticker_to_fetch.upper()
            market = "ETF_KR" if (ticker_clean in scanner.TOP_KR_ETFS) else "KR"
        else:
            # Fallback: Assume KOSPI (.KS)
            ticker_to_fetch = f"{query}.KS"
            market = "ETF_KR" if (ticker_to_fetch in scanner.TOP_KR_ETFS) else "KR"
    # 4. Assume Korean Stock Name (or KR ETF Name)
    else:
        mapped = db.search_krx_ticker(query)
        if mapped:
            ticker_to_fetch, name_override = mapped
            ticker_clean = ticker_to_fetch.upper()
            market = "ETF_KR" if (ticker_clean in scanner.TOP_KR_ETFS) else "KR"
        else:
            raise HTTPException(
                status_code=404, 
                detail=f"주식 종목 '{query}'을(를) 한국 거래소 매핑 테이블에서 찾을 수 없습니다. 미국 티커(예: AAPL) 또는 정확한 한국 종목명을 입력해주세요."
            )

    # Check database cache first
    cached_stock = db.get_stock(ticker_to_fetch)
    if cached_stock:
        # Check if cache is older than 5 minutes (300 seconds)
        cache_valid = False
        try:
            updated_time = datetime.strptime(cached_stock["updated_at"], "%Y-%m-%d %H:%M:%S")
            if (datetime.now() - updated_time).total_seconds() < 300:
                cache_valid = True
        except Exception:
            pass
            
        if cache_valid:
            return {
                "source": "cache",
                "stock": cached_stock
            }
        else:
            print(f"Cache expired or invalid for {ticker_to_fetch}. Fetching real-time update...")
        
    # Fetch from Yahoo Finance
    print(f"Fetching {ticker_to_fetch} dynamically...")
    stock_data = scanner.fetch_and_update_stock(ticker_to_fetch, name_override)
    
    if not stock_data:
        raise HTTPException(
            status_code=404, 
            detail=f"Yahoo Finance에서 '{ticker_to_fetch}' 정보를 가져오지 못했습니다. 올바른 티커인지 확인해 주세요."
        )
        
    # Since we added a new stock, recalculate ranks for that market to integrate it
    scanner.calculate_market_ranks(market)
    
    # Return the newly calculated stock
    updated_stock = db.get_stock(ticker_to_fetch)
    return {
        "source": "live",
        "stock": updated_stock
    }

# Endpoint to get DB status
@app.get("/api/status")
def get_status():
    conn = db.get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM stocks WHERE market = 'US'")
    us_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM stocks WHERE market = 'KR'")
    kr_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM stocks WHERE market = 'ETF_US'")
    etf_us_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM stocks WHERE market = 'ETF_KR'")
    etf_kr_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM krx_mapping")
    krx_mapping_count = cursor.fetchone()[0]
    
    conn.close()
    
    today_visitors, total_visitors = 0, 0
    try:
        today_visitors, total_visitors = db.get_visitor_stats()
    except Exception as e:
        print(f"Error fetching visitor stats: {e}")
    
    return {
        "us_cached_stocks": us_count,
        "kr_cached_stocks": kr_count,
        "etf_us_cached_stocks": etf_us_count,
        "etf_kr_cached_stocks": etf_kr_count,
        "total_krx_mapped_names": krx_mapping_count,
        "db_initialized": True,
        "today_visitors": today_visitors,
        "total_visitors": total_visitors
    }

# Endpoint to get Live Sync Progress (reported in Korean)
@app.get("/api/sync-progress")
def get_sync_progress():
    return scanner.sync_state

# Sync in the background
def bg_sync_task():
    print("Background synchronization started...")
    try:
        scanner.run_sync_all()
        print("Background synchronization completed successfully.")
    except Exception as e:
        print(f"Error in background sync: {e}")

@app.post("/api/sync")
def trigger_sync(background_tasks: BackgroundTasks):
    background_tasks.add_task(bg_sync_task)
    return {"status": "sync_started", "message": "전체 주식 종목 동기화가 백그라운드에서 시작되었습니다."}

# Mount static folder
static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")
