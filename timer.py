import time
from decimal import Decimal

def timer(func):
    def wrapper(*args, **kwargs):
        start = float(time.perf_counter())
        result = func(*args, **kwargs)
        end = float(time.perf_counter())
        print("계산함수 종료, 실행시간: ", Decimal(end-start))
        return result
    return wrapper