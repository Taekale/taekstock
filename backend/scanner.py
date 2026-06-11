# -*- coding: utf-8 -*-
import yfinance as yf
import pandas as pd
from datetime import datetime
import concurrent.futures
import requests
import time
from . import db
from .kis import kis_client

# Global requests session with customized User-Agent to bypass Yahoo Finance scrap-blocks / Crumb issues
yf_session = requests.Session()
yf_session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9,ko-KR;q=0.8,ko;q=0.7",
    "Connection": "keep-alive"
})


# Predefined Top 100 US Stock Tickers (S&P 100 / Nasdaq Mega Caps)
TOP_US_TICKERS = [
    "AAPL", "MSFT", "AMZN", "NVDA", "META", "GOOGL", "GOOG", "TSLA", "BRK-B", "LLY",
    "AVGO", "JPM", "UNH", "V", "MA", "COST", "HD", "PG", "NFLX", "AMD",
    "JNJ", "ABBV", "MRK", "ORCL", "WMT", "BAC", "PEP", "CVX", "KO", "TMO",
    "CRM", "ADBE", "ACN", "QCOM", "CSCO", "MCD", "ABT", "INTC", "TXN", "GE",
    "AMGN", "DIS", "ISRG", "IBM", "CAT", "AXP", "PFE", "PM", "MS", "NKE",
    "GS", "HON", "CMCSA", "BKNG", "COP", "SPGI", "LOW", "RTX", "AMAT", "TJX",
    "LRCX", "UNP", "PLTR", "PANW", "FI", "MU", "REGN", "UBER", "ETN", "MDT",
    "BMY", "DE", "SYK", "SBUX", "ADP", "LMT", "VRTX", "ELV", "CI", "GILD",
    "GEV", "MDLZ", "CRWD", "PGR", "ADI", "MMC", "BSX", "MELI", "CB", "ANET",
    "SO", "HCA", "KLAC", "WM", "DHR", "ZTS"
]

# Predefined Top 100 KR Stock Tickers (KOSPI & KOSDAQ Large Caps)
TOP_KR_TICKERS = [
    "005930.KS", "000660.KS", "373220.KS", "207940.KS", "005380.KS", "000270.KS", "068270.KS", "005490.KS", "035420.KS", "035720.KS",
    "051910.KS", "006400.KS", "105560.KS", "055550.KS", "302440.KQ", "012330.KS", "032830.KS", "066570.KS", "086790.KS", "096770.KS",
    "000810.KS", "033780.KS", "003550.KS", "015760.KS", "009150.KS", "017670.KS", "018260.KS", "011200.KS", "010950.KS", "251270.KS",
    "034730.KS", "005830.KS", "000720.KS", "004020.KS", "002790.KS", "088350.KS", "097950.KS", "028260.KS", "316140.KS", "326030.KS",
    "036570.KS", "009830.KS", "011170.KS", "024110.KS", "034220.KS", "161390.KS", "009540.KS", "010130.KS", "010140.KS", "280360.KS",
    "047050.KS", "051900.KS", "071050.KS", "090430.KS", "180640.KS", "267250.KS", "247540.KQ", "091990.KQ", "068760.KQ", "293490.KQ",
    "035900.KQ", "253450.KQ", "192080.KQ", "112040.KQ", "058470.KQ", "036830.KQ", "066970.KQ", "022100.KQ", "278280.KQ", "214150.KQ",
    "145020.KQ", "381970.KQ", "000100.KS", "000120.KS", "000210.KS", "000240.KS", "000990.KS", "001040.KS", "001450.KS", "001800.KS",
    "002380.KS", "003410.KS", "003490.KS", "004370.KS", "005250.KS", "005440.KS", "008770.KS", "009420.KS", "010060.KS", "010120.KS",
    "011070.KS", "011780.KS", "012450.KS", "014680.KS", "016360.KS", "017800.KS", "020150.KS", "021240.KS", "023530.KS", "029780.KS"
]

# Predefined Top US ETF Tickers
TOP_US_ETFS = [
    # 시장 지수 추종
    "SPY", "IVV", "VOO", "QQQ", "DIA", "IWM",
    # 가치/배당/배당성장
    "SCHD", "VYM", "SDY", "DVY", "DGRO", "VIG",
    # 채권 (단기, 중기, 장기, 하이일드)
    "TLT", "IEF", "SHY", "BND", "AGG", "LQD", "HYG",
    # 대표 섹터 및 테마 (반도체, 기술, 바이오, 금융 등)
    "SOXX", "SMH", "XLK", "XLV", "XLF", "XLY", "XLP", "XLE", "XLI", "XLB", "XLRE", "IBB", "XBI",
    # 레버리지 및 인버스
    "TQQQ", "SQQQ", "QLD", "SSO", "SDS", "SPXL", "SPXS", "SOXL", "SOXS"
]

# Predefined Top KR ETF Tickers
TOP_KR_ETFS = [
    # 국내 지수 추종 및 레버리지/인버스
    "069500.KS", "102110.KS", "122630.KS", "252670.KS", "114800.KS", 
    "229200.KS", "233740.KS", "251340.KS", "123320.KS", "252710.KS",
    # 미국 및 해외 지수 추종
    "360750.KS", "133690.KS", "381040.KS", "381170.KS", "458730.KS", 
    "446770.KS", "379800.KS", "453810.KS", "143850.KS", "407830.KS",
    # 국내외 섹터 및 테마 (2차전지, 반도체, 헬스케어, 차이나 등)
    "305720.KS", "305540.KS", "396500.KS", "091230.KS", "227540.KS", 
    "371460.KS", "423920.KS", "211900.KS", "210780.KS", "292150.KS", 
    "266370.KS", "329200.KS", "390310.KS", "102040.KS"
]

def fetch_single_stock_metrics(ticker_symbol, name_override=None):
    """
    Fetches raw stock details from Korea Investment Securities (KIS) or Yahoo Finance.
    Handles fallbacks dynamically if API key is not provided.
    """
    try:
        # 0. Check KIS API first for Korean stocks
        kis_data = None
        is_korean = ticker_symbol.endswith((".KS", ".KQ"))
        if is_korean and kis_client.is_available():
            kis_data = kis_client.fetch_domestic_stock_metrics(ticker_symbol)
            
        ticker = yf.Ticker(ticker_symbol, session=yf_session)
        
        # Parallel fetch for info and news to drastically reduce latency bottleneck
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            future_info = executor.submit(lambda: ticker.info)
            future_news = executor.submit(lambda: ticker.news)
            
            try:
                info = future_info.result(timeout=4.5)
            except Exception as e:
                print(f"yfinance info timeout/error for {ticker_symbol}: {e}")
                info = {}
                
            try:
                news = future_news.result(timeout=2.5)
            except Exception as e:
                print(f"yfinance news timeout/error for {ticker_symbol}: {e}")
                news = []
                
        # Fast Info Fallback if full info is missing or failed
        if not info or ("currentPrice" not in info and "regularMarketPrice" not in info and "previousClose" not in info):
            try:
                fast = ticker.fast_info
                if fast:
                    info["currentPrice"] = fast.get("lastPrice") or fast.get("last_price")
                    info["volume"] = fast.get("lastVolume") or fast.get("last_volume") or fast.get("volume")
                    info["fiftyDayAverage"] = fast.get("fiftyDayAverage") or fast.get("fifty_day_average")
                    info["twoHundredDayAverage"] = fast.get("twoHundredDayAverage") or fast.get("two_hundred_day_average")
            except Exception as e:
                print(f"yfinance fast_info fallback failed for {ticker_symbol}: {e}")
                
        if not info or ("currentPrice" not in info and "regularMarketPrice" not in info and "previousClose" not in info):
            if not kis_data:
                # Maybe invalid ticker or API failed completely
                return None
            info = {} # Empty fallback
            
        name = name_override or info.get("longName") or info.get("shortName") or ticker_symbol
        
        # Price
        if kis_data and kis_data.get("price"):
            price = kis_data["price"]
        else:
            price = info.get("currentPrice") or info.get("regularMarketPrice") or info.get("previousClose")
        
        # 1. PER (Price-to-Earnings Ratio) with Fallbacks
        if kis_data and kis_data.get("per") is not None:
            per = kis_data["per"]
        else:
            per = info.get("trailingPE")
            if per is None:
                per = info.get("forwardPE")
            if per is None:
                per = info.get("priceEpsCurrentYear")
            if per is None:
                eps = info.get("epsCurrentYear")
                if eps and price and eps != 0:
                    per = price / eps

        # 2. ROE (Return on Equity)
        roe = info.get("returnOnEquity")
        if roe is not None:
            # Store ROE as a percentage
            roe = roe * 100.0

        # 3. PBR (Price-to-Book Ratio) with Fallbacks
        if kis_data and kis_data.get("pbr") is not None:
            pbr = kis_data["pbr"]
        else:
            pbr = info.get("priceToBook")
            if pbr is None:
                # Calculate from: Equity = Net Income / ROE (as decimal)
                shares = info.get("sharesOutstanding")
                net_income = info.get("netIncomeToCommon")
                # Convert ROE back to decimal for calculation if needed
                roe_dec = (roe / 100.0) if roe else None
                if roe_dec and net_income and shares and price and roe_dec != 0 and shares != 0:
                    try:
                        equity = net_income / roe_dec
                        book_value_per_share = equity / shares
                        pbr = price / book_value_per_share
                    except ZeroDivisionError:
                        pbr = None

        # 4. PSR (Price-to-Sales Ratio) with Fallbacks
        psr = info.get("priceToSalesTrailing12Months")
        if psr is None:
            market_cap = info.get("marketCap")
            revenue = info.get("totalRevenue")
            if market_cap and revenue and revenue != 0:
                psr = market_cap / revenue

        # Check if it is an ETF
        is_etf_us = ticker_symbol in TOP_US_ETFS
        is_etf_kr = ticker_symbol in TOP_KR_ETFS
        if not (is_etf_us or is_etf_kr) and info.get("quoteType") == "ETF":
            if ticker_symbol.endswith((".KS", ".KQ")):
                is_etf_kr = True
            else:
                is_etf_us = True
            
        if is_etf_us:
            market = "ETF_US"
        elif is_etf_kr:
            market = "ETF_KR"
        else:
            market = "KR" if ticker_symbol.endswith((".KS", ".KQ")) else "US"
        
        # 5. Volume and Trading Value (거래량 및 거래대금)
        if kis_data:
            volume = kis_data.get("volume", 0)
            trading_value = kis_data.get("trading_value", 0.0)
        else:
            volume = info.get("volume") or info.get("regularMarketVolume") or info.get("averageVolume") or 0
            trading_value = price * volume if price and volume else 0.0

        # 6. Moving Averages for ETFs
        fifty_day_avg = info.get("fiftyDayAverage")
        two_hundred_day_avg = info.get("twoHundredDayAverage")

        # 7. News Sentiment Analysis (호재 점수)
        sentiment_score = 0.5 # Neutral fallback
        try:
            if news:
                pos_words = ["buy", "up", "growth", "profit", "surpass", "bullish", "upgrade", "beat", "positive", "high", "success", "gain", "raise", "increase", "jump", "호재", "상승", "성장", "흑자", "돌파", "매수", "개선"]
                neg_words = ["sell", "down", "loss", "decline", "bearish", "downgrade", "miss", "negative", "low", "fail", "risk", "drop", "fall", "decrease", "cut", "악재", "하락", "손실", "적자", "우려", "매도", "부진"]
                
                pos_count = 0
                neg_count = 0
                for article in news:
                    if not article or not isinstance(article, dict):
                        continue
                    title = article.get("title")
                    if not title or not isinstance(title, str):
                        continue
                    title_lower = title.lower()
                    has_pos = any(w in title_lower for w in pos_words)
                    has_neg = any(w in title_lower for w in neg_words)
                    if has_pos and not has_neg:
                        pos_count += 1
                    elif has_neg and not has_pos:
                        neg_count += 1
                
                total_classified = pos_count + neg_count
                if total_classified > 0:
                    sentiment_score = 0.5 + 0.5 * (pos_count - neg_count) / total_classified
        except Exception:
            pass
            
        # 8. Extra Growth & Fundamental Factors (PEG, Revenue/Earnings Growth, Debt, FCF, EPS)
        peg_ratio = info.get("pegRatio")
        revenue_growth = info.get("revenueGrowth")
        earnings_growth = info.get("earningsGrowth")
        debt_to_equity = info.get("debtToEquity")
        free_cash_flow = info.get("freeCashflow")
        eps = info.get("trailingEps") or info.get("forwardEps") or info.get("epsTrailingTwelveMonths")
            
        return {
            "ticker": ticker_symbol,
            "name": name,
            "market": market,
            "price": price,
            "per": per,
            "pbr": pbr,
            "psr": psr,
            "roe": roe,
            "volume": int(volume) if volume else 0,
            "trading_value": float(trading_value) if trading_value else 0.0,
            "sentiment_score": float(sentiment_score),
            "buy_score": None, # calculated in rank step
            "recommendation": None,
            "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "fifty_day_avg": fifty_day_avg,
            "two_hundred_day_avg": two_hundred_day_avg,
            "volume_power": kis_data.get("volume_power") if kis_data else None,
            "bid_ask_ratio": kis_data.get("bid_ask_ratio") if kis_data else None,
            "peg_ratio": float(peg_ratio) if peg_ratio is not None else None,
            "revenue_growth": float(revenue_growth) if revenue_growth is not None else None,
            "earnings_growth": float(earnings_growth) if earnings_growth is not None else None,
            "debt_to_equity": float(debt_to_equity) if debt_to_equity is not None else None,
            "free_cash_flow": float(free_cash_flow) if free_cash_flow is not None else None,
            "eps": float(eps) if eps is not None else None
        }
    except Exception as e:
        print(f"Error fetching metrics for {ticker_symbol}: {e}")
        return None

def fetch_and_update_stock(ticker_symbol, name_override=None):
    """
    Fetch stock metrics and save directly to DB cache.
    """
    data = fetch_single_stock_metrics(ticker_symbol, name_override)
    if data:
        db.save_stock(data)
        return data
    return None

def sync_krx_mappings_from_kind():
    """
    Downloads list of all listed Korean companies from KIND (KRX)
    and saves the mappings in the database.
    """
    try:
        url = 'http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13'
        df = pd.read_html(url, header=0, encoding='cp949')[0]
        
        mappings = []
        for _, row in df.iterrows():
            ticker_raw = str(row['종목코드']).zfill(6)
            name = str(row['회사명'])
            market_segment = str(row['시장구분'])
            
            # Map suffix based on market segment
            if "유가" in market_segment or "코스피" in market_segment:
                suffix = ".KS"
            elif "코스닥" in market_segment:
                suffix = ".KQ"
            else:
                # KONEX or others
                suffix = ".KQ"
                
            mappings.append({
                "ticker": ticker_raw,
                "name": name,
                "market_type": market_segment,
                "yf_ticker": f"{ticker_raw}{suffix}"
            })
            
        db.save_krx_mappings(mappings)
        print(f"Successfully synced {len(mappings)} KRX mappings from KIND.")
        return True
    except Exception as e:
        print(f"Error syncing mappings from KIND: {e}")
        return False

# Global background sync state (reported in Korean)
sync_state = {
    "status": "idle",
    "message": "대기 중",
    "percent": 0
}

progress_lock = concurrent.futures.thread.threading.Lock()
progress_counter = 0

def update_sync_state(status, message, percent):
    global sync_state
    sync_state["status"] = status
    sync_state["message"] = message
    sync_state["percent"] = percent
    print(f"[{percent}%] {message}")

def calculate_etf_ranks(market):
    """
    Loads all cached ETFs for the specified market, computes relative rankings based on Momentum + Liquidity + Sentiment,
    updates buy_score and recommendation, and writes back to DB.
    """
    stocks = db.get_all_cached_stocks(market)
    if not stocks:
        return
    df = pd.DataFrame(stocks)
    
    # 1. Momentum Score: fifty_day_avg / two_hundred_day_avg
    # If not available, use 1.0 (neutral)
    def calc_momentum(row):
        f50 = row.get("fifty_day_avg")
        f200 = row.get("two_hundred_day_avg")
        if f50 and f200 and f200 != 0:
            return float(f50) / float(f200)
        return 1.0
        
    df["momentum"] = df.apply(calc_momentum, axis=1)
    
    # Normalize Momentum: Higher is better
    df_mom = df.copy().sort_values(by="momentum", ascending=True)
    V = len(df_mom)
    df_mom["momentum_score"] = [(i / (V - 1) if V > 1 else 1.0) for i in range(V)]
    df = df.merge(df_mom[["ticker", "momentum_score"]], on="ticker", how="left")
    
    # 2. Volume/Liquidity Score: Higher is better
    df_vol = df[df["volume"].notna() & (df["volume"] > 0)].copy()
    if not df_vol.empty:
        df_vol = df_vol.sort_values(by="volume", ascending=True)
        V = len(df_vol)
        df_vol["volume_score"] = [(i / (V - 1) if V > 1 else 1.0) for i in range(V)]
    else:
        df_vol["volume_score"] = []
    df = df.merge(df_vol[["ticker", "volume_score"]], on="ticker", how="left")
    df["volume_score"] = df["volume_score"].fillna(0.0)
    
    # 3. News Sentiment Score: Higher is better
    df_sent = df[df["sentiment_score"].notna()].copy()
    if not df_sent.empty:
        df_sent = df_sent.sort_values(by="sentiment_score", ascending=True)
        V = len(df_sent)
        df_sent["sentiment_score_rank"] = [(i / (V - 1) if V > 1 else 1.0) for i in range(V)]
    else:
        df_sent["sentiment_score_rank"] = []
    df = df.merge(df_sent[["ticker", "sentiment_score_rank"]], on="ticker", how="left")
    df["sentiment_score_rank"] = df["sentiment_score_rank"].fillna(0.5)
    
    # Store previous buy score for EMA smoothing
    if "buy_score" in df.columns:
        df["prev_buy_score"] = df["buy_score"]
    else:
        df["prev_buy_score"] = None

    df["buy_score"] = (
        0.45 * df["momentum_score"] +
        0.40 * df["volume_score"] +
        0.15 * df["sentiment_score_rank"]
    )
    
    # Apply KIS supply/demand bonus to enhance KIS predictive accuracy for Korean ETFs
    if market == "ETF_KR" and 'volume_power' in df.columns:
        def apply_etf_kis_bonus(row):
            score = row['buy_score']
            if pd.isna(score) or score is None:
                return 0.5
            bonus = 0.0
            vp = row.get('volume_power')
            if vp is not None and not pd.isna(vp):
                if vp >= 120.0:
                    bonus += 0.05
                elif vp >= 100.0:
                    bonus += 0.02
            bar = row.get('bid_ask_ratio')
            if bar is not None and not pd.isna(bar):
                if bar >= 1.5:
                    bonus += 0.03
                elif bar >= 1.2:
                    bonus += 0.015
            return min(1.0, score + bonus)
        df['buy_score'] = df.apply(apply_etf_kis_bonus, axis=1)
    
    # Apply Exponential Moving Average (EMA) smoothing to prevent volatile ranking jumps
    alpha = 0.4
    def smooth_etf_score(row):
        new_val = row['buy_score']
        old_val = row.get('prev_buy_score')
        if old_val is not None and not pd.isna(old_val):
            return alpha * new_val + (1.0 - alpha) * old_val
        return new_val
    df['buy_score'] = df.apply(smooth_etf_score, axis=1)
    
    # Sort valid indices by score descending
    sorted_df = df.sort_values(by="buy_score", ascending=False)
    total_valid = len(sorted_df)
    
    for rank_idx, (_, row) in enumerate(sorted_df.iterrows()):
        percentile = rank_idx / (total_valid - 1) if total_valid > 1 else 0.5
        
        # Map percentile rank to rating
        if percentile <= 0.05:      # Top 5%
            recommendation = "강력 매수"
        elif percentile <= 0.25:    # Top 5% - 25% (Next 20%)
            recommendation = "매수"
        elif percentile <= 0.75:    # Top 25% - 75% (Middle 50%)
            recommendation = "관망"
        elif percentile <= 0.95:    # Top 75% - 95% (Next 20%)
            recommendation = "매도"
        else:                       # Bottom 5%
            recommendation = "강력 매도"
            
        db.save_stock({
            "ticker": row["ticker"],
            "name": row["name"],
            "market": row["market"],
            "price": row["price"],
            "per": None,
            "pbr": None,
            "psr": None,
            "roe": None,
            "volume": int(row["volume"]) if not pd.isna(row["volume"]) else 0,
            "trading_value": float(row["trading_value"]) if not pd.isna(row["trading_value"]) else 0.0,
            "sentiment_score": float(row["sentiment_score"]) if not pd.isna(row["sentiment_score"]) else 0.5,
            "buy_score": float(row["buy_score"]),
            "recommendation": recommendation,
            "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "fifty_day_avg": float(row["fifty_day_avg"]) if 'fifty_day_avg' in row and not pd.isna(row["fifty_day_avg"]) else None,
            "two_hundred_day_avg": float(row["two_hundred_day_avg"]) if 'two_hundred_day_avg' in row and not pd.isna(row["two_hundred_day_avg"]) else None,
            "volume_power": float(row["volume_power"]) if 'volume_power' in row and not pd.isna(row["volume_power"]) else None,
            "bid_ask_ratio": float(row["bid_ask_ratio"]) if 'bid_ask_ratio' in row and not pd.isna(row["bid_ask_ratio"]) else None,
        })
 
def calculate_market_ranks(market):
    """
    Loads all cached stocks for a market, computes relative rankings,
    trains a local XGBoost Factor Model, updates buy_score and recommendation,
    and writes back to DB.
    """
    if market in ["ETF_US", "ETF_KR"]:
        calculate_etf_ranks(market)
        return

    stocks = db.get_all_cached_stocks(market)
    if not stocks:
        return
    df = pd.DataFrame(stocks)
    # --- Part 1: Standard Relative Percentile Ranks ---
    # 1. PER score: Lower positive is better.
    df_per = df[df['per'].notna() & (df['per'] > 0)].copy()
    if not df_per.empty:
        df_per = df_per.sort_values(by='per', ascending=True)
        V = len(df_per)
        df_per['per_score'] = [1.0 - (i / (V - 1) if V > 1 else 0.0) for i in range(V)]
    else:
        df_per['per_score'] = []
    df = df.merge(df_per[['ticker', 'per_score']], on='ticker', how='left')
    df['per_score'] = df['per_score'].fillna(0.0)
    
    # 2. PBR score: Lower positive is better.
    df_pbr = df[df['pbr'].notna() & (df['pbr'] > 0)].copy()
    if not df_pbr.empty:
        df_pbr = df_pbr.sort_values(by='pbr', ascending=True)
        V = len(df_pbr)
        df_pbr['pbr_score'] = [1.0 - (i / (V - 1) if V > 1 else 0.0) for i in range(V)]
    else:
        df_pbr['pbr_score'] = []
    df = df.merge(df_pbr[['ticker', 'pbr_score']], on='ticker', how='left')
    df['pbr_score'] = df['pbr_score'].fillna(0.0)
    
    # 3. PSR score: Lower positive is better.
    df_psr = df[df['psr'].notna() & (df['psr'] > 0)].copy()
    if not df_psr.empty:
        df_psr = df_psr.sort_values(by='psr', ascending=True)
        V = len(df_psr)
        df_psr['psr_score'] = [1.0 - (i / (V - 1) if V > 1 else 0.0) for i in range(V)]
    else:
        df_psr['psr_score'] = []
    df = df.merge(df_psr[['ticker', 'psr_score']], on='ticker', how='left')
    df['psr_score'] = df['psr_score'].fillna(0.0)
    
    # 4. ROE score: Higher is better.
    df_roe = df[df['roe'].notna() & (df['roe'] > 0)].copy()
    if not df_roe.empty:
        df_roe = df_roe.sort_values(by='roe', ascending=True)
        V = len(df_roe)
        df_roe['roe_score'] = [(i / (V - 1) if V > 1 else 1.0) for i in range(V)]
    else:
        df_roe['roe_score'] = []
    df = df.merge(df_roe[['ticker', 'roe_score']], on='ticker', how='left')
    df['roe_score'] = df['roe_score'].fillna(0.0)
    
    # 5. Volume score: Higher is better.
    df_vol = df[df['volume'].notna() & (df['volume'] > 0)].copy()
    if not df_vol.empty:
        df_vol = df_vol.sort_values(by='volume', ascending=True)
        V = len(df_vol)
        df_vol['volume_score'] = [(i / (V - 1) if V > 1 else 1.0) for i in range(V)]
    else:
        df_vol['volume_score'] = []
    df = df.merge(df_vol[['ticker', 'volume_score']], on='ticker', how='left')
    df['volume_score'] = df['volume_score'].fillna(0.0)
    
    # 6. Trading Value score: Higher is better.
    df_val = df[df['trading_value'].notna() & (df['trading_value'] > 0)].copy()
    if not df_val.empty:
        df_val = df_val.sort_values(by='trading_value', ascending=True)
        V = len(df_val)
        df_val['trading_value_score'] = [(i / (V - 1) if V > 1 else 1.0) for i in range(V)]
    else:
        df_val['trading_value_score'] = []
    df = df.merge(df_val[['ticker', 'trading_value_score']], on='ticker', how='left')
    df['trading_value_score'] = df['trading_value_score'].fillna(0.0)
    
    # 7. Sentiment score rank: Higher is better.
    df_sent = df[df['sentiment_score'].notna()].copy()
    if not df_sent.empty:
        df_sent = df_sent.sort_values(by='sentiment_score', ascending=True)
        V = len(df_sent)
        df_sent['sentiment_score_rank'] = [(i / (V - 1) if V > 1 else 1.0) for i in range(V)]
    else:
        df_sent['sentiment_score_rank'] = []
    df = df.merge(df_sent[['ticker', 'sentiment_score_rank']], on='ticker', how='left')
    df['sentiment_score_rank'] = df['sentiment_score_rank'].fillna(0.5)
    
    # --- Part 2: XGBoost + Factor Model Integration ---
    try:
        import xgboost as xgb
        import numpy as np
        
        # Calculate Target Buy Score using the Advanced Growth & Liquidity Multi-Factor Model
        def get_factor_target_score(row):
            # 1. Base relative scores
            roe_s = row.get("roe_score", 0.0)
            sent_s = row.get("sentiment_score_rank", 0.5)
            per_s = row.get("per_score", 0.0)
            pbr_s = row.get("pbr_score", 0.0)
            psr_s = row.get("psr_score", 0.0)
            vol_s = row.get("volume_score", 0.0)
            val_s = row.get("trading_value_score", 0.0)
            
            # 2. Overbought (Disparity) Penalty: 이미 단기 급등한 종목은 후순위 배치
            price = row.get("price")
            ma50 = row.get("fifty_day_avg")
            overbought_penalty = 0.0
            if price and ma50 and not pd.isna(ma50) and ma50 > 0:
                ratio = price / ma50
                if ratio >= 1.25:
                    overbought_penalty = -0.15
                elif ratio >= 1.15:
                    overbought_penalty = -0.08
                elif ratio >= 1.08:
                    overbought_penalty = -0.03
                    
            # 3. Illiquidity Penalty: 거래대금 및 거래량이 극도로 적은 비인기 잡주 디스카운트
            # 거래량 및 거래대금 상대 평가의 평균이 하위 25% 이하인 경우 -0.25 강력 감점
            illiquidity_penalty = 0.0
            if (vol_s + val_s) / 2.0 <= 0.25:
                illiquidity_penalty = -0.25
                
            # 4. Growth & Value Bonus (매출 성장, EPS 성장, ROE, PEG, 부채비율, FCF)
            growth_bonus = 0.0
            rev_g = row.get("revenue_growth")
            earn_g = row.get("earnings_growth")
            roe_val = row.get("roe")
            peg = row.get("peg_ratio")
            debt = row.get("debt_to_equity")
            fcf = row.get("free_cash_flow")
            
            is_growth_stock = False
            # 매출 성장률 > 20%
            if rev_g is not None and not pd.isna(rev_g) and rev_g > 0.20:
                growth_bonus += 0.05
                is_growth_stock = True
            # EPS 성장률 > 25%
            if earn_g is not None and not pd.isna(earn_g) and earn_g > 0.25:
                growth_bonus += 0.05
                is_growth_stock = True
            # ROE > 15%
            if roe_val is not None and not pd.isna(roe_val) and roe_val > 15.0:
                growth_bonus += 0.05
            # PEG < 1
            if peg is not None and not pd.isna(peg) and 0.0 < peg < 1.0:
                growth_bonus += 0.06
                is_growth_stock = True
            # 부채비율 낮음 (< 100%)
            if debt is not None and not pd.isna(debt) and debt < 100.0:
                growth_bonus += 0.03
            # FCF 양수 (> 0)
            if fcf is not None and not pd.isna(fcf) and fcf > 0:
                growth_bonus += 0.03
                
            # 5. 고PER 완화 (성장률이 높고 PEG가 훌륭하면 고PER 감점 상쇄 보정)
            per_offset = 0.0
            if is_growth_stock and per_s < 0.5:
                per_offset = 0.10
                
            # Calculate final target score
            # Valuation (PER, PBR, PSR): 40% (각 13.3%)
            # Quality (ROE): 25%
            # Liquidity (Volume, Trading Value): 25% (각 12.5%) -> 실거래 대폭 반영
            # News Sentiment: 10%
            base_score = (
                0.25 * roe_s +
                0.10 * sent_s +
                0.133 * (per_s + per_offset) + 0.133 * pbr_s + 0.134 * psr_s +
                0.125 * vol_s + 0.125 * val_s
            )
            
            final_score = base_score + overbought_penalty + illiquidity_penalty + growth_bonus
            return min(1.0, max(0.0, final_score))

        df['target_score'] = df.apply(get_factor_target_score, axis=1)
        
        if len(df) < 15:
            # Fallback for small datasets (e.g. testing) to avoid XGBoost predicting mean
            df['xgb_buy_score'] = df['target_score']
        else:
            # We train XGBoost on both raw financial values (imputed) and relative ranks
            features = [
                'per', 'pbr', 'psr', 'roe', 'volume', 'trading_value', 'sentiment_score',
                'per_score', 'pbr_score', 'psr_score', 'roe_score', 'volume_score', 'trading_value_score', 'sentiment_score_rank'
            ]
            
            # Make a copy and impute missing/negative values for safe ML training
            train_df = df.copy()
            for col in ['per', 'pbr', 'psr', 'roe', 'volume', 'trading_value', 'sentiment_score']:
                median_val = train_df[train_df[col].notna() & (train_df[col] > 0)][col].median()
                if pd.isna(median_val) or median_val is None:
                    median_val = 0.0
                train_df[col] = train_df[col].fillna(median_val)
                # Clip negative raw values for model stability
                train_df.loc[train_df[col] < 0, col] = 0.0
                
            X = train_df[features].values
            y = train_df['target_score'].values
            
            # Train a local small-tree XGBoost model with regularization to prevent overfitting on ~100-200 stocks
            model = xgb.XGBRegressor(
                n_estimators=50,
                max_depth=3,
                learning_rate=0.08,
                subsample=0.8,
                colsample_bytree=0.8,
                reg_lambda=1.5,
                reg_alpha=0.5,
                random_state=42
            )
            model.fit(X, y)
            
            # Predict robust buy_scores
            predictions = model.predict(X)
            predictions = np.clip(predictions, 0.0, 1.0)
            df['xgb_buy_score'] = predictions
        
    except Exception as e:
        print(f"XGBoost training failed, falling back to standard scoring: {e}")
        # Use the exact same get_factor_target_score logic for fallback consistency
        df['xgb_buy_score'] = df['target_score']

    # Apply KIS supply/demand bonus to enhance KIS predictive accuracy
    if 'volume_power' in df.columns:
        def apply_kis_bonus(row):
            score = row['xgb_buy_score']
            if pd.isna(score) or score is None:
                return 0.5
            bonus = 0.0
            vp = row.get('volume_power')
            if vp is not None and not pd.isna(vp):
                if vp >= 120.0:
                    bonus += 0.05
                elif vp >= 100.0:
                    bonus += 0.02
            bar = row.get('bid_ask_ratio')
            if bar is not None and not pd.isna(bar):
                if bar >= 1.5:
                    bonus += 0.03
                elif bar >= 1.2:
                    bonus += 0.015
            return min(1.0, score + bonus)
        df['xgb_buy_score'] = df.apply(apply_kis_bonus, axis=1)
    
    # Apply Exponential Moving Average (EMA) smoothing to prevent volatile ranking jumps
    alpha = 0.4
    def smooth_score(row):
        new_val = row['xgb_buy_score']
        old_val = row.get('buy_score')
        if old_val is not None and not pd.isna(old_val):
            return alpha * new_val + (1.0 - alpha) * old_val
        return new_val
    df['xgb_buy_score'] = df.apply(smooth_score, axis=1)
    
    # Save scores and recommendations back to DB
    # Identify valid stocks and map their predicted buy_scores to relative percentiles
    valid_indices = []
    valid_scores = []
    
    for idx, row in df.iterrows():
        missing_count = sum(1 for field in ['per', 'pbr', 'psr', 'roe'] if pd.isna(row[field]) or row[field] is None or (field != 'roe' and row[field] <= 0))
        if missing_count < 3:
            valid_indices.append(idx)
            valid_scores.append(float(row['xgb_buy_score']))
            
    score_percentile_map = {}
    if valid_indices:
        # Sort valid indices by score descending (highest score gets rank 0)
        sorted_indices = [x for _, x in sorted(zip(valid_scores, valid_indices), reverse=True)]
        total_valid = len(sorted_indices)
        for rank_idx, idx in enumerate(sorted_indices):
            percentile = rank_idx / (total_valid - 1) if total_valid > 1 else 0.5
            score_percentile_map[idx] = percentile
            
    for idx, row in df.iterrows():
        missing_count = sum(1 for field in ['per', 'pbr', 'psr', 'roe'] if pd.isna(row[field]) or row[field] is None or (field != 'roe' and row[field] <= 0))
        
        if missing_count >= 3:
            buy_score = None
            recommendation = "데이터 부족"
        else:
            buy_score = float(row['xgb_buy_score'])
            percentile = score_percentile_map.get(idx, 0.5)
            
            # Map percentile rank to rating
            if percentile <= 0.05:      # Top 5%
                recommendation = "강력 매수"
            elif percentile <= 0.25:    # Top 5% - 25% (Next 20%)
                recommendation = "매수"
            elif percentile <= 0.75:    # Top 25% - 75% (Middle 50%)
                recommendation = "관망"
            elif percentile <= 0.95:    # Top 75% - 95% (Next 20%)
                recommendation = "매도"
            else:                       # Bottom 5%
                recommendation = "강력 매도"
                
        db.save_stock({
            "ticker": row["ticker"],
            "name": row["name"],
            "market": row["market"],
            "price": row["price"],
            "per": float(row["per"]) if not pd.isna(row["per"]) else None,
            "pbr": float(row["pbr"]) if not pd.isna(row["pbr"]) else None,
            "psr": float(row["psr"]) if not pd.isna(row["psr"]) else None,
            "roe": float(row["roe"]) if not pd.isna(row["roe"]) else None,
            "volume": int(row["volume"]) if not pd.isna(row["volume"]) else 0,
            "trading_value": float(row["trading_value"]) if not pd.isna(row["trading_value"]) else 0.0,
            "sentiment_score": float(row["sentiment_score"]) if not pd.isna(row["sentiment_score"]) else 0.5,
            "buy_score": buy_score,
            "recommendation": recommendation,
            "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "fifty_day_avg": float(row["fifty_day_avg"]) if 'fifty_day_avg' in row and not pd.isna(row["fifty_day_avg"]) else None,
            "two_hundred_day_avg": float(row["two_hundred_day_avg"]) if 'two_hundred_day_avg' in row and not pd.isna(row["two_hundred_day_avg"]) else None,
            "volume_power": float(row["volume_power"]) if 'volume_power' in row and not pd.isna(row["volume_power"]) else None,
            "bid_ask_ratio": float(row["bid_ask_ratio"]) if 'bid_ask_ratio' in row and not pd.isna(row["bid_ask_ratio"]) else None,
            "peg_ratio": float(row["peg_ratio"]) if 'peg_ratio' in row and not pd.isna(row["peg_ratio"]) else None,
            "revenue_growth": float(row["revenue_growth"]) if 'revenue_growth' in row and not pd.isna(row["revenue_growth"]) else None,
            "earnings_growth": float(row["earnings_growth"]) if 'earnings_growth' in row and not pd.isna(row["earnings_growth"]) else None,
            "debt_to_equity": float(row["debt_to_equity"]) if 'debt_to_equity' in row and not pd.isna(row["debt_to_equity"]) else None,
            "free_cash_flow": float(row["free_cash_flow"]) if 'free_cash_flow' in row and not pd.isna(row["free_cash_flow"]) else None,
            "eps": float(row["eps"]) if 'eps' in row and not pd.isna(row["eps"]) else None,
        })

def run_sync_all():
    """
    Runs background sync for all pre-defined top US and KR stocks,
    populating metrics and calculating overall ranks.
    """
    global progress_counter
    
    # Reset progress counter
    with progress_lock:
        progress_counter = 0
        
    # 1. Sync KRX name mapping
    update_sync_state("running", "한국거래소(KRX) 상장 종목 목록 다운로드 및 이름 매핑 중...", 5)
    sync_krx_mappings_from_kind()
    update_sync_state("running", "상장사 매핑 완료 (2,700여개 종목 완료). 미국 주식 데이터 수집 시작...", 15)
    
    # 2. Fetch US stocks
    total_us = len(TOP_US_TICKERS)
    
    def fetch_us_task(ticker):
        global progress_counter
        # Introduce a micro delay to prevent rate limit blocks
        time.sleep(0.3)
        fetch_and_update_stock(ticker)
        with progress_lock:
            progress_counter += 1
            pct = 15 + int(30 * progress_counter / total_us) # goes from 15% to 45%
            update_sync_state("running", f"미국 대표 주식 재무 정보 수집 중 ({progress_counter}/{total_us})...", pct)
            
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(fetch_us_task, t) for t in TOP_US_TICKERS]
        concurrent.futures.wait(futures)
        
    update_sync_state("running", "미국 주식 지표 수집 완료. XGBoost + 팩터 가치 평가 모델 빌드 중...", 46)
    calculate_market_ranks("US")
    update_sync_state("running", "미국 주식 랭킹 모델 빌드 완료. 한국 주식 데이터 수집 시작...", 50)
    
    # Reset progress counter for KR stocks
    with progress_lock:
        progress_counter = 0
        
    # 3. Fetch KR stocks
    total_kr = len(TOP_KR_TICKERS)
    kr_tickers_with_names = []
    for ticker in TOP_KR_TICKERS:
        clean_code = ticker.split('.')[0]
        mapped = db.search_krx_ticker(clean_code)
        name_override = mapped[1] if mapped else None
        kr_tickers_with_names.append((ticker, name_override))
        
    def fetch_kr_task(ticker, name):
        global progress_counter
        # Introduce a micro delay to prevent rate limit blocks
        time.sleep(0.2)
        fetch_and_update_stock(ticker, name)
        with progress_lock:
            progress_counter += 1
            pct = 50 + int(25 * progress_counter / total_kr) # goes from 50% to 75%
            update_sync_state("running", f"한국 대표 주식 재무 정보 수집 중 ({progress_counter}/{total_kr})...", pct)
            
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(fetch_kr_task, t, n) for t, n in kr_tickers_with_names]
        concurrent.futures.wait(futures)
        
    update_sync_state("running", "한국 주식 지표 수집 완료. XGBoost + 팩터 가치 평가 모델 빌드 중...", 77)
    calculate_market_ranks("KR")

    # 4. Fetch ETFs
    update_sync_state("running", "한국 및 미국 대표 ETF 데이터 수집 시작...", 80)
    all_etf_tickers = TOP_US_ETFS + TOP_KR_ETFS
    total_etfs = len(all_etf_tickers)
    etfs_with_names = []
    for ticker in all_etf_tickers:
        name_override = None
        if ticker.endswith((".KS", ".KQ")):
            clean_code = ticker.split('.')[0]
            mapped = db.search_krx_ticker(clean_code)
            name_override = mapped[1] if mapped else None
        etfs_with_names.append((ticker, name_override))
        
    with progress_lock:
        progress_counter = 0
        
    def fetch_etf_task(ticker, name):
        global progress_counter
        # Introduce a micro delay to prevent rate limit blocks
        time.sleep(0.2)
        fetch_and_update_stock(ticker, name)
        with progress_lock:
            progress_counter += 1
            pct = 80 + int(15 * progress_counter / total_etfs) # goes from 80% to 95%
            update_sync_state("running", f"ETF 정보 수집 및 분석 중 ({progress_counter}/{total_etfs})...", pct)
            
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(fetch_etf_task, t, n) for t, n in etfs_with_names]
        concurrent.futures.wait(futures)
        
    update_sync_state("running", "ETF 지표 수집 완료. ETF 모멘텀 평가 모델 빌드 중...", 97)
    calculate_market_ranks("ETF_US")
    calculate_market_ranks("ETF_KR")
    
    update_sync_state("idle", "모든 미국, 한국 주식 및 ETF 데이터 동기화와 가치 분석 평가가 성공적으로 완료되었습니다!", 100)
