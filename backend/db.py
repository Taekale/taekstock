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
            market TEXT NOT NULL,
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
            updated_at TEXT,
            fifty_day_avg REAL,
            two_hundred_day_avg REAL,
            volume_power REAL,
            bid_ask_ratio REAL,
            peg_ratio REAL,
            revenue_growth REAL,
            earnings_growth REAL,
            debt_to_equity REAL,
            free_cash_flow REAL,
            eps REAL
        )
    """)
    
    # Run self-healing schema migration to add new columns if they don't exist
    for column, col_type in [
        ("volume", "INTEGER"), 
        ("trading_value", "REAL"), 
        ("sentiment_score", "REAL"),
        ("fifty_day_avg", "REAL"),
        ("two_hundred_day_avg", "REAL"),
        ("volume_power", "REAL"),
        ("bid_ask_ratio", "REAL"),
        ("peg_ratio", "REAL"),
        ("revenue_growth", "REAL"),
        ("earnings_growth", "REAL"),
        ("debt_to_equity", "REAL"),
        ("free_cash_flow", "REAL"),
        ("eps", "REAL")
    ]:
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

    # Visitor statistics table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS visitor_stats (
            date TEXT PRIMARY KEY, -- 'YYYY-MM-DD'
            count INTEGER DEFAULT 0
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
    "메타": ("META", "Meta Platforms, Inc."),
    # KR ETFs
    "kodex 200": ("069500.KS", "KODEX 200"),
    "kodex200": ("069500.KS", "KODEX 200"),
    "kodex 레버리지": ("122630.KS", "KODEX 레버리지"),
    "kodex레버리지": ("122630.KS", "KODEX 레버리지"),
    "kodex 200선물인버스2x": ("252670.KS", "KODEX 200선물인버스2X"),
    "kodex 200 선물인버스 2x": ("252670.KS", "KODEX 200선물인버스2X"),
    "곱버스": ("252670.KS", "KODEX 200선물인버스2X"),
    "kodex 인버스": ("114800.KS", "KODEX 인버스"),
    "kodex인버스": ("114800.KS", "KODEX 인버스"),
    "kodex 코스닥150레버리지": ("229200.KS", "KODEX 코스닥150레버리지"),
    "kodex 코스닥150 레버리지": ("229200.KS", "KODEX 코스닥150레버리지"),
    "kodex코스닥150레버리지": ("229200.KS", "KODEX 코스닥150레버리지"),
    "kodex 코스닥150선물인버스": ("251340.KS", "KODEX 코스닥150선물인버스"),
    "kodex코스닥150선물인버스": ("251340.KS", "KODEX 코스닥150선물인버스"),
    "kodex 미국나스닥100레버리지": ("379800.KS", "KODEX 미국나스닥100레버리지(합성 H)"),
    "kodex미국나스닥100레버리지": ("379800.KS", "KODEX 미국나스닥100레버리지(합성 H)"),
    "plus 미국테크top10": ("453810.KS", "PLUS 미국테크TOP10"),
    "plus미국테크top10": ("453810.KS", "PLUS 미국테크TOP10"),
    "tiger 2차전지테마": ("305720.KS", "TIGER 2차전지테마"),
    "tiger2차전지테마": ("305720.KS", "TIGER 2차전지테마"),
    # US ETFs
    "spy": ("SPY", "SPDR S&P 500 ETF Trust"),
    "ivv": ("IVV", "iShares Core S&P 500 ETF"),
    "voo": ("VOO", "Vanguard S&P 500 ETF"),
    "qqq": ("QQQ", "Invesco QQQ Trust"),
    "dia": ("DIA", "SPDR Dow Jones Industrial Average ETF Trust"),
    "iwm": ("IWM", "iShares Russell 2000 ETF"),
    "soxx": ("SOXX", "iShares Semiconductor ETF"),
    "smh": ("SMH", "VanEck Semiconductor ETF"),
    "tqqq": ("TQQQ", "ProShares UltraPro QQQ"),
    "sqqq": ("SQQQ", "ProShares UltraPro Short QQQ"),
    "jepi": ("JEPI", "JPMorgan Equity Premium Income ETF"),
    "schd": ("SCHD", "Schwab U.S. Dividend Equity ETF"),
    "tlt": ("TLT", "iShares 20+ Year Treasury Bond ETF"),
    "슈드": ("SCHD", "Schwab U.S. Dividend Equity ETF")
}

US_KOREAN_NAMES = {
    "애플": "AAPL", "마이크로소프트": "MSFT", "아마존": "AMZN", "엔비디아": "NVDA", "메타": "META",
    "구글": "GOOGL", "테슬라": "TSLA", "버크셔해서웨이": "BRK-B", "버크셔 해서웨이": "BRK-B", "일라이릴리": "LLY", "일라이 릴리": "LLY",
    "브로드컴": "AVGO", "jp모건": "JPM", "유나이티드헬스": "UNH", "비자": "V", "마스터카드": "MA",
    "코스트코": "COST", "홈디포": "HD", "프록터앤갬블": "PG", "프록터 앤 갬블": "PG", "넷플릭스": "NFLX", "amd": "AMD",
    "존슨앤존슨": "JNJ", "애브비": "ABBV", "머크": "MRK", "오라클": "ORCL", "월마트": "WMT",
    "뱅크오브아메리카": "BAC", "펩시코": "PEP", "쉐브론": "CVX", "코카콜라": "KO", "써모피셔": "TMO",
    "세일즈포스": "CRM", "어도비": "ADBE", "액센츄어": "ACN", "퀄컴": "QCOM", "시스코": "CSCO",
    "맥도날드": "MCD", "애보트": "ABT", "인텔": "INTC", "텍사스인스트루먼트": "TXN", "제너럴일렉트릭": "GE",
    "암젠": "AMGN", "디즈니": "DIS", "인튜이티브서지컬": "ISRG", "ibm": "IBM", "캐터필러": "CAT",
    "아메리칸익스프레스": "AXP", "화이자": "PFE", "필립모리스": "PM", "모건스탠리": "MS", "나이키": "NKE",
    "골드만삭스": "GS", "하니웰": "HON", "컴캐스트": "CMCSA", "부킹홀딩스": "BKNG", "코노코필립스": "COP",
    "s&p글로벌": "SPGI", "로우스": "LOW", "레이시온": "RTX", "어플라이드머티어리얼즈": "AMAT", "tjx": "TJX",
    "램리서치": "LRCX", "유니온퍼시픽": "UNP", "팔란티어": "PLTR", "팔로알토": "PANW", "피서브": "FI",
    "마이크론": "MU", "리제네론": "REGN", "우버": "UBER", "이튼": "ETN", "메드트로닉": "MDT",
    "브리스톨마이어스": "BMY", "디어앤컴퍼니": "DE", "스트라이커": "SYK", "스타벅스": "SBUX", "adp": "ADP",
    "록히드마틴": "LMT", "버텍스": "VRTX", "엘레반스": "ELV", "시그나": "CI", "길리어드": "GILD",
    "ge베르노바": "GEV", "몬델리즈": "MDLZ", "크라우드스트라이크": "CRWD", "프로그레시브": "PGR", "아날로그디바이스": "ADI",
    "마쉬앤맥레넌": "MMC", "보스턴사이언티픽": "BSX", "메르카도리브레": "MELI", "처브": "CB", "아리스타": "ANET",
    "서던컴퍼니": "SO", "hca헬스케어": "HCA", "kla": "KLAC", "웨이스트매니지먼트": "WM", "다나허": "DHR", "조에티스": "ZTS",
    # ETFs
    "spy": "SPY", "sp500": "SPY", "ivv": "IVV", "voo": "VOO", "qqq": "QQQ", "나스닥100": "QQQ", "dia": "DIA",
    "다우존스": "DIA", "iwm": "IWM", "러셀2000": "IWM", "soxx": "SOXX", "필라델피아반도체": "SOXX",
    "smh": "SMH", "tqqq": "TQQQ", "sqqq": "SQQQ", "jepi": "JEPI", "schd": "SCHD", "슈드": "SCHD", "tlt": "TLT"
}

def get_us_ticker_by_korean_name(query):
    """
    Search US tickers by Korean name mapping.
    """
    q = query.strip().replace(" ", "").lower()
    if q in US_KOREAN_NAMES:
        return US_KOREAN_NAMES[q]
    
    # Also check if query matches any Korean name as substring/partial
    for name, ticker in US_KOREAN_NAMES.items():
        if name in q or q in name:
            return ticker
    return None

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
    stock_data: dict with ticker, name, market, price, per, pbr, psr, roe, volume, trading_value, sentiment_score, buy_score, recommendation, updated_at, fifty_day_avg, two_hundred_day_avg, volume_power, bid_ask_ratio
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Ensure all required keys exist in the dict to prevent sqlite3.ProgrammingError
    required_keys = [
        "per", "pbr", "psr", "roe", "volume", "trading_value", "sentiment_score", 
        "buy_score", "recommendation", "fifty_day_avg", "two_hundred_day_avg", 
        "volume_power", "bid_ask_ratio", "peg_ratio", "revenue_growth", 
        "earnings_growth", "debt_to_equity", "free_cash_flow", "eps"
    ]
    for k in required_keys:
        if k not in stock_data:
            stock_data[k] = None

    cursor.execute("""
        INSERT OR REPLACE INTO stocks (
            ticker, name, market, price, per, pbr, psr, roe, volume, trading_value, 
            sentiment_score, buy_score, recommendation, updated_at, fifty_day_avg, 
            two_hundred_day_avg, volume_power, bid_ask_ratio, peg_ratio, 
            revenue_growth, earnings_growth, debt_to_equity, free_cash_flow, eps
        )
        VALUES (
            :ticker, :name, :market, :price, :per, :pbr, :psr, :roe, :volume, :trading_value, 
            :sentiment_score, :buy_score, :recommendation, :updated_at, :fifty_day_avg, 
            :two_hundred_day_avg, :volume_power, :bid_ask_ratio, :peg_ratio, 
            :revenue_growth, :earnings_growth, :debt_to_equity, :free_cash_flow, :eps
        )
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

def get_top30(market, order_by_buy=True):
    """
    Returns top 30 stocks based on buy_score.
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
            LIMIT 30
        """, (market,))
    else:
        cursor.execute(f"""
            SELECT * FROM stocks 
            WHERE market = ? AND buy_score IS NOT NULL AND recommendation IN ('강력 매도', '매도')
            ORDER BY buy_score {order}, ticker ASC
            LIMIT 30
        """, (market,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def increment_visitor_count():
    today = datetime.now().strftime("%Y-%m-%d")
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO visitor_stats (date, count)
        VALUES (?, 1)
        ON CONFLICT(date) DO UPDATE SET count = count + 1
    """, (today,))
    conn.commit()
    conn.close()

def get_visitor_stats():
    today = datetime.now().strftime("%Y-%m-%d")
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Today's count
    cursor.execute("SELECT count FROM visitor_stats WHERE date = ?", (today,))
    row = cursor.fetchone()
    today_count = row["count"] if row else 0
    
    # Cumulative count
    cursor.execute("SELECT SUM(count) FROM visitor_stats")
    cum_row = cursor.fetchone()
    cumulative_count = cum_row[0] if cum_row and cum_row[0] is not None else 0
    
    conn.close()
    return today_count, cumulative_count
