


import logging
import time
import os
from colorama import Fore, init
from flask import Flask
from threading import Thread
from waitress import serve
#routes
from routes.start_flood import Flood
from routes.status import Status


PRODUCTION = True

app = Flask(__name__, None, "static")

logging.basicConfig(filename='data/record.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

app.secret_key = "pokeloanjg"

app.register_blueprint(Flood)
app.register_blueprint(Status)

@app.errorhandler(404)
def error_404(e):
    return "Error 404.... oh noo"

@app.errorhandler(Exception)          
def basic_error(e):
    app.logger.warning(f'Caught exception: {str(e)}')
    return "Unknown error logged. Contact staff."+str(e)

def run_cleanup_task():
    while True:
        os.system('rm -f proxy.txt && python3 main.py')
        time.sleep(120)  # 600 seconds = 10 minutes
        

if __name__ == "__main__":

    init()

    print(Fore.MAGENTA, """

   ____                                   _    ____ ___ 
  / ___|___  ___ _ __ ___   ___  ___     / \  |  _ \_ _|
 | |   / _ \/ __| '_ ` _ \ / _ \/ __|   / _ \ | |_) | | 
 | |__| (_) \__ \ | | | | | (_) \__ \  / ___ \|  __/| | 
  \____\___/|___/_| |_| |_|\___/|___/ /_/   \_\_|  |___|

  [Made by robert streahorn aka robert]
            [t.me/ambuscade]
                                                        
    """, Fore.RESET)

    if PRODUCTION:
        print(Fore.GREEN, "API server started.", Fore.RESET)
        serve(app, host="0.0.0.0", port=80) # change port here if you want
    else:
        Thread(target=app.run, kwargs={"threaded":True}).start()
        Thread(target=run_cleanup_task).start()
        
