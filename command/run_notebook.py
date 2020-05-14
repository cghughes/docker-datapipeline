"""Python script to run Juptyer Notebooks."""
import _thread as thread
import datetime
import json
from pprint import pprint
from shutil import Error
import sys
import time
import uuid

import requests
from websocket import ABNF, WebSocket, WebSocketApp, create_connection

from notebook import Notebook

#base_url = 'http://localhost:8888'
#notebook_password = '3point142'
notebook_path = '/work/BatchAPIExample.ipynb'

nb = Notebook(notebook_path)
nb.start_session()

if (nb.login()):
    nb.start_kernel()
    nb.build_notebook()

messages = []
session = uuid.uuid1().hex

def send_execute_request(code):
    msg_type = 'execute_request'
    content = { 
        'code' : code, 
        'silent' : False 
        }
    hdr = { 
        'msg_id' : uuid.uuid1().hex, 
        'username': 'test', 
        'session': nb.notebook_session_id, 
        'data': datetime.datetime.now().isoformat(),
        'msg_type': msg_type,
        'version' : '5.0' 
        }
    msg = { 
        'header': hdr, 
        'parent_header': hdr, 
        'metadata': {},
        'content': content 
        }
    return msg

def on_message(ws, message):
    print("Received << ")
    messages.append(message)

def on_error(ws, error):
    print("Error :: " + error)

def on_close(ws):
    print("### closed ###")     

def on_open(ws):
    def run(*args):
        for c in nb.code:
            message = json.dumps(send_execute_request(c))
            messages.append(message)
            ws.send(message)
            time.sleep(1)
        time.sleep(30)
        ws.close()
        print("thread terminating...")
    thread.start_new_thread(run, ())             

# Execution request/reply is done on websockets channels
cookies = nb.session.cookies.get_dict()
#ws = create_connection("ws://localhost:8888/api/kernels/"+kernel['id']+"/channels",
     #header=headers, cookie = "; ".join(["%s=%s" %(i, j) for i, j in cookies.items()]), class_=MyWebSocket)

ws = WebSocketApp(nb.ws_url + "/api/kernels/"+nb.active_kernel_id+"/channels",
                            header=nb.headers, cookie = "; ".join(["%s=%s" %(i, j) for i, j in cookies.items()]),
                            on_message = on_message,
                            on_error = on_error,
                            on_close = on_close)

ws.on_open = on_open
ws.run_forever()  

#for c in code:
#    ws.send(json.dumps(send_execute_request(c)))

count = 0
for m in messages:
    rsp = json.loads(m)
    msg_type = rsp["header"]["msg_type"]

    if msg_type == '_execute_request':
        print("--------------------------------------------------------------------------------")
        try:
            ecount = None
            try:
                ecount = str(rsp["content"]["execution_count"])                
            except:
                ecount = "#"
            print(msg_type + "(" + ecount + "): \n" + rsp["content"]["code"])
        except:
            error = sys.exc_info()[0]
            print("[EXECUTE_REQUEST]->Unexpected error:", error)
        print("--------------------------------------------------------------------------------")
    elif msg_type == 'execute_request':
        #print(msg_type + ">>")
        count = count + 1
    elif msg_type == 'execute_input':
        
        try: 
            print(msg_type + "(" + str(rsp["content"]["execution_count"]) + ") for " + rsp["header"]["msg_id"])
            print("-------")
            print(rsp["content"]["code"])
        except:
            error = sys.exc_info()[0]
            print("[EXECUTE_INPUT]->Unexpected error:", error)
        print("--------------------------------------------------------------------------------")
        
    elif msg_type == 'execute_result':
        
        try:
            print(msg_type + "(" + str(rsp["content"]["execution_count"]) + ") for " + rsp["header"]["msg_id"])
            print("-------")
            for k,v in rsp["content"]["data"].items():
                print(str(k))
                print(str(v))
        except:
            error = sys.exc_info()[0]
            print("[EXECUTE_RESULT]->Unexpected error:", error)
        print("--------------------------------------------------------------------------------")
    elif msg_type == 'execute_reply':        
        try:            
            if (rsp["content"]["status"] == "error"):
                print(msg_type + "(" + str(rsp["content"]["execution_count"]) + ") for " + rsp["header"]["msg_id"] + " : " + rsp["content"]["ename"])
                print("-------")
                print(rsp["content"]["evalue"])
            else:
                print(msg_type + "(" + str(rsp["content"]["execution_count"]) + ") for " + rsp["header"]["msg_id"] + " : " + rsp["content"]["status"])
        except:
            error = sys.exc_info()[0]
            print("[EXECUTE_REPLY]->Unexpected error:", error)
        print("--------------------------------------------------------------------------------")            
    elif msg_type == 'status':
        #print(msg_type + "<<")
        count = count + 1
    elif msg_type == 'stream':
        print(msg_type + "<<")        
        stdout = None
        try:
            stdout = rsp["content"]["text"]
        except:
            stdout = ""
        print(msg_type + ">> " + rsp["header"]["msg_id"] + ":")
        print("-------")
        print(stdout)
        print("--------------------------------------------------------------------------------")
    elif msg_type == 'error':
        #print(msg_type + "<<")        
        count = count + 1
    elif msg_type == '_error':
        try:
            print(msg_type + ">> " + rsp["content"]["ename"] + "::\n" +  rsp["content"]["evalue"])
        except:
            error = sys.exc_info()[0]
            print("[ERRROR]->Unexpected error:", error)                
    else:
        print("*-------------------------------------------------------------------------------")
        try:
            print(msg_type + ">> \n" + str(rsp))
        except:
            error = sys.exc_info()[0]
            print("Unexpected error:", error)
        print("*-------------------------------------------------------------------------------")