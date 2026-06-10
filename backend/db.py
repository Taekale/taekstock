# -*- coding: utf-8 -*-
import sqlite3
import os
from datetime import datetime

DB_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "stocks.db")

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Stocks metrics cache table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stocks (
            ticker TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            market TEXT NOT NULL, -- 'US' or 'KR'
            price REAL,
            per REAL,
            pbr REAL,
            psr REAL,
            roe REAL,
            volume INTEGER,
            trading_value REAL,
            sentiment_score REAL,
            buy_score REAL,
            recommendation TEXT,
            updated_at TEXT
        )
    """)
    
    # Run self-healing schema migration to add new columns if they don't exist
    for column, col_type in [("volume", "INTEGER"), ("trading_value", "REAL"), ("sentiment_score", "REAL")]:
        try:
            cursor.execute(f"ALTER TABLE stocks ADD COLUMN {column} {col_type}")
        except sqlite3.OperationalError:
            # Column already exists
            pass
            
    # Purge any old test/dummy data
    cursor.execute("DELETE FROM stocks WHERE ticker = 'TEST.US' OR market = 'TEST_MKT' OR ticker LIKE '%TEST%'")
    
    # Complete KRX ticker name mapping table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS krx_mapping (
            ticker TEXT PRIMARY KEY, -- 6 digit KRX code e.g. '005930'
            name TEXT NOT NULL,      -- Korean company name e.g. '삼성전자'
            market_type TEXT,        -- '코스피', '코스닥'
            yf_ticker TEXT NOT NULL  -- yfinance format e.g. '005930.KS'
        )
    """)
    
    conn.commit()
    conn.close()

def save_krx_mappings(mappings):
    """
    mappings: list of dicts with keys: ticker, name, market_type, yf_ticker
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.executemany("""
        INSERT OR REPLACE INTO krx_mapping (ticker, name, market_type, yf_ticker)
        VALUES (:ticker, :name, :market_type, :yf_ticker)
    """, mappings)
    conn.commit()
    conn.close()

# Common Korean short names and translations to official tickers
ALIASES = {
    "현대차": ("005380.KS", "현대자동차"),
    "현대자동차": ("005380.KS", "현대자동차"),
    "삼성전자": ("005930.KS", "삼성전자"),
    "sk하이닉스": ("000660.KS", "SK하이닉스"),
    "하이닉스": ("000660.KS", "SK하이닉스"),
    "카카오": ("035720.KS", "카카오"),
    "네이버": ("035420.KS", "NAVER"),
    "naver": ("035420.KS", "NAVER"),
    "엔비디아": ("NVDA", "NVIDIA Corporation"),
    "애플": ("AAPL", "Apple Inc."),
    "테슬라": ("TSLA", "Tesla, Inc."),
    "아마존": ("AMZN", "Amazon.com, Inc."),
    "구글": ("GOOGL", "Alphabet Inc."),
    "메타": ("META", "Meta Platforms, Inc.")
}

def search_krx_ticker(query):
    """
    Search by name or ticker in Korea Exchange.
    Returns yf_ticker and name.
    """
    query_clean = query.strip().lower()
    
    # 0. Check alias dictionary first
    if query_clean in ALIASES:
        return ALIASES[query_clean]
        
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 1. Search in cached major 'stocks' table first to prioritize large caps
    cursor.execute("""
        SELECT ticker, name FROM stocks 
        WHERE ticker = ? OR name = ?
        LIMIT 1
    """, (query, query))
    row = cursor.fetchone()
    
    if not row:
        cursor.execute("""
            SELECT ticker, name FROM stocks 
            WHERE name LIKE ? 
            ORDER BY length(name) ASC
            LIMIT 1
        """, (f"%{query}%",))
        row = cursor.fetchone()
        
    if not row:
        # Character-spaced wildcard search (e.g. "현대차" -> "%현%대%차%")
        spaced_query = "%" + "%".join(list(query)) + "%"
        cursor.execute("""
            SELECT ticker, name FROM stocks 
            WHERE name LIKE ? 
            ORDER BY length(name) ASC
            LIMIT 1
        """, (spaced_query,))
        row = cursor.fetchone()
        
    if row:
        ticker_val = row["ticker"]
        name_val = row["name"]
        conn.close()
        return ticker_val, name_val
        
    # 2. Search in complete krx_mapping table
    cursor.execute("""
        SELECT yf_ticker, name FROM krx_mapping 
        WHERE ticker = ? OR name = ?
        LIMIT 1
    """, (query, query))
    row = cursor.fetchone()
    
    if not row:
        cursor.execute("""
            SELECT yf_ticker, name FROM krx_mapping 
            WHERE name LIKE ? 
            ORDER BY length(name) ASC
            LIMIT 1
        """, (f"%{query}%",))
        row = cursor.fetchone()
        
    if not row:
        # Character-spaced wildcard search (e.g. "현대차" -> "%현%대%차%")
        spaced_query = "%" + "%".join(list(query)) + "%"
        cursor.execute("""
            SELECT yf_ticker, name FROM krx_mapping 
            WHERE name LIKE ? 
            ORDER BY length(name) ASC
            LIMIT 1
        """, (spaced_query,))
        row = cursor.fetchone()
    
    conn.close()
    if row:
        return row["yf_ticker"], row["name"]
    return None

def save_stock(stock_data):
    """
    stock_data: dict with ticker, name, market, price, per, pbr, psr, roe, volume, trading_value, sentiment_score, buy_score, recommendation, updated_at
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO stocks (ticker, name, market, price, per, pbr, psr, roe, volume, trading_value, sentiment_score, buy_score, recommendation, updated_at)
        VALUES (:ticker, :name, :market, :price, :per, :pbr, :psr, :roe, :volume, :trading_value, :sentiment_score, :buy_score, :recommendation, :updated_at)
    """, stock_data)
    conn.commit()
    conn.close()

def get_stock(ticker):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM stocks WHERE ticker = ?", (ticker,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return dict(row)
    return None

def get_all_cached_stocks(market=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    if market:
        cursor.execute("SELECT * FROM stocks WHERE market = ?", (market,))
    else:
        cursor.execute("SELECT * FROM stocks")
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_top10(market, order_by_buy=True):
    """
    Returns top 10 stocks based on buy_score.
    If order_by_buy is True, return highest scores (Buy) with recommendation IN ('강력 매수', '매수').
    If False, return lowest scores (Sell) with recommendation IN ('강력 매도', '매도').
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    order = "DESC" if order_by_buy else "ASC"
    # Filter out stocks that are Neutral (관망)
    if order_by_buy:
        cursor.execute(f"""
            SELECT * FROM stocks 
            WHERE market = ? AND buy_score IS NOT NULL AND recommendation IN ('강력 매수', '매수')
            ORDER BY buy_score {order}, ticker ASC
            LIMIT 10
        """, (market,))
    else:
        cursor.execute(f"""
            SELECT * FROM stocks 
            WHERE market = ? AND buy_score IS NOT NULL AND recommendation IN ('강력 매도', '매도')
            ORDER BY buy_score {order}, ticker ASC
            LIMIT 10
        """, (market,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]
