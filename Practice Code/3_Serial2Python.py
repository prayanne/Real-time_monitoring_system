# 목적: 파이썬 to 아두이노의 시리얼 통신을 이해하고 있는지 확인하는 코드
# 수행할 항목 :
# 1. - 처리되어 있는 줄의 코드를 작성
# 2. 모든 코드의 주석을 추가

# - 처리되어 있는 항목은 2개 입니다.

# 전제 조건: 
# 컴퓨터 to 아두이노, 근거리 무선 연결
# 아두이노는 블루투스로 연결되었고, 문자열을 지속적으로 출력한다.
# 아두이노의 블루투스 통신 포트는 COM8이다.

import serial # 파이썬에서 시리얼 통신을 하기 위해, 호출한 라이브러리

serial_sensor = -.Serial( - , 9600) # 

def sensor_input():
    if serial_sensor.readable():  # 시리얼 통신이 이루어질 때, ser.readable()의 값이 1이 된다. 그러므로, if문이 실행됨.
        val = serial_sensor.readline()  #
        val = val.decode('utf-8')[:len(val) - 2] #
        print(val) # 사용자에게 어떤 값을 표시하는지 간단히 설명하시오.

if __name__ == '__main__':
    while 1:
         sensor_input()