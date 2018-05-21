import base64


__author__ = 'Erwin'
from flask import Flask,request,render_template
import DBController, Objects

app = Flask(__name__)
app.secret_key = 'admin'

@app.route('/')
def indexPage():

    return render_template('index.html')


@app.route('/pruebas')
def test():
    conection = DBController.DBController('centralDB', 'postgres', 'postgres', 'localhost')
    conection.servisiosMasCaros()





@app.route('/test/configs', methods=['POST'])
def getTestConfigs():
    connections = int(request.form['connections'])
    time = int(request.form['time'])
    operations = int(request.form['operation_number'])
    conection = DBController.DBController('centralDB', 'postgres', 'postgres', 'localhost')
    ob = Objects.Configs(connections,time ,operations)
    conection.connection(ob)
    return render_template('test_result.html', results=conection.connection(ob))


if __name__ == '__main__':
    app.run(debug=True)
