from Simulator import fun
from flask import Flask

app = Flask(__name__)

@app.route('/simulator')
def simulator_handler():
    return fun(2)

app.run(host='0.0.0.0', port=5000, debug=True)