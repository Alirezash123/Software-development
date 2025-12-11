from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clinic.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# جدول نقش کاربران
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)  # guest, regular, doctor

# جدول کاربران
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    phone_number = db.Column(db.String(20))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    national_medical_number = db.Column(db.String(50))  # فقط برای پزشک

    role = db.relationship('Role', backref='users')
    visits = db.relationship('Visit', backref='user', lazy=True)
    comments = db.relationship('Comment', backref='user', lazy=True)
    favorites = db.relationship('FavoriteDoctor', backref='user', lazy=True)
    doctor_profile = db.relationship('DoctorProfile', uselist=False, backref='user')

# جدول اطلاعات پزشک
class DoctorProfile(db.Model):
    __tablename__ = 'doctor_profiles'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    address = db.Column(db.String(255))
    city = db.Column(db.String(100))  # برای فیلتر بر اساس شهر
    specialty = db.Column(db.String(100))  # تخصص پزشک
    degree = db.Column(db.String(100))  # مدرک تحصیلی
    work_days = db.Column(db.String(255))  # مثال: "شنبه,یکشنبه,دوشنبه"
    work_hours = db.Column(db.String(255))  # مثال: "08:00-12:00,14:00-18:00"

    visits = db.relationship('Visit', backref='doctor', lazy=True)
    comments = db.relationship('Comment', backref='doctor', lazy=True)
    favorited_by = db.relationship('FavoriteDoctor', backref='doctor', lazy=True)

# جدول وقت ویزیت
class Visit(db.Model):
    __tablename__ = 'visits'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor_profiles.id'), nullable=False)
    visit_date = db.Column(db.Date, nullable=False)
    visit_time = db.Column(db.Time, nullable=False)
    status = db.Column(db.String(50), default="pending")  # pending, confirmed, cancelled

# جدول کامنت کاربران
class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor_profiles.id'), nullable=False)
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# جدول علاقه‌مندی پزشک برای کاربران
class FavoriteDoctor(db.Model):
    __tablename__ = 'favorite_doctors'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor_profiles.id'), nullable=False)

# ایجاد دیتابیس
if __name__ == "__main__":
    db.create_all()
    print("Database created successfully!")