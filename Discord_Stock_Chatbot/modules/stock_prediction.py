# # my_commands/stock_prediction.py

# import yfinance as yf
# import pandas as pd
# import pandas_ta as ta

# def calculate_indicators(stock_data):
#     macd = ta.macd(stock_data['Close'])
#     kdj = ta.stoch(stock_data['High'], stock_data['Low'], stock_data['Close'])
#     rsi = ta.rsi(stock_data['Close'])
#     atr = ta.atr(stock_data['High'], stock_data['Low'], stock_data['Close'])
#     adx = ta.adx(stock_data['High'], stock_data['Low'], stock_data['Close'])
#     short_ma = ta.sma(stock_data['Close'], length=10)
#     long_ma = ta.sma(stock_data['Close'], length=50)
#     bollinger = ta.bbands(stock_data['Close'])

#     return macd, kdj, rsi, atr, adx, short_ma, long_ma, bollinger

# def hybrid_decision(macd, kdj, rsi, atr, adx, short_ma, long_ma, stock_data):
#     votes = {"做多": 0, "做空": 0}

#     # MACD voting
#     if macd['MACDh_12_26_9'].iloc[-1] > 0:
#         votes["做多"] += 1
#     elif macd['MACDh_12_26_9'].iloc[-1] < 0:
#         votes["做空"] += 1

#     # KDJ voting
#     if kdj['STOCHk_14_3_3'].iloc[-1] < 50 and kdj['STOCHd_14_3_3'].iloc[-1] < 50:
#         votes["做多"] += 1
#     elif kdj['STOCHk_14_3_3'].iloc[-1] > 50 and kdj['STOCHd_14_3_3'].iloc[-1] > 50:
#         votes["做空"] += 1

#     # RSI voting
#     if rsi.iloc[-1] < 30:
#         votes["做多"] += 1
#     elif rsi.iloc[-1] > 70:
#         votes["做空"] += 1

#     # MA cross voting
#     if short_ma.iloc[-1] > long_ma.iloc[-1]:
#         votes["做多"] += 1
#     elif short_ma.iloc[-1] < long_ma.iloc[-1]:
#         votes["做空"] += 1

#     # ATR check
#     if atr.iloc[-1] > atr.iloc[-2]:
#         votes["做多"] += 1

#     # ADX check
#     if adx['ADX_14'].iloc[-1] > 25:
#         votes["做多"] += 1
#     elif adx['ADX_14'].iloc[-1] < 25:
#         votes["做空"] += 1

#     # Moving average retracement check
#     current_price = stock_data['Close'].iloc[-1]
#     if current_price >= short_ma.iloc[-1] * 0.95:
#         votes["做多"] += 1

#     if votes["做多"] > votes["做空"] + 1:
#         return "做多"
#     elif votes["做空"] > votes["做多"] + 1:
#         return "做空"
#     else:
#         return "觀望"

# def predict_stock(stock_id):
#     try:
#         stock_data = yf.download(f"{stock_id}.TW", period="1y", interval="1d")

#         if stock_data.empty:
#             stock_data = yf.download(f"{stock_id}.TWO", period="1y", interval="1d")

#         if stock_data.empty:
#             return "無法獲取股票數據"

#         macd, kdj, rsi, atr, adx, short_ma, long_ma, bollinger = calculate_indicators(stock_data)
#         decision = hybrid_decision(macd, kdj, rsi, atr, adx, short_ma, long_ma, stock_data)

#         return f"對於股票 {stock_id} 的建議是：{decision}"

#     except Exception as e:
#         return f"分析過程中發生錯誤: {str(e)}"
import yfinance as yf
import pandas as pd
import pandas_ta as ta

def calculate_indicators(stock_data):
    macd = ta.macd(stock_data['Close'])
    kdj = ta.stoch(stock_data['High'], stock_data['Low'], stock_data['Close'])
    rsi = ta.rsi(stock_data['Close'])
    atr = ta.atr(stock_data['High'], stock_data['Low'], stock_data['Close'])
    adx = ta.adx(stock_data['High'], stock_data['Low'], stock_data['Close'])
    short_ma = ta.sma(stock_data['Close'], length=10)
    long_ma = ta.sma(stock_data['Close'], length=50)
    bollinger = ta.bbands(stock_data['Close'])

    return macd, kdj, rsi, atr, adx, short_ma, long_ma, bollinger

def hybrid_decision(macd, kdj, rsi, atr, adx, short_ma, long_ma, stock_data):
    votes = {"做多": 0, "做空": 0}
    log_list = []

    # MACD voting
    if macd['MACDh_12_26_9'].iloc[-1] > 0:
        votes["做多"] += 1
        log_list.append("MACD 投票：做多")
    elif macd['MACDh_12_26_9'].iloc[-1] < 0:
        votes["做空"] += 1
        log_list.append("MACD 投票：做空")

    # KDJ voting
    if kdj['STOCHk_14_3_3'].iloc[-1] < 50 and kdj['STOCHd_14_3_3'].iloc[-1] < 50:
        votes["做多"] += 1
        log_list.append("KDJ 投票：做多")
    elif kdj['STOCHk_14_3_3'].iloc[-1] > 50 and kdj['STOCHd_14_3_3'].iloc[-1] > 50:
        votes["做空"] += 1
        log_list.append("KDJ 投票：做空")

    # RSI voting
    if rsi.iloc[-1] < 30:
        votes["做多"] += 1
        log_list.append("RSI 投票：做多")
    elif rsi.iloc[-1] > 70:
        votes["做空"] += 1
        log_list.append("RSI 投票：做空")

    # MA cross voting
    if short_ma.iloc[-1] > long_ma.iloc[-1]:
        votes["做多"] += 1
        log_list.append("MA 交叉投票：做多")
    elif short_ma.iloc[-1] < long_ma.iloc[-1]:
        votes["做空"] += 1
        log_list.append("MA 交叉投票：做空")

    # ATR check
    if atr.iloc[-1] > atr.iloc[-2]:
        votes["做多"] += 1
        log_list.append("ATR 增加，市場波動性強，做多信號")

    # ADX check
    if adx['ADX_14'].iloc[-1] > 25:
        votes["做多"] += 1
        log_list.append("ADX 趨勢強，做多信號")
    elif adx['ADX_14'].iloc[-1] < 25:
        votes["做空"] += 1
        log_list.append("ADX 趨勢弱，做空信號")

    # Moving average retracement check
    current_price = stock_data['Close'].iloc[-1]
    if current_price >= short_ma.iloc[-1] * 0.95:
        votes["做多"] += 1
        log_list.append("回檔不破均線，強力做多信號")

    log_list.append(f"投票結果：做多 {votes['做多']} 票, 做空 {votes['做空']} 票")

    if votes["做多"] > votes["做空"] + 1:
        decision = "做多"
    elif votes["做空"] > votes["做多"] + 1:
        decision = "做空"
    else:
        decision = "觀望"

    log_list.append(f"最終決策：{decision}")

    return decision, log_list

def predict_stock(stock_id):
    try:
        stock_data = yf.download(f"{stock_id}.TW", period="1y", interval="1d")

        if stock_data.empty:
            stock_data = yf.download(f"{stock_id}.TWO", period="1y", interval="1d")

        if stock_data.empty:
            return "無法獲取股票數據"

        macd, kdj, rsi, atr, adx, short_ma, long_ma, bollinger = calculate_indicators(stock_data)
        decision, log_list = hybrid_decision(macd, kdj, rsi, atr, adx, short_ma, long_ma, stock_data)

        result = f"對於股票 {stock_id} 的分析：\n\n"
        result += "技術指標數值：\n"
        result += f"MACD: {macd.iloc[-1]['MACD_12_26_9']:.2f}\n"
        result += f"KDJ: K={kdj.iloc[-1]['STOCHk_14_3_3']:.2f}, D={kdj.iloc[-1]['STOCHd_14_3_3']:.2f}\n"
        result += f"RSI: {rsi.iloc[-1]:.2f}\n"
        result += f"ATR: {atr.iloc[-1]:.2f}\n"
        result += f"ADX: {adx.iloc[-1]['ADX_14']:.2f}\n"
        result += f"短期MA: {short_ma.iloc[-1]:.2f}\n"
        result += f"長期MA: {long_ma.iloc[-1]:.2f}\n\n"

        result += "決策過程：\n"
        result += "\n".join(log_list)

        return result

    except Exception as e:
        return f"分析過程中發生錯誤: {str(e)}"