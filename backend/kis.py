# -*- coding: utf-8 -*-
import os
import requests
import json
import time

class KISClient:
    """
    한국투자증권 Open API (KIS Developer) 연동 클라이언트.
    AppKey, AppSecret이 설정되지 않은 경우 안전하게 Fallback 모드로 작동합니다.
    """
    def __init__(self):
        # 환경변수 또는 로컬 설정 파일에서 로드
        self.app_key = os.environ.get("KIS_APPKEY") or ""
        self.app_secret = os.environ.get("KIS_APPSECRET") or ""
        
        # 실전투자 도메인 사용 (기본)
        self.base_url = "https://openapi.koreainvestment.com:9443"
        self.access_token = ""
        self.token_expired_at = 0
        
        # 키가 설정되어 있는 경우 자동으로 토큰을 발급받습니다.
        if self.app_key and self.app_secret:
            self.fetch_access_token()
            
    def is_available(self):
        """
        KIS API가 유효하게 작동하는지 여부를 판단합니다.
        """
        if not self.app_key or not self.app_secret:
            return False
        # 토큰 만료 여부 체크
        if not self.access_token or time.time() >= self.token_expired_at:
            return self.fetch_access_token()
        return True

    def fetch_access_token(self):
        """
        OAuth2 Access Token 발급 API 호출
        """
        try:
            url = f"{self.base_url}/oauth2/tokenP"
            headers = {"content-type": "application/json"}
            body = {
                "grant_type": "client_credentials",
                "appkey": self.app_key,
                "appsecret": self.app_secret
            }
            res = requests.post(url, headers=headers, data=json.dumps(body), timeout=7)
            if res.status_code == 200:
                data = res.json()
                self.access_token = data.get("access_token")
                # 토큰 유효 시간 저장 (초 단위, 안전하게 2시간 만료 기준에서 30분 마진을 둡니다)
                expires_in = int(data.get("expires_in", 7200))
                self.token_expired_at = time.time() + expires_in - 1800
                print("[KIS API] Access Token 발급에 성공했습니다.")
                return True
            else:
                print(f"[KIS API] 토큰 발급 실패 (HTTP {res.status_code}): {res.text}")
                return False
        except Exception as e:
            print(f"[KIS API] 토큰 발급 예외 발생: {e}")
            return False

    def fetch_domestic_stock_metrics(self, ticker_symbol):
        """
        한국투자증권 API를 사용하여 국내 주식/ETF 실시간 시세 및 
        체결강도, 호가 잔량 비율 등의 정밀 수급 지표를 조회합니다.
        ticker_symbol: 6자리 숫자 + 접미사 (예: "005930.KS" -> "005930")
        """
        if not self.is_available():
            return None
            
        try:
            # yfinance 티커 형식("005930.KS")에서 6자리 종목 코드만 추출
            code = ticker_symbol.split(".")[0]
            
            # 1. 주식/ETF 현재가 및 수급 지표 조회 API
            url = f"{self.base_url}/uapi/domestic-stock/v1/quotations/inquire-price"
            headers = {
                "content-type": "application/json",
                "authorization": f"Bearer {self.access_token}",
                "appkey": self.app_key,
                "appsecret": self.app_secret,
                "tr_id": "FHKST01010100" # 주식현재가 상세 조회 TR ID
            }
            params = {
                "fid_cond_mrkt_div_code": "J", # 주식, ETF 모두 J
                "fid_input_iscd": code
            }
            
            res = requests.get(url, headers=headers, params=params, timeout=5)
            if res.status_code == 200:
                out = res.json().get("output", {})
                if not out:
                    return None
                    
                # KIS API에서 수급 및 펀더멘탈 정보를 디코딩
                price = float(out.get("stck_prpr", 0))       # 현재가
                volume = int(out.get("acml_vol", 0))         # 당일 누적 거래량
                trading_value = float(out.get("acml_tr_pbmn", 0)) # 누적 거래대금 (원)
                
                # 예측 정확도를 높이기 위한 정밀 수급 팩터 추출
                volume_power = float(out.get("wghn_avrg_prpr", 100)) # 체결강도 (100% 이상일 때 매수세가 더 강함)
                per = out.get("per")
                pbr = out.get("pbr")
                
                per_val = float(per) if per and float(per) > 0 else None
                pbr_val = float(pbr) if pbr and float(pbr) > 0 else None
                
                # 호가 비대칭도 (매수잔량 / 매도잔량 비율) - 단기 상승 수급 예측에 매우 중요
                total_ask_rem = float(out.get("total_ask_rem", 1)) # 총 매도잔량
                total_bid_rem = float(out.get("total_bid_rem", 1)) # 총 매수잔량
                bid_ask_ratio = total_bid_rem / total_ask_rem if total_ask_rem > 0 else 1.0
                
                return {
                    "price": price,
                    "volume": volume,
                    "trading_value": trading_value,
                    "volume_power": volume_power, # 체결강도 추가 피처
                    "bid_ask_ratio": bid_ask_ratio, # 호가 비율 추가 피처
                    "per": per_val,
                    "pbr": pbr_val,
                    "source": "KIS"
                }
            else:
                print(f"[KIS API] 시세 조회 실패 ({ticker_symbol}): {res.text}")
                return None
        except Exception as e:
            print(f"[KIS API] 시세 조회 예외 발생 ({ticker_symbol}): {e}")
            return None

# 전역 클라이언트 인스턴스 싱글톤
kis_client = KISClient()
