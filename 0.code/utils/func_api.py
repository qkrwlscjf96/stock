from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import yfinance as yf

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
      
def stock_data_loading(ticker_symbol, start_date, end_date):
    ticker = yf.Ticker(ticker_symbol)
    df = ticker.history(start=start_date, end=end_date)
    return df
