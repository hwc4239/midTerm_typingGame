# 업그레이드 타이핑 게임 제작
# 사운드 적용 및 DB 연동
'''파일 목록에서 ctrl+c+v하면 두번째 파일 생성됨. 2로 바꾸고 거기에 코드 추가'''

import random
import time
import sys
######### 사운드 출력 필요 모듈
import winsound    #'''파이썬에 내장된 패키지<--소리 재생'''
import sqlite3
import datetime    #'''게임 시간 기록에 필요한 패키지'''

######### DB생성 & Autocommit
# 본인 DB 파일 경로
conn = sqlite3.connect('./records.db', isolation_level=None)

######### Cursor연결
cursor = conn.cursor()

######### 테이블 생성(Datatype : TEXT NUMERIC INTEGER REAL BLOB)
cursor.execute(
    "CREATE TABLE IF NOT EXISTS records(id INTEGER PRIMARY KEY AUTOINCREMENT,\
cor_cnt INTEGER, record text, regdate text)"
)

'''AUTOINCREMENT : 삽입할 때 insert해주지 않아도, 저절로 1씩 증가 또는 지정한 수로 증가\
    cor_cnt:정답 개수, record : 결과 '''
'''실행 했을 때 에러 발생하면 안됨. 데이터베이스 생성됐는지 확인'''

############################# 추가 코드 ############################
# GameStart 클래스 생성
class GameStart():
    
    def __init__(self, user):
        self.user = user
        
        
    # 유저 입장 알림
    def user_info(self):
        print("User : {}님이 입장하였습니다.".format(self.user))
        print()
    def choose_type(self):
        self.select=input("Choose TYPE 1.WORD 2.SENTENCE >>>")
        try:
            if int(self.select)==1:
                open_f=open('./resource/word.txt','r')
                print('Start WORD TYPING!\n')
            elif int(self.select)==2:
                open_f=open('./resource/sentence.txt','r')
                print('Start SENTENCE TYPING!\n')
                self.i=1
        except IOError:
            print("파일이 없습니다!! 게임을 진행할 수 없습니다!!")
        else:
            for c in open_f:
                words.append(c.strip())
            open_f.close()
#####################################################################

words = []                                   # 영어 단어 리스트(1000개 로드)
typing_speeds = []                            # 타이핑 속도 리스트     
avg_correctRate=[]                            # 정확도 리스트

n = 1                                        # 게임 시도 횟수
cor_cnt = 0                                  # 정답 개수
life = 5                                    #life 제한

user_name=input("Ready? Input Your name>> ")             # Enter Game Start! 
user=GameStart(user_name)                     #### GameStart의 user객체 생성
user.user_info()                              #### user 입장 알림 메서드 호출
user.choose_type()                          # 게임 선택


if words==[]:                           #파일이 없을때 프로그램 종료
    sys.exit()
    
start = time.time()                          # Start Time

while life > 0:                                # 5회 반복

    if(int(user.select) == 1):                  #단어일 경우
        i=random.randint(1,3)                   #출력할 단어 개수 1~3

    elif(int(user.select) == 2):                #문장일 경우
        i=user.i                                #출력 1개로 제한

    random.shuffle(words)                    # List shuffle!
    q = ' '.join(random.sample(words, i))    # 리스트의 단어 중 랜덤개수만큼 선택

    print("{}번 문제>>".format(n),q)         # 문제 출력
    time_start = time.time()
    x = input("타이핑 하세요>> ")            # 타이핑 입력
  
    time_end = time.time()-time_start
    speed = float(len(str(x).strip()) / time_end) * 60      #타이핑 속도
    typing_speeds.append(speed)
    if str(q).strip() == str(x).strip():     # 입력 확인(공백제거)
        ########### 정답 소리 재생
        winsound.PlaySound(                  
            './sound/good.wav',
            winsound.SND_FILENAME   #'''winsound의 PlaySound라는 클래스로 지정'''
            #'''SND_FILENAME을 직접 넣었음'''
        )
        ############
        print(">>Pass!")
        print("남은 기회:"+str(life),end=' ')     #남은 횟수 보여주기
        cor_cnt += 1                         # 정답 개수 카운트

    else:
        ########### 오답 소리 재생
        winsound.PlaySound(                  
            './sound/bad.wav',
            winsound.SND_FILENAME
        )
        ##################
        life-=1
        print(">>Wrong!")
        print("남은 기회:"+str(life),end=' ')
        

    if life==0:                             #life==0이면 게임오버
        print("!!Game Over!!")

    n += 1                                   # 도전 문제 개수 세기

    correct=0                                # 정확도 구하기
    for i,c in enumerate(q,start=0):
        try:
            if x[i]==c:
                correct +=1
        except:
            pass
    
    q_len=len(q)
    correctRate=correct/q_len * 100
    avg_correctRate.append(correctRate)
    print("타자 속도:%.2f" % speed,end=' ')     # 타자속도 
    print("정확도:{:0.2f}".format(correctRate)+'%'+'\n')
    
    
end = time.time()                            # End Time
et = end - start                             # 총 게임 시간
et = format(et, ".3f")                       # 소수 셋째 자리 출력(시간)
print()

######### 결과 기록 DB 삽입
   # '''data삽입 전에 먼저 기록테이블 구조 열어보기'''
cursor.execute(
    "INSERT INTO records('cor_cnt', 'record', 'regdate') VALUES (?, ?, ?)",
    (
        cor_cnt, et, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    )
)
'''ID는 오토 인크리먼트이므로 입력안해줘도 자동으로 db에서 연속된 숫자형으로 넣어줌'''
'''strftime('%Y-%m-%d %H:%M:%S') : 포맷 변환'''

'''게임 실행해서 db기록되는지 확인'''
######### 접속 해제
conn.close()

# 수행 시간 출력
print('***************** '+user_name+'님의 게임 정보 *****************')
print("게임 시간:", et+"s", "도전 문제 개수:",n-1,  "정답 개수: {}".format(cor_cnt))
# 평균 타자 속도 출력
print("평균 타자 속도: %.2f" % (float(sum(typing_speeds) / len(typing_speeds))),end=' ')
print("평균 정확도 : %.2f"%(float(sum(avg_correctRate) / len(avg_correctRate)))+'%')