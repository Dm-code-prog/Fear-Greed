import flask
from twitter import *
import time
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
import re, pickle, functions


def fear():
    fear_ = twitter()
    with open('fear.pkl', 'wb') as f:
        pickle.dump(fear_, f)


bg = BackgroundScheduler(daemon=True)
bg.add_job(fear, 'interval', hours=12)
bg.start()


app = flask.Flask(__name__)


@app.route('/')
def Home():
    fear()
    with open('fear.pkl', 'rb') as f:
        fear_ = pickle.load(f)
        print(fear_)
    vol = functions.volatility(["BTC-USD", "ETH-USD", "BNB-USD", "XRP-USD", "ADA-USD",
                                "LUNA-USD", "SOL-USD", "AVAX-USD", "DOT-USD", "DOGE-USD"])
    data = int((fear_ + vol)/2) 
    return flask.render_template('index.html', data=data)



atexit.register(lambda: cron.shutdown(wait=False))

if __name__ == '__main__':
    app.run(debug=True)
