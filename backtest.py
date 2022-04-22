import pyupbit
import numpy as np

#OHLCV(Open, high, low, close, volume)로 당일 시가, 고가, 저가, 종가, 거래량
df = pyupbit.get_ohlcv("KRW-ETH", count=10)

# 변동폭*k계산, (고가-저가)*k값
df['range'] = (df['high'] - df['low']) * 0.5

# target(매수가), range 컬럼을 한칸식 밑으로 내림(.shift(1))
df['target'] = df['open'] + df['range'].shift(1)

##np.where(조건문, 참일때 값, 거짓일때 값)
df['ror'] = np.where(df['high'] > df['target'],
                     df['close'] / df['target'],
                     1)

##누적 곱 계산(cumprod) -> 누적수익률
df['hpr'] = df['ror'].cumprod()

# drow down 계산(누적 최대 값과 현재 hpr차리 / 누적 최대값 * 100)
df['dd'] = (df['hpr'].cummax() - df['hpr']) / df['hpr'].cummax() * 100

#mdd계산(max값)
print("MDD(%): ", df['dd'].max())

# dd.xls 엑셀파일
df.to_excel("AA.xlsx")