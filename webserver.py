from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
#what is printed on the webserver
def home():
    return("Hi!")

#setting up website hosting
def run():
  app.run(host='0.0.0.0',port=8080)

#start website
def keep_alive():  
    t = Thread(target=run)
    t.start()
