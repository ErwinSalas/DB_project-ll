import base64


__author__ = 'Erwin'
from flask import Flask,request,render_template
import DBController, Objects

app = Flask(__name__)
app.secret_key = 'admin'

@app.route('/')
def indexPage():

    return render_template('index.html')



@app.route('/test/configs', methods=['POST'])
def getTestConfigs():
    connections = int(request.form['connections'])
    time= request.form['time']
    conf = Objects.Configs(connections,time,operation, operationNumber)
    conection = DBController.DBController('centraldb', 'Postgres', 'pass', 'localhost')
    conection.insertUsers()
    return "listo"


if __name__ == '__main__':
    app.run(debug=True)
