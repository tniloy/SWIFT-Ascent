from Simulator import get_simulator_data
from flask import Flask

app = Flask(__name__)

@app.route('/simulator')
def simulator_handler():
    return get_simulator_data(2)

app.run(host='0.0.0.0', port=5000, debug=True)