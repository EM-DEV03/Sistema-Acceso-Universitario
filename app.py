import os
from flask import Flask, render_template, redirect, url_for, request, flash, session, Response
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import csv
import random
import string
from pytz import timezone

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
    pin = db.Column(db.String(3), unique=True, nullable=False)

class Visitante(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    motivo = db.Column(db.String(100))
    numero = db.Column(db.String(20))  # Teléfono o número de contacto
    hora_entrada = db.Column(db.String(19))
    hora_salida = db.Column(db.String(19), nullable=True)
    tiempo_limite = db.Column(db.Integer)
    unidad = db.Column(db.String(5))  # 'min' o 'h'

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
    return db.session.get(Admin, int(user_id))

def generar_pin():
    return "".join(random.choices(string.digits, k=3))

def hora_colombia():
    return datetime.now(timezone('America/Bogota')).strftime("%Y-%m-%d %H:%M:%S")

@app.route('/')
def root():
    return redirect(url_for('estudiante_login'))

@app.route('/index')
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

def actualizar_visitantes_finalizados():
    ahora = datetime.now(timezone('America/Bogota'))
    visitantes_activos = Visitante.query.filter_by(hora_salida=None).all()
    for v in visitantes_activos:
        unidad = v.unidad if v.unidad else 'min'
        limite = v.tiempo_limite
        entrada = datetime.strptime(v.hora_entrada, "%Y-%m-%d %H:%M:%S")
        entrada = timezone('America/Bogota').localize(entrada)
        if unidad == 'h':
            fin = entrada + timedelta(hours=limite)
        else:
            fin = entrada + timedelta(minutes=limite)
        if ahora > fin:
            v.hora_salida = ahora.strftime("%Y-%m-%d %H:%M:%S")
            # También marca el registro como inactivo
            registro = Registro.query.filter_by(persona_id=v.id, rol="Visitante", activo=True).first()
            if registro:
                registro.hora_salida = v.hora_salida
                registro.activo = False
    db.session.commit()

@app.route('/admin')
@login_required
def admin_dashboard():
    actualizar_visitantes_finalizados()
    estudiantes = Estudiante.query.all()
    # Solo estudiantes en registros
    registros = Registro.query.filter_by(rol="Estudiante").order_by(Registro.id.desc()).limit(20).all()
    # Solo visitantes en visitantes
    visitantes = Visitante.query.order_by(Visitante.id.desc()).limit(10).all()
    # Visitantes activos cuyo tiempo terminó
    visitantes_alerta = []
    ahora = datetime.now(timezone('America/Bogota'))
    for v in Visitante.query.filter_by(hora_salida=None).all():
        unidad = v.unidad if v.unidad else 'min'
        limite = v.tiempo_limite
        entrada = datetime.strptime(v.hora_entrada, "%Y-%m-%d %H:%M:%S")
        entrada = timezone('America/Bogota').localize(entrada)
        if unidad == 'h':
            fin = entrada + timedelta(hours=limite)
        else:
            fin = entrada + timedelta(minutes=limite)
        if ahora > fin:
            visitantes_alerta.append(v)
    return render_template(
        'admin_dashboard.html',
        estudiantes=estudiantes,
        registros_estudiantes=registros,
        visitantes=visitantes,
        visitantes_alerta=visitantes_alerta
    )

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
        numero = request.form.get('numero')
        tiempo_limite = int(request.form.get('tiempo_limite'))
        unidad = request.form.get('unidad_tiempo')
        ahora = hora_colombia()
        if not (nombre and motivo and numero and tiempo_limite):
            mensaje = "Todos los campos son obligatorios"
        else:
            visitante = Visitante(nombre=nombre, motivo=motivo, numero=numero, hora_entrada=ahora, tiempo_limite=tiempo_limite, unidad=unidad)
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
    visitantes_activos = Visitante.query.filter_by(hora_salida=None).all()
    return render_template('visitante.html', mensaje=mensaje, visitantes_activos=visitantes_activos)

# ACCESO ESTUDIANTE SOLO PIN (sin dashboard ni materias)
@app.route('/estudiante/login', methods=['GET', 'POST'])
def estudiante_login():
    if request.method == 'POST':
        pin = request.form.get('pin')
        estudiante = Estudiante.query.filter_by(pin=pin).first()
        if estudiante:
            registro_activo = Registro.query.filter_by(persona_id=estudiante.id, rol="Estudiante", activo=True).first()
            ahora = hora_colombia()
            if registro_activo:
                registro_activo.hora_salida = ahora
                registro_activo.activo = False
                db.session.commit()
                flash('¡Salida registrada correctamente! Esperamos verte pronto.', 'success')
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
                flash('¡Ingreso registrado correctamente!', 'success')
            return redirect(url_for('estudiante_login'))
        else:
            flash('PIN incorrecto', 'danger')
    return render_template('estudiante_login.html')

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

@app.template_filter('todatetime')
def todatetime(value):
    from datetime import datetime
    return datetime.strptime(value, "%Y-%m-%d %H:%M:%S")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if not Admin.query.filter_by(username='admin').first():
            admin = Admin(username='admin')
            admin.set_password('123')
            db.session.add(admin)
            db.session.commit()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
