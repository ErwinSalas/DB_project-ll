import base64

from Objects import Configs

__author__ = 'Erwin'
from flask import Flask,request,render_template


app = Flask(__name__)
app.secret_key = 'admin'

@app.route('/')
def indexPage():

    return render_template('index.html')



@app.route('/test/config', methods=['POST'])
def getTestConfigs():
    connections = int(request.form['connections'])
    time= request.form['time']
    operation= request.form['operation']


    conf = Configs(connections,time,operation)

    return


if __name__ == '__main__':
    app.run(debug=True)
