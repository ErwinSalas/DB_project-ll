import base64
__author__ = 'Erwin'
from flask import Flask,request,render_template


app = Flask(__name__)
app.secret_key = 'admin'

@app.route('/')
def indexPage():

    return render_template('index.html')



@app.route('/test/config', methods=['POST'])
def getTestConfigs():
    id = int(request.form['id'])
    anim= request.form['animal']
    med= request.form['medicamento']
    enf= request.form['enfermedad']
    dosis= request.form['dosis']
    pesoMax=request.form['pesoMax']
    pesoMin=request.form['pesoMin']

    dos = Dosis(id,anim,enf,med ,pesoMax,pesoMin,dosis)
    dosisController.update(dos)
    return mostrarDosis(0)
if __name__ == '__main__':
    app.run(debug=True)
