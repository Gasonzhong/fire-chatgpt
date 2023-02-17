from __future__ import unicode_literals
import uuid
import redis
pool = redis.ConnectionPool(host='127.0.0.1',port=6379,decode_responses=True,encoding='UTF-8')   #实现一个连接池 
r = redis.StrictRedis(connection_pool=pool)
import json
import asyncio

#IMPORT THIRD-PARTY LIBRARIES
from flask import Flask
from flask import request
from flask_cors import CORS
from waitress import serve
from rediskey import QUESTIONS_KEY,QUEUE_KEY
from settings import API_HOST, API_PORT
#SETUP FLASK APP
app = Flask(__name__)
CORS(app)
@app.route("/test", methods=["GET", "POST"])
async def test():
    return "ping ping",200
@app.route("/uuid", methods=["GET"])
async def getUUID():
    return {'uuid':str(uuid.uuid1())},200

@app.route("/answers", methods=["GET"])
async def getAnswers():
    userId = request.args.get("userId")
    if userId is None:
        return "userId is none",200
    #从redis获取问题
    answers=r.hvals(QUESTIONS_KEY+userId)
    if answers is None:
        return {},200
    return answers,200
@app.route("/counts", methods=["GET"])
#获取问题排队数
async def counts():
    #从redis获取问题总数
    return str(r.llen(QUEUE_KEY)),200

@app.route("/chat", methods=[ "POST"])
async def chat():
    prompt = request.json.get("prompt")
  
    userId = request.json.get("userId")
    if userId is None or userId =="":
        return "userId is none",401
    question={"question":prompt,"userId":userId,"isAnswer":0,"answer":"","uuid":str(uuid.uuid1())}
    # ensure_ascii=False 解决乱码问题
    print(json.dumps(question,ensure_ascii=False))
    r.hset(QUESTIONS_KEY+userId,question['uuid'],json.dumps(question,ensure_ascii=False))
    r.lpush(QUEUE_KEY,json.dumps(question,ensure_ascii=False))
    return str(r.llen(QUEUE_KEY)), 200

def main():
    print(f"ChatGPT API is loading on {API_HOST}:{API_PORT}...")
    serve(app, host=API_HOST, port=int(API_PORT))

if __name__ == "__main__":
    asyncio.run(main())
