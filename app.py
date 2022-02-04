from flask import Flask
from flask import render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask import send_from_directory

from datetime import datetime
import os
#from sqlalchemy.orm import session

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database/task.db'
#app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Empleados(db.Model):
    __tablename__='empleados'
    id = db.Column(db.Integer,primary_key=True)
    nombre = db.Column(db.String(200))
    correo = db.Column(db.String(200))
    foto = db.Column(db.String(200))

db.create_all()

carpeta = os.path.join('uploads')
app.config['carpeta'] = carpeta

@app.route("/uploads/<nombreFoto>")
def uploads(nombreFoto):
    return send_from_directory(app.config['carpeta'],nombreFoto)

@app.route('/')
def index():
    empleado = Empleados.query.all()
    return render_template('empleados/index.html',empleado=empleado)

@app.route('/create')
def create():
    return render_template('empleados/create.html')

@app.route('/store',methods=['POST'])
def store():
    nombre = request.form['txtNombre']
    correo = request.form['txtCorreo']
    foto = request.files['txtFoto']

    now = datetime.now()
    tiempo = now.strftime('%Y%H%M%S')

    if foto.filename != '':
        nuevoNombreFoto = tiempo+foto.filename
        foto.save('uploads/'+nuevoNombreFoto)

    emp = Empleados(nombre=nombre,correo=correo,foto=nuevoNombreFoto)
    db.session.add(emp)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/destroy/<int:id>')
def destroy(id):
    task = Empleados.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/edit/<int:id>')
def edit(id):
    empleado = Empleados.query.filter_by(id=id).all()
    db.session.commit()
    return render_template('empleados/edit.html',empleado=empleado)

@app.route('/update',methods=['POST'])
def update():
    id = request.form['txtID']
    emp = Empleados.query.filter_by(id=id).first()
    emp.nombre = request.form['txtNombre']
    emp.correo = request.form['txtCorreo']
    foto = emp.foto
    emp.foto = request.files['txtFoto']

    print(foto)
    now = datetime.now()
    tiempo = now.strftime('%Y%H%M%S')

    if foto != '':
        nuevoNombreFoto = tiempo+emp.foto.filename
        print(nuevoNombreFoto)
        os.remove(os.path.join(app.config['carpeta'],foto))
        emp.foto.save('uploads/'+nuevoNombreFoto)
        emp.foto = nuevoNombreFoto
        db.session.commit()
    
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)