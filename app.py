import http
import json
from math import prod
from pickle import GET
from urllib3 import request
from flask import Flask, render_template,request
import requests
import time
import threading

app = Flask(__name__)


@app.route('/',methods=["GET", "POST"])
def listern():
    print('Background Process Started ')
    backgroundThread = threading.Thread(target = processWebhookPayload, args = (request,))
    backgroundThread.start()
    print("Background Process Running")
    print("Success to BC")
    return 'Yeah, I got it',200

def processWebhookPayload(request):
    time.sleep(0.1)
    print("Funnction is working  \n ")
    
    
if __name__ == '__main__':
    app.run()










