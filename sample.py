# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
import time
import threading
from flask import Flask, request
# Flask constructor takes the name of
# current module (__name__) as argument.
app = Flask(__name__)
# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.
# @app.route('/')
# # ‘/’ URL is bound with hello_world() function.
# def hello_world():
#     return 'Hello World'



# The route() to experiment the threading in python
@app.route('/listen-webhook')
def listern():
    # first strat the threading to run our main process in the background thread
    print('background process about to start')
    backgroundThread = threading.Thread(target = processWebhookPayload, args = (request,))
    backgroundThread.start()
    print('background process is already started')
    
    # processWebhookPayload(request)
    # then inform the bigcommerce that we got the the webhook successfuly
    print('we are about to infrom BC that we got webhook')
    print('The main process is just completed')
    return 'Yeah, I got it',200


def processWebhookPayload(request):
    # do over stuff
    print('processWebhookPayloadn this is working soon')
    print('processWebhookPayloadn this is working soon')
    time.sleep(30)
    print('processWebhookPayloadn this is working after 30s')
    time.sleep(30)
    print('processWebhookPayloadn this is working after another 30s')
    print('processWebhookPayloadn this is working soon')
    time.sleep(10)
    print('processWebhookPayloadn this is working after 10s')
    time.sleep(20)
    print('processWebhookPayloadn this is working after 20s')
    time.sleep(5)
    print('processWebhookPayloadn this is working after 5s')
    time.sleep(60)
    print('processWebhookPayloadn this is working after 1 minute')
    print('processWebhookPayloadn we will stop this process after waiting for another 30 second')
    time.sleep(30)
    print('Oh! we just stoped now')





# main driver function
if __name__ == '__main__':
    # run() method of Flask class runs the application
    # on the local development server.
    app.run()










