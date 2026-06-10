import os
import sys
import unittest
import pandas as pd
from datetime import datetime

# Add root folder to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend import db, scanner

class TestStockRecommendationLogic(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        # Initialize the database file
        db.init_db()
        
    def tearDown(self):
        # Clear test database pollution
        conn = db.get_db_connection()
        conn.execute("DELETE FROM stocks WHERE ticker = 'TEST.US'")
        conn.execute("DELETE FROM stocks WHERE market = 'TEST_MKT'")
        conn.execute("DELETE FROM stocks WHERE ticker = 'A.TEST' OR ticker = 'B.TEST' OR ticker = 'C.TEST'")
        conn.commit()
        conn.close()
        
    def test_01_db_operations(self):
        print("\n[Test 1] Testing Database CRUD...")
        # Save a test stock
        test_stock = {
            "ticker": "TEST.US",
            "name": "Test Company",
            "market": "US",
            "price": 100.0,
            "per": 10.0,
            "pbr": 1.0,
            "psr": 1.0,
            "roe": 10.0,
            "volume": 10000,
            "trading_value": 1000000.0,
            "sentiment_score": 0.5,
            "buy_score": 0.85,
            "recommendation": "강력 매수",
            "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        db.save_stock(test_stock)
        
        # Retrieve and verify
        retrieved = db.get_stock("TEST.US")
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved["name"], "Test Company")
        self.assertEqual(retrieved["buy_score"], 0.85)
        self.assertEqual(retrieved["recommendation"], "강력 매수")
        
        # Test Top 10 retrieval
        top10_buys = db.get_top10("US", order_by_buy=True)
        self.assertTrue(len(top10_buys) > 0)
        self.assertEqual(top10_buys[0]["ticker"], "TEST.US")
        print("Database CRUD operations passed.")

    def test_02_krx_mapping_search(self):
        print("\n[Test 2] Testing KRX mapping search...")
        # Populate mapping database with dummy data
        dummy_mappings = [
            {"ticker": "999001", "name": "테스트바이오", "market_type": "코스닥", "yf_ticker": "999001.KQ"},
            {"ticker": "999002", "name": "테스트전자", "market_type": "코스피", "yf_ticker": "999002.KS"},
        ]
        db.save_krx_mappings(dummy_mappings)
        
        # Exact match name
        res = db.search_krx_ticker("테스트전자")
        self.assertIsNotNone(res)
        self.assertEqual(res[0], "999002.KS")
        
        # Partial match name
        res_partial = db.search_krx_ticker("스트바이오")
        self.assertIsNotNone(res_partial)
        self.assertEqual(res_partial[0], "999001.KQ")
        
        # Exact match ticker
        res_ticker = db.search_krx_ticker("999001")
        self.assertIsNotNone(res_ticker)
        self.assertEqual(res_ticker[1], "테스트바이오")
        print("KRX mapping search passed.")

    def test_03_yfinance_fetch_and_calculation(self):
        print("\n[Test 3] Testing Live Yahoo Finance fetch and metrics calculation...")
        # Fetch Apple Inc.
        metrics = scanner.fetch_single_stock_metrics("AAPL")
        self.assertIsNotNone(metrics)
        self.assertEqual(metrics["ticker"], "AAPL")
        self.assertEqual(metrics["market"], "US")
        self.assertGreater(metrics["price"], 0)
        self.assertGreater(metrics["per"], 0)
        self.assertGreater(metrics["pbr"], 0)
        self.assertGreater(metrics["psr"], 0)
        self.assertGreater(metrics["roe"], 0)
        
        print("Live fetch metrics parsed for AAPL:")
        print(f"  Price: {metrics['price']}")
        print(f"  PER: {metrics['per']}")
        print(f"  PBR: {metrics['pbr']}")
        print(f"  PSR: {metrics['psr']}")
        print(f"  ROE: {metrics['roe']}%")
        print("yfinance fetch and calculation passed.")

    def test_04_ranking_logic(self):
        print("\n[Test 4] Testing relative ranking & scoring logic...")
        # Populate DB with mock market stocks
        # We create a simple universe of 3 stocks to verify sorting and scoring
        
        # Clear existing cached US stocks first for controlled testing
        conn = db.get_db_connection()
        conn.execute("DELETE FROM stocks WHERE market = 'TEST_MKT'")
        conn.commit()
        conn.close()
        
        # Stock A: Cheap and highly profitable (Should be Strong Buy)
        # PER = 5 (low), PBR = 0.5 (low), PSR = 0.5 (low), ROE = 30 (high)
        stock_a = {
            "ticker": "A.TEST", "name": "Company A", "market": "TEST_MKT", "price": 10.0,
            "per": 5.0, "pbr": 0.5, "psr": 0.5, "roe": 30.0,
            "volume": 100000, "trading_value": 1000000.0, "sentiment_score": 0.8,
            "buy_score": None, "recommendation": None,
            "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        # Stock B: Average
        # PER = 15, PBR = 1.5, PSR = 2.0, ROE = 15
        stock_b = {
            "ticker": "B.TEST", "name": "Company B", "market": "TEST_MKT", "price": 20.0,
            "per": 15.0, "pbr": 1.5, "psr": 2.0, "roe": 15.0,
            "volume": 50000, "trading_value": 500000.0, "sentiment_score": 0.5,
            "buy_score": None, "recommendation": None,
            "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        # Stock C: Expensive and low profit (Should be Strong Sell)
        # PER = 45, PBR = 5.0, PSR = 10.0, ROE = 2.0
        stock_c = {
            "ticker": "C.TEST", "name": "Company C", "market": "TEST_MKT", "price": 50.0,
            "per": 45.0, "pbr": 5.0, "psr": 10.0, "roe": 2.0,
            "volume": 1000, "trading_value": 10000.0, "sentiment_score": 0.2,
            "buy_score": None, "recommendation": None,
            "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        db.save_stock(stock_a)
        db.save_stock(stock_b)
        db.save_stock(stock_c)
        
        # Calculate ranks
        scanner.calculate_market_ranks("TEST_MKT")
        
        a_scored = db.get_stock("A.TEST")
        b_scored = db.get_stock("B.TEST")
        c_scored = db.get_stock("C.TEST")
        
        # Verify scores
        # Stock A is best in all 4 categories, so it should get score 1.0 in all, and buy_score = 1.0 (Strong Buy)
        # Stock C is worst in all 4, so it should get score 0.0 in all, and buy_score = 0.0 (Strong Sell)
        # Stock B is middle, so it should get score 0.5 in all, and buy_score = 0.5 (Neutral)
        self.assertEqual(a_scored["buy_score"], 1.0)
        self.assertEqual(a_scored["recommendation"], "강력 매수")
        
        self.assertEqual(b_scored["buy_score"], 0.5)
        self.assertEqual(b_scored["recommendation"], "관망")
        
        self.assertEqual(c_scored["buy_score"], 0.0)
        self.assertEqual(c_scored["recommendation"], "강력 매도")
        
        print("Relative ranking calculation math test passed.")

    def test_05_etf_fetch_and_ranking(self):
        print("\n[Test 5] Testing ETF fetch and custom ranking...")
        # Fetch SPY ETF
        etf_metrics = scanner.fetch_single_stock_metrics("SPY")
        self.assertIsNotNone(etf_metrics)
        self.assertEqual(etf_metrics["market"], "ETF_US")
        self.assertGreater(etf_metrics["fifty_day_avg"], 0)
        self.assertGreater(etf_metrics["two_hundred_day_avg"], 0)
        
        # Save a few mock ETFs to test ranking
        etf_a = {
            "ticker": "ETF_A.TEST", "name": "ETF A", "market": "ETF_US", "price": 100.0,
            "volume": 100000, "trading_value": 10000000.0, "sentiment_score": 0.8,
            "fifty_day_avg": 110.0, "two_hundred_day_avg": 100.0, # Momentum = 1.10 (Best)
            "buy_score": None, "recommendation": None,
            "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        etf_b = {
            "ticker": "ETF_B.TEST", "name": "ETF B", "market": "ETF_US", "price": 100.0,
            "volume": 1000, "trading_value": 100000.0, "sentiment_score": 0.2,
            "fifty_day_avg": 90.0, "two_hundred_day_avg": 100.0, # Momentum = 0.90 (Worst)
            "buy_score": None, "recommendation": None,
            "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        db.save_stock(etf_a)
        db.save_stock(etf_b)
        
        scanner.calculate_market_ranks("ETF_US")
        
        a_scored = db.get_stock("ETF_A.TEST")
        b_scored = db.get_stock("ETF_B.TEST")
        
        # Clean up test database pollution for test ETFs
        conn = db.get_db_connection()
        conn.execute("DELETE FROM stocks WHERE ticker = 'ETF_A.TEST' OR ticker = 'ETF_B.TEST'")
        conn.commit()
        conn.close()
        
        self.assertIsNotNone(a_scored)
        self.assertIsNotNone(b_scored)
        self.assertGreater(a_scored["buy_score"], b_scored["buy_score"])
        print("ETF fetch and ranking test passed.")

if __name__ == "__main__":
    unittest.main()
