import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from datetime import date,timedelta
from utils.func_analysis import *
from utils.func_api import *
from utils.func_common import *

if __name__ == "__main__":
    
    # 현재 파일 기준 디렉토리
    BASE_DIR = Path(__file__).resolve().parent
    #BASE_DIR = Path.cwd() / "0.code"
        
    # 중복 실행 방지
    joblog_path = (BASE_DIR / ".." / "99.logs"/ "job.log").resolve()
    if already_ran_today_twice(joblog_path):
        print("Already ran today. Exiting.")
        sys.exit(0)

    # 슬랙 통신
    load_dotenv()  # .env 파일 로드
    slack_token = os.getenv("SLACK_TOKEN")
    channel_id = os.getenv("CHANNEL_ID")
    slack = Slack(channel_id, slack_token)
    
    # 분석할 주식 리스트 및 기간 설정
    my_stocks = ["GOOGL","MSFT","AAPL"]
    end_date = date.today()
    start_date = end_date + timedelta(days=-365)
    
    for my_stock in my_stocks:
        
        # 주가 데이터 불러오기
        df = stock_data_loading(my_stock, start_date, end_date)
        signal, save_path = stock_trend_analysis(BASE_DIR,my_stock,end_date,df)
        
        # 분석
        if signal is not None:
            slack.send_image(save_path, f"{my_stock}_{end_date}_trend")
            print(f"{my_stock} {end_date} 이상 징후 포착")
            
        else:
            slack.send_text(f"{my_stock} {end_date} 이상 무")
            print(f"{my_stock} {end_date} 이상 무")






