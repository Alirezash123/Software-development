from flask import Blueprint, request, jsonify
import requests
from models import db, UserProfile, FavoriteDoctor, Comment
from functools import wraps
import jwt
import datetime
from werkzeug.security import generate_password_hash, check_password_hash

user_bp = Blueprint("user_bp", __name__)
DOCTOR_SERVICE_URL = "http://localhost:5001"  # Doctor Panel Service
SECRET_KEY = "SECRET_KEY"  # برای ارسال JWT به Doctor Panel

# -------------------------
# مشاهده لیست پزشکان (با فیلتر)
# -------------------------
@user_bp.route("/doctors", methods=["GET"])
def get_doctors():
    city = request.args.get("city")
    specialty = request.args.get("specialty")
    

    params = {}
    if city: params["city"] = city
    if specialty: params["specialty"] = specialty
    

    response = requests.get(f"{DOCTOR_SERVICE_URL}/doctors", params=params)
    return jsonify(response.json())

# -------------------------
# درخواست رزرو ویزیت
# -------------------------
@user_bp.route("/visits", methods=["POST"])
def book_visit():
    data = request.json
    token = request.headers.get("Authorization")  # JWT از Auth Service
    headers = {"Authorization": token}

    response = requests.post(f"{DOCTOR_SERVICE_URL}/visits", json=data, headers=headers)
    return jsonify(response.json())

# -------------------------
# مشاهده وقت‌های رزرو شده کاربر
# -------------------------
@user_bp.route("/my_visits", methods=["GET"])
def my_visits():
    token = request.headers.get("Authorization")
    headers = {"Authorization": token}

    response = requests.get(f"{DOCTOR_SERVICE_URL}/my_visits", headers=headers)
    return jsonify(response.json())

# -------------------------
# اضافه کردن پزشک به علاقه‌مندی‌ها
# -------------------------
@user_bp.route("/favorite", methods=["POST"])
def add_favorite():
    data = request.json
    user_id = data["user_id"]
    doctor_id = data["doctor_id"]

    fav = FavoriteDoctor(user_id=user_id, doctor_id=doctor_id)
    db.session.add(fav)
    db.session.commit()
    return jsonify({"message": "Doctor added to favorites"})

# -------------------------
# ارسال کامنت برای پزشک
# -------------------------
@user_bp.route("/comment", methods=["POST"])
def add_comment():
    data = request.json
    user_id = data["user_id"]
    doctor_id = data["doctor_id"]
    content = data["content"]

    comment = Comment(user_id=user_id, doctor_id=doctor_id, content=content)
    db.session.add(comment)
    db.session.commit()
    return jsonify({"message": "Comment added"})


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"error": "Token missing"}), 401

        try:
            token = token.replace("Bearer ", "")
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except:
            return jsonify({"error": "Invalid token"}), 401

        return f(payload["user_id"], payload["role"], *args, **kwargs)

    return decorated






# -------------------------
# ثبت یا ویرایش اطلاعات کاربر
# -------------------------
@user_bp.route("/profile", methods=["POST", "PUT"])
@login_required
def upsert_profile(current_user_id, role):
    if role != "user":
        return jsonify({"error": "Only normal users can edit profile"}), 403

    data = request.json

    profile = UserProfile.query.filter_by(
        auth_user_id=current_user_id
    ).first()

    if not profile:
        profile = UserProfile(
            auth_user_id=current_user_id,
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            phone=data.get("phone")
        )
        db.session.add(profile)
    else:
        profile.first_name = data.get("first_name", profile.first_name)
        profile.last_name = data.get("last_name", profile.last_name)
        profile.phone = data.get("phone", profile.phone)

    db.session.commit()

    return jsonify({"message": "Profile saved successfully"})




@user_bp.route("/comments/doctor/<int:doctor_id>", methods=["GET"])
def get_doctor_comments(doctor_id):
    comments = Comment.query.filter_by(doctor_id=doctor_id).all()

    result = []
    for c in comments:
        result.append({
            "comment_id": c.id,
            "patient_id": c.patient_id,
            "text": c.text,
            "created_at": c.created_at
        })

    return jsonify(result)
