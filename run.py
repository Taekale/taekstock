# -*- coding: utf-8 -*-
import os
import sys
import threading
import time
import webbrowser

# Ensure current working directory is added to sys.path so backend imports work
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    import uvicorn
    from backend import db, scanner
except ImportError as e:
    print(f"Error: Missing dependencies. {e}")
    print("Please install requirements by running: py -m pip install -r requirements.txt")
    sys.exit(1)

def initialize_app():
    print("=== 스마트 주식 추천 시스템 초기 설정 ===")
    
    # Self-healing check: reset DB if KOSPI stocks are mapped to .KQ due to encoding error
    db_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "stocks.db")
    if os.path.exists(db_file):
        try:
            import sqlite3
            conn = sqlite3.connect(db_file)
            row = conn.execute("SELECT yf_ticker FROM krx_mapping WHERE ticker = '005380'").fetchone()
            conn.close()
            if row and row[0].endswith(".KQ"):
                print("이전 실행 시의 인코딩 오류로 인해 손상된 데이터베이스 매핑이 감지되었습니다. DB를 초기화합니다...")
                try:
                    os.remove(db_file)
                    print("기존 데이터베이스가 성공적으로 삭제되었습니다.")
                except Exception as e:
                    print(f"데이터베이스 파일 삭제 오류: {e}")
        except Exception as e:
            pass
            
    # 1. Initialize SQLite Database
    db.init_db()
    
    # 2. Check if KRX Mapping table is empty
    conn = db.get_db_connection()
    count = conn.execute("SELECT COUNT(*) FROM krx_mapping").fetchone()[0]
    conn.close()
    
    if count == 0:
        print("KRX 종목 매핑 테이블이 비어 있습니다. 초기 구축을 시작합니다...")
        success = scanner.sync_krx_mappings_from_kind()
        if success:
            print("성공적으로 KRX 종목 매핑 데이터를 가져왔습니다.")
        else:
            print("경고: KRX 종목 매핑 구축에 실패했습니다. 오프라인 또는 서버 상태를 확인해 주세요.")
    else:
        print(f"KRX 종목 매핑 테이블 로드 완료 (등록된 종목 수: {count}개)")

def open_browser():
    time.sleep(1.5)
    url = "http://127.0.0.1:8000"
    print(f"웹 브라우저를 열어 앱에 접속합니다: {url}")
    webbrowser.open(url)

if __name__ == "__main__":
    # Initialize DB & mapping cache
    initialize_app()
    
    # Launch browser in a background daemon thread
    threading.Thread(target=open_browser, daemon=True).start()
    
    # Run Uvicorn FastAPI Server
    print("\nLocal Web Server를 구동합니다. 콘솔창을 종료하지 마세요...")
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=False)
