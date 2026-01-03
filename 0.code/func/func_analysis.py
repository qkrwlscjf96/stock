from pathlib import Path
import matplotlib.pyplot as plt

# 주가 추세 분석 함수
def stock_trend_analysis(current_dir,my_stock,end_date,df): 
    save_path = Path(current_dir) / "3.result" / f"{my_stock}_{end_date}_trend.png"
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
        return None, None

    # 차트 생성
    plt.figure(figsize=(10, 5))
    plt.plot(df.index, df["Close"], label="Close")
    plt.plot(df.index, df["MA20"], label="MA20")
    plt.plot(df.index, df["MA60"], label="MA60")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()

    return signals,save_path