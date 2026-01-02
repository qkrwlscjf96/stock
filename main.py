import yfinance as yf
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import date,timedelta
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# 주가 추세 분석 함수
def stock_trend_analysis(df):
    df = df.copy()

    df["MA20"] = df["Close"].rolling(20).mean()
    df["MA60"] = df["Close"].rolling(60).mean()

    # 최근 2일 데이터
    last = df.iloc[-1]
    prev = df.iloc[-2]

    signals = []

    # ① 데드크로스
    if prev["MA20"] > prev["MA60"] and last["MA20"] < last["MA60"]:
        signals.append("⚠️ 데드크로스 발생")

    # ② 추세 이탈
    if last["Close"] < last["MA60"]:
        signals.append("⚠️ 종가가 MA60 아래로 하락")

    # ③ 급락
    drop_rate = (last["Close"] - prev["Close"]) / prev["Close"] * 100
    if drop_rate <= -3:
        signals.append(f"🚨 급락 경고 ({drop_rate:.2f}%)")

    # 위험 없으면 종료
    if not signals:
        return None

    # 차트 생성
    plt.figure(figsize=(10, 5))
    plt.plot(df.index, df["Close"], label="Close")
    plt.plot(df.index, df["MA20"], label="MA20")
    plt.plot(df.index, df["MA60"], label="MA60")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("trend.png")
    plt.close()

    return signals

# 슬랙으로 정보 메신저 보내기

class Slack:
    """
    Slack API를 사용하여 메시지 및 파일을 Slack 채널에 전송하는 클래스.
    :param channel: 메시지를 보낼 Slack 채널 ID, !채널 이름은 이미지 전송 안됨!
    :param token: Slack OAuth 토큰
    """

    def __init__(self, channel, token):
        self._channel = channel
        self._token = token
        self._client = WebClient(token=token)

    def send_text(self, text):
        """
        주어진 텍스트 메시지를 Slack 채널에 전송
        :param text: 전송할 텍스트 메시지
        :return: Slack API의 응답 JSON
        """
        try:
            self._client.chat_postMessage(channel=self._channel, text=text)
        except SlackApiError as e:
            print(e)

    def send_image(self, image, text=None):
        """
        주어진 이미지를 Slack 채널에 전송
        :param image: 이미지 파일의 경로
        :param text: (선택적) 이미지와 함께 전송할 텍스트
        :return: Slack API의 응답 JSON
        """
        try:
            response = self._client.files_upload_v2(
                file=image,
                channels=[self._channel],
                initial_comment=text,
            )
            response.get("file")
        except SlackApiError as e:
            print(e)
            
        
if __name__ == "__main__":

    # 슬랙 통신
    slack_token = "#" 
    channel_id = "#"
    slack = Slack(channel_id, slack_token)
    
    # 주가 데이터 불러오기
    my_stock = "GOOGL"
    end_date = date.today() + timedelta(days=1)
    ticker = yf.Ticker(my_stock)
    df = ticker.history(start="2024-01-01", end=end_date)
    
    # 분석
    signal = stock_trend_analysis(df)
    if signal is not None:
        slack.send_image("trend.png", f"{my_stock} 주식 분석 결과")
        
    else:
        slack.send_text(f"{my_stock} 이상 무")



