import os
from flask import Flask, render_template, redirect, url_for, request, flash, session, Response
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import csv

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_DIR = os.path.join(BASE_DIR, 'db')
if not os.path.exists(DB_DIR):
    os.makedirs(DB_DIR)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supercreto'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(DB_DIR, 'acceso.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# MODELOS
class Estudiante(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    dni = db.Column(db.String(20), unique=True, nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    curso = db.Column(db.String(50), nullable=False)
    salon = db.Column(db.String(20), nullable=False)
    pin = db.Column(db.String(6), unique=True, nullable=False)
    materias = db.relationship('Materia', backref='estudiante', lazy=True)

class Materia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    hora_inicio = db.Column(db.String(5), nullable=False)
    hora_fin = db.Column(db.String(5), nullable=False)
    estudiante_id = db.Column(db.Integer, db.ForeignKey('estudiante.id'), nullable=False)

class Visitante(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    motivo = db.Column(db.String(200), nullable=False)
    hora_entrada = db.Column(db.String(30), nullable=False)
    hora_salida = db.Column(db.String(30))
    tiempo_limite = db.Column(db.Integer, nullable=False)  
    unidad = db.Column(db.String(5), default='min')  

class Registro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    persona_id = db.Column(db.Integer, nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    rol = db.Column(db.String(20), nullable=False)
    hora_entrada = db.Column(db.String(30), nullable=False)
    hora_salida = db.Column(db.String(30))
    activo = db.Column(db.Boolean, default=True)

class Admin(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))

import random
import string
def generar_pin():
    return "".join(random.choices(string.digits, k=6))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/hardware')
def hardware():
    return render_template('hardware.html')

# ADMINISTRADOR
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        admin = Admin.query.filter_by(username=username).first()
        if admin and admin.check_password(password):
            login_user(admin)
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Usuario o contraseña incorrectos', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/admin')
@login_required
def admin_dashboard():
    estudiantes = Estudiante.query.all()
    # Solo estudiantes en registros
    registros = Registro.query.filter_by(rol="Estudiante").order_by(Registro.id.desc()).limit(20).all()
    # Solo visitantes en visitantes
    visitantes = Visitante.query.order_by(Visitante.id.desc()).limit(10).all()
    # Visitantes activos cuyo tiempo terminó
    visitantes_alerta = []
    ahora = datetime.now()
    for v in Visitante.query.filter_by(hora_salida=None).all():
        unidad = v.unidad if v.unidad else 'min'
        limite = v.tiempo_limite
        entrada = datetime.strptime(v.hora_entrada, "%Y-%m-%d %H:%M:%S")
        if unidad == 'h':
            fin = entrada + timedelta(hours=limite)
        else:
            fin = entrada + timedelta(minutes=limite)
        if ahora > fin:
            visitantes_alerta.append(v)
    return render_template('admin_dashboard.html', estudiantes=estudiantes, registros=registros, visitantes=visitantes, visitantes_alerta=visitantes_alerta)

@app.route('/admin/nuevo_estudiante', methods=['POST'])
@login_required
def nuevo_estudiante():
    nombre = request.form.get('nombre')
    dni = request.form.get('dni')
    telefono = request.form.get('telefono')
    curso = request.form.get('curso')
    salon = request.form.get('salon')
    if not (nombre and dni and telefono and curso and salon):
        flash('Todos los campos son obligatorios', 'danger')
        return redirect(url_for('admin_dashboard'))
    if Estudiante.query.filter_by(dni=dni).first():
        flash('DNI ya registrado', 'danger')
        return redirect(url_for('admin_dashboard'))
    pin = generar_pin()
    while Estudiante.query.filter_by(pin=pin).first():
        pin = generar_pin()
    estudiante = Estudiante(nombre=nombre, dni=dni, telefono=telefono, curso=curso, salon=salon, pin=pin)
    db.session.add(estudiante)
    db.session.commit()
    flash(f'Estudiante registrado con PIN: {pin}', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/eliminar_estudiante/<int:id>', methods=['POST'])
@login_required
def eliminar_estudiante(id):
    estudiante = Estudiante.query.get(id)
    if estudiante:
        db.session.delete(estudiante)
        db.session.commit()
        flash('Estudiante eliminado', 'success')
    return redirect(url_for('admin_dashboard'))

# VISITANTES
@app.route('/visitante', methods=['GET', 'POST'])
def visitante():
    mensaje = None
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        motivo = request.form.get('motivo')
        tiempo_limite = int(request.form.get('tiempo_limite'))
        unidad = request.form.get('unidad_tiempo')
        ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if not (nombre and motivo and tiempo_limite):
            mensaje = "Todos los campos son obligatorios"
        else:
            visitante = Visitante(nombre=nombre, motivo=motivo, hora_entrada=ahora, tiempo_limite=tiempo_limite, unidad=unidad)
            db.session.add(visitante)
            db.session.commit()
            nuevo_registro = Registro(
                persona_id=visitante.id,
                nombre=visitante.nombre,
                rol="Visitante",
                hora_entrada=ahora,
                activo=True
            )
            db.session.add(nuevo_registro)
            db.session.commit()
            mensaje = f"Visitante {nombre} registrado correctamente."
    # Visitantes activos (sin hora_salida)
    visitantes_activos = Visitante.query.filter_by(hora_salida=None).all()
    return render_template('visitante.html', mensaje=mensaje, visitantes_activos=visitantes_activos)

# DASHBOARD ESTUDIANTE
@app.route('/estudiante/login', methods=['GET', 'POST'])
def estudiante_login():
    if request.method == 'POST':
        pin = request.form.get('pin')
        estudiante = Estudiante.query.filter_by(pin=pin).first()
        if estudiante:
            registro_activo = Registro.query.filter_by(persona_id=estudiante.id, rol="Estudiante", activo=True).first()
            ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if registro_activo:
                # Registrar salida
                registro_activo.hora_salida = ahora
                registro_activo.activo = False
                db.session.commit()
                flash('¡Salida registrada correctamente! Esperamos verte pronto.', 'success')
                return redirect(url_for('estudiante_login'))
            else:
                # Registrar entrada y permitir acceso al dashboard
                session['estudiante_id'] = estudiante.id
                nuevo_registro = Registro(
                    persona_id=estudiante.id,
                    nombre=estudiante.nombre,
                    rol="Estudiante",
                    hora_entrada=ahora,
                    activo=True
                )
                db.session.add(nuevo_registro)
                db.session.commit()
                return redirect(url_for('estudiante_dashboard'))
        else:
            flash('PIN incorrecto', 'danger')
    return render_template('estudiante_login.html')

@app.route('/estudiante/dashboard', methods=['GET', 'POST'])
def estudiante_dashboard():
    estudiante_id = session.get('estudiante_id')
    if not estudiante_id:
        return redirect(url_for('estudiante_login'))
    estudiante = Estudiante.query.get(estudiante_id)
    materias = Materia.query.filter_by(estudiante_id=estudiante_id).all()
    return render_template('estudiante_dashboard.html', estudiante=estudiante, materias=materias)

@app.route('/estudiante/agregar_materia', methods=['POST'])
def agregar_materia():
    estudiante_id = session.get('estudiante_id')
    if not estudiante_id:
        return redirect(url_for('estudiante_login'))
    nombre = request.form.get('nombre')
    hora_inicio = request.form.get('hora_inicio')
    hora_fin = request.form.get('hora_fin')
    if not (nombre and hora_inicio and hora_fin):
        flash('Todos los campos son obligatorios', 'danger')
        return redirect(url_for('estudiante_dashboard'))
    materia = Materia(nombre=nombre, hora_inicio=hora_inicio, hora_fin=hora_fin, estudiante_id=estudiante_id)
    db.session.add(materia)
    db.session.commit()
    flash('Materia agregada', 'success')
    return redirect(url_for('estudiante_dashboard'))

@app.route('/estudiante/eliminar_materia/<int:id>', methods=['POST'])
def eliminar_materia(id):
    estudiante_id = session.get('estudiante_id')
    if not estudiante_id:
        return redirect(url_for('estudiante_login'))
    materia = Materia.query.get(id)
    if materia and materia.estudiante_id == estudiante_id:
        db.session.delete(materia)
        db.session.commit()
        flash('Materia eliminada', 'success')
    return redirect(url_for('estudiante_dashboard'))

@app.route('/estudiante/logout')
def estudiante_logout():
    session.pop('estudiante_id', None)
    return redirect(url_for('estudiante_login'))

# EXPORTAR HISTORIAL A CSV
@app.route('/admin/exportar_csv')
@login_required
def exportar_csv():
    registros = Registro.query.order_by(Registro.id.desc()).all()
    def generar():
        yield 'Nombre,Rol,Entrada,Salida\n'
        for reg in registros:
            yield f'{reg.nombre},{reg.rol},{reg.hora_entrada},{reg.hora_salida or ""}\n'
    return Response(generar(), mimetype='text/csv',
                    headers={"Content-Disposition": "attachment;filename=historial_accesos.csv"})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if not Admin.query.filter_by(username='admin').first():
            admin = Admin(username='admin')
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
    app.run(debug=True)
    
    
    
    '''
__/\\\\\\\\\\\\\\\__/\\\\____________/\\\\____________________/\\\\\\\\\\\\_____/\\\\\\\\\\\\\\\__/\\\________/\\\_        
 _\/\\\///////////__\/\\\\\\________/\\\\\\___________________\/\\\////////\\\__\/\\\///////////__\/\\\_______\/\\\_       
  _\/\\\_____________\/\\\//\\\____/\\\//\\\___________________\/\\\______\//\\\_\/\\\_____________\//\\\______/\\\__      
   _\/\\\\\\\\\\\_____\/\\\\///\\\/\\\/_\/\\\___________________\/\\\_______\/\\\_\/\\\\\\\\\\\______\//\\\____/\\\___     
    _\/\\\///////______\/\\\__\///\\\/___\/\\\___________________\/\\\_______\/\\\_\/\\\///////________\//\\\__/\\\____    
     _\/\\\_____________\/\\\____\///_____\/\\\___________________\/\\\_______\/\\\_\/\\\________________\//\\\/\\\_____   
      _\/\\\_____________\/\\\_____________\/\\\___________________\/\\\_______/\\\__\/\\\_________________\//\\\\\______  
       _\/\\\\\\\\\\\\\\\_\/\\\_____________\/\\\__/\\\\\\\\\\\\\\\_\/\\\\\\\\\\\\/___\/\\\\\\\\\\\\\\\______\//\\\_______ 
        _\///////////////__\///______________\///__\///////////////__\////////////_____\///////////////________\///________
    '''