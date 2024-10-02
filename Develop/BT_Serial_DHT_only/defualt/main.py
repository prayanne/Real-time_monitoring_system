import serial #라이브러리인 Pyserial, import는 serial로 호출한다.

ser = serial.Serial('COM6', 9600) #시리얼 통신을 위한 준비작업 | (포트, 통신 비트레이트)
#변수 ser 이 시리얼 통신의 주가 된다.

while True: #값을 계속 받기 위해, 무한 반복문 설정

    if ser.readable(): #시리얼 통신이 이루어질 때, ser.readable()의 값이 1이 된다. 그러므로, if문이 실행됨.
        val = ser.readline() #변수 val에 수신된 값을 저장함. | ser = 시리얼 통신, .readline() = 파이썬에서 내용을 읽어올 때, 사용.
        val = val.decode('utf-8')[:len(val)-2] #val에 저장된 값을 utf-8로 디코딩함. | 아두이노와 파이썬의 문자 규격이 다르다.
        val = val.split(',') #수신받은 문자열은 콤마(,)로 구분되고 있다. .split(',')은 문자열에서 콤마를 기준으로 분리해준다.
        if int(val[0]) == 0: #val의 첫 번째 값, 오류 유무 코드가 0일 때, 정상 출력
            print(val)  # 수신된 후, 가공된 val 값을 불러옴. | 이 경우에는, [{0 or 1}, 습도값, 온도값]
        elif int(val[0]) == 1: #val의 첫 번째 값, 오류 유무 코드가 1일 때, 오류문 출력
            print("DHT22 has Error!") #오류 출력문

