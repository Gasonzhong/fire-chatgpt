from __future__ import unicode_literals
import redis
import random
import time
import json
from datetime import datetime
from revChatGPT.V1 import Chatbot
from rediskey import QUESTIONS_KEY,QUEUE_KEY
with open('./config.json', 'r') as f:
    data = json.load(f)
email=data["email"]
password=data["password"]
chatbot=Chatbot(config={
  "email": email,
  "password": password
})

pool = redis.ConnectionPool(host='127.0.0.1',port=6379,decode_responses=True,encoding='UTF-8')   #实现一个连接池 
r = redis.StrictRedis(connection_pool=pool)
def consumer():
    while True:
        data = r.rpop(QUEUE_KEY)
        if data is None:
            time.sleep(1)
            # print('等待消息中')
            continue
        question=json.loads(data)
        print("ask:"+question['question'])
        datalist=[]
        start_time = datetime.now() #Start counting time
        try:
           for data in chatbot.ask(
           question['question'],
           conversation_id=chatbot.config.get("conversation"),
           parent_id=chatbot.config.get("parent_id"),
          ):
             datalist.append(data["message"])
        except Exception:
            print('chatgpt服务器错误')
            datalist.append('chapgpt服务发生错误')
        end_time = datetime.now() #Stop counting time
        response_time = str(round((end_time - start_time).total_seconds(), 2)) #Calculate time difference
        print("spend:"+response_time+"s")
        question['isAnswer']=1
        if len(datalist)>0:
           question['answer']=datalist[-1]
        else:
           question['answer']='访问过多'
        userId=question['userId']
        r.hset(QUESTIONS_KEY+userId,question['uuid'],json.dumps(question,ensure_ascii=False))
        print('消费:',data)   # 消费数据
        # 想chatgpt提问
        # 将结果更新并存到队列中
        time.sleep(random.randint(2,5))

if __name__ == '__main__':
    consumer()