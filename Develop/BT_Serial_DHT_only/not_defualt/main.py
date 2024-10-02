import serial #라이브러리인 Pyserial, import는 serial로 호출한다.

ser = serial.Serial('COM6', 9600, timeout=1) #시리얼 통신을 위한 준비작업 | (포트, 통신 비트레이트, 지연시간)
#지연시간이 없을 때, 오류 발생함. 삽입 필. | 변수 ser 이 시리얼 통신의 주가 된다.

while True: #값을 계속 받기 위해, 무한 반복문 설정

    if ser.readable(): #시리얼 통신이 이루어질 때, ser.readable()의 값이 1이 된다. 그러므로, if문이 실행됨.
        val = ser.readline() #변수 val에 수신된 값을 저장함. | ser = 시리얼 통신, .readline() = 파이썬에서 내용을 읽어올 때, 사용.
        val = val.decode('utf-8') #val에 저장된 값을 utf-8로 디코딩함. | 아두이노와 파이썬의 문자 규격이 다르다.
        print(val) #수신되고, 가공된 val 값을 불러옴. | 이 경우에는, Humidity: {습도값} %	Temperture: {온도값} *C 으로 출력됨.
