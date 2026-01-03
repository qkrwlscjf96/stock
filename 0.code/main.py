import sys
sys.path.append(r"C:/Users/wlscj/coding/stock/0.code")

import os
from dotenv import load_dotenv
from datetime import date,timedelta
from func.func_analysis import *
from func.func_api import *

if __name__ == "__main__":

    # 슬랙 통신
    load_dotenv()  # .env 파일 로드

    slack_token = os.getenv("SLACK_TOKEN")
    channel_id = os.getenv("CHANNEL_ID")
    slack = Slack(channel_id, slack_token)
    
    # 작업 디렉토리 설정
    current_dir = os.path.dirname(os.path.abspath(__file__))
    current_dir = "C:/Users/wlscj/coding/stock"
    os.chdir(current_dir)
    
    # 분석할 주식 리스트 및 기간 설정
    my_stocks = ["GOOGL","MSFT","AAPL"]
    end_date = date.today()
    start_date = end_date + timedelta(days=-365)
    
    for my_stock in my_stocks:
        
        # 주가 데이터 불러오기
        df = stock_data_loading(my_stock, start_date, end_date)
        signal, save_path = stock_trend_analysis(current_dir,my_stock,end_date,df)
        
        # 분석
        if signal is not None:
            slack.send_image(save_path, f"{my_stock}_{end_date}_trend")
            print(f"{my_stock} {end_date} 이상 징후 포착")
            
        else:
            slack.send_text(f"{my_stock} {end_date} 이상 무")
            print(f"{my_stock} {end_date} 이상 무")






