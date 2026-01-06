Flask==3.0.0
Flask-SQLAlchemy==3.1.1
Flask-JWT-Extended==4.6.0
Werkzeug==3.0.1





from flask import Flask, request, jsonify, g
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    verify_jwt_in_request,
    get_jwt_identity
)
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from datetime import datetime, timedelta

from models import (
    db,
    User,
    DoctorProfile,
    Appointment,
    Comment,
    FavoriteDoctor,
    Role
)

# ----------------------------------
# App Config
# ----------------------------------
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'secret-key'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)

db.init_app(app)
jwt = JWTManager(app)

# ----------------------------------
# Decorators
# ----------------------------------
def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
        except Exception:
            return jsonify({'msg': 'Authentication required'}), 401

        user = User.query.get(get_jwt_identity())
        if not user:
            return jsonify({'msg': 'Invalid token'}), 401

        g.current_user = user
        return fn(*args, **kwargs)
    return wrapper


def role_required(*roles):
    def decorator(fn):
        @wraps(fn)
        @login_required
        def wrapper(*args, **kwargs):
            if g.current_user.role not in roles:
                return jsonify({'msg': 'Access denied'}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator

# ----------------------------------
# Auth
# ----------------------------------
@app.route('/auth/register', methods=['POST'])
def register():
    data = request.json

    if not all(k in data for k in ['username', 'password', 'role']):
        return jsonify({'msg': 'Missing fields'}), 400

    if data['role'] == Role.DOCTOR:
        if not data.get('phone') or not data.get('medical_id'):
            return jsonify({'msg': 'Doctor info required'}), 400

    user = User(
        username=data['username'],
        password=generate_password_hash(data['password']),
        role=data['role'],
        phone=data.get('phone'),
        medical_id=data.get('medical_id')
    )

    db.session.add(user)
    db.session.commit()

    if user.role == Role.DOCTOR:
        db.session.add(DoctorProfile(user_id=user.id))
        db.session.commit()

    return jsonify({'msg': 'Registered successfully'})


@app.route('/auth/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data.get('username')).first()

    if not user or not check_password_hash(user.password, data.get('password')):
        return jsonify({'msg': 'Invalid credentials'}), 401

    token = create_access_token(identity=user.id)
    return jsonify(access_token=token)

# ----------------------------------
# Guest
# ----------------------------------
@app.route('/doctors', methods=['GET'])
def list_doctors():
    query = DoctorProfile.query

    if request.args.get('city'):
        query = query.filter_by(city=request.args['city'])
    if request.args.get('specialty'):
        query = query.filter_by(specialty=request.args['specialty'])
    if request.args.get('degree'):
        query = query.filter_by(degree=request.args['degree'])

    doctors = query.all()
    return jsonify([
        {
            'id': d.id,
            'city': d.city,
            'specialty': d.specialty,
            'degree': d.degree
        } for d in doctors
    ])

# ----------------------------------
# Doctor Panel
# ----------------------------------
@app.route('/doctor/appointments', methods=['GET'])
@role_required(Role.DOCTOR)
def doctor_appointments():
    profile = DoctorProfile.query.filter_by(user_id=g.current_user.id).first()
    appointments = Appointment.query.filter_by(doctor_id=profile.id).all()

    return jsonify([
        {
            'user_id': a.user_id,
            'time': a.appointment_time,
            'status': a.status
        } for a in appointments
    ])


@app.route('/doctor/worktime', methods=['PUT'])
@role_required(Role.DOCTOR)
def update_worktime():
    profile = DoctorProfile.query.filter_by(user_id=g.current_user.id).first()
    data = request.json

    profile.work_days = data.get('work_days')
    profile.work_hours = data.get('work_hours')
    db.session.commit()

    return jsonify({'msg': 'Worktime updated'})


@app.route('/doctor/comments', methods=['GET'])
@role_required(Role.DOCTOR)
def doctor_comments():
    profile = DoctorProfile.query.filter_by(user_id=g.current_user.id).first()
    comments = Comment.query.filter_by(doctor_id=profile.id).all()

    return jsonify([
        {'content': c.content, 'date': c.created_at}
        for c in comments
    ])

# ----------------------------------
# User
# ----------------------------------
@app.route('/appointments', methods=['POST'])
@role_required(Role.USER)
def request_appointment():
    data = request.json
    appointment = Appointment(
        user_id=g.current_user.id,
        doctor_id=data['doctor_id'],
        appointment_time=datetime.fromisoformat(data['time'])
    )
    db.session.add(appointment)
    db.session.commit()
    return jsonify({'msg': 'Appointment requested'})


@app.route('/favorites', methods=['POST'])
@role_required(Role.USER)
def add_favorite():
    fav = FavoriteDoctor(
        user_id=g.current_user.id,
        doctor_id=request.json['doctor_id']
    )
    db.session.add(fav)
    db.session.commit()
    return jsonify({'msg': 'Added to favorites'})


@app.route('/comments', methods=['POST'])
@role_required(Role.USER)
def add_comment():
    comment = Comment(
        user_id=g.current_user.id,
        doctor_id=request.json['doctor_id'],
        content=request.json['content']
    )
    db.session.add(comment)
    db.session.commit()
    return jsonify({'msg': 'Comment added'})

# ----------------------------------
# Run
# ----------------------------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000)






#########22#########################




from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from .. import db
from ..models import User

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    role = data.get("role")
    phone = data.get("phone")
    medical_id = data.get("medical_id")

    if not username or not password or not role:
        return jsonify({"error": "username, password and role required"}), 400

    hashed_password = generate_password_hash(password)
    user = User(username=username, password=hashed_password, role=role, phone=phone, medical_id=medical_id)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": f"{role} '{username}' registered successfully!"})

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"error": "Invalid credentials"}), 401

    token = create_access_token(identity={"id": user.id, "role": user.role})
    return jsonify({"access_token": token})











from datetime import datetime

# نقش‌های کاربری
class Role:
    GUEST = 'guest'
    USER = 'user'
    DOCTOR = 'doctor'

# جدول کاربران
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # guest, user, doctor
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    phone = db.Column(db.String(20))
    medical_id = db.Column(db.String(50), unique=True)  # فقط برای پزشکان

    # روابط
    appointments = db.relationship('Appointment', backref='user', lazy=True)
    favorite_doctors = db.relationship('FavoriteDoctor', backref='user', lazy=True)
    comments = db.relationship('Comment', backref='user', lazy=True)

# جدول پزشکان (اطلاعات تخصصی پزشک)
class DoctorProfile(db.Model):
    __tablename__ = 'doctor_profiles'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)
    address = db.Column(db.String(255))
    city = db.Column(db.String(100))
    specialty = db.Column(db.String(100))
    degree = db.Column(db.String(100))
    work_days = db.Column(db.String(100))  # مثال: "شنبه-یکشنبه-دوشنبه"
    work_hours = db.Column(db.String(100))  # مثال: "08:00-12:00,14:00-18:00"

    # روابط
    appointments = db.relationship('Appointment', backref='doctor', lazy=True)
    comments = db.relationship('Comment', backref='doctor', lazy=True)

# جدول وقت‌های ویزیت
class Appointment(db.Model):
    __tablename__ = 'appointments'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # کاربر عادی
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor_profiles.id'))  # پزشک
    appointment_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, confirmed, canceled

# جدول کامنت‌ها
class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor_profiles.id'))
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# جدول لیست علاقه‌مندی‌ها
class FavoriteDoctor(db.Model):
    __tablename__ = 'favorite_doctors'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor_profiles.id'))