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
    conection = DBController.DBController('nodeIII', 'postgres', 'password', 'localhost')
    ob = Objects.Configs(6, 1)
    conection.connection(ob)
    return "listo"


if __name__ == '__main__':
    app.run(debug=True)
