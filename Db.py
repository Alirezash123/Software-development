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