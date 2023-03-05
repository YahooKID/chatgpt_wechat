from flask import Flask,request
import chatgpt
import hashlib
import uuid
import random

app = Flask(__name__)

aplist = {}

@app.route('/')
def defa():
    return "hello"

@app.route('/amionline')
def amionline():
    pif = request.args
    try:
        if pif["cc"]!="随便定一个密码":
            return "0"
    except:
        return "0"
    qp=str(uuid.uuid4())
    qp1=qp
    qp = str(hashlib.md5(qp.encode(encoding='utf-8')).hexdigest())
    print(qp)
    aplist[qp] = chatgpt.chatGpt()
    return qp1


@app.route('/get_chatgpt')
def getandsend():
    pif = request.args
    if "message" not in pif:
        return "网络错误"
    if "token" not in pif:
        return "网络错误"
    try:
        return aplist[pif["token"]].add_message(pif["message"])
    except:
        return "网络错误"
    

if  __name__  ==  '__main__':
    #app.run(host='192.168.1.*',port=5001, ssl_context=('/Users/yahookid/sslkey/server.crt', '/Users/yahookid/sslkey/server.key'))
    app.run(host='192.168.1.*',port=5001)


#699dd9a119eab193e637d5ff8190480d
#5e543256c480ac577d30f76f9120eb74
