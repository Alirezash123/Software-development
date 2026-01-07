# 🏥 سامانه نوبت‌دهی پزشکان – REST API

---

## 📌 معرفی پروژه
این پروژه یک REST API مبتنی بر Flask است که برای مدیریت نوبت‌دهی پزشکان طراحی شده است.
سیستم دارای سه نقش کاربری می‌باشد:

- کاربر مهمان
- کاربر عادی
- پزشک

احراز هویت با استفاده از JWT Token انجام شده و پروژه قابلیت اجرا در Docker را دارد.

---

## 🛠 تکنولوژی‌ها
- Python 3
- Flask
- Flask-SQLAlchemy
- Flask-JWT-Extended
- SQLite
- Docker / Docker Compose

---

## 📂 ساختار پروژه

    project/
    │── app.py
    │── models.py
    │── requirements.txt
    │── Dockerfile
    │── docker-compose.yml
    └── README.md

---

## 🔐 احراز هویت (JWT)

### محتوای JWT
    {
      "user_id": 1,
      "role": "user"
    }

### دکوریتورها
- login_required : بررسی معتبر بودن JWT
- role_required(role) : بررسی نقش کاربر

---

## 👥 نقش‌های کاربری

### کاربر مهمان
- ثبت‌نام
- ورود
- مشاهده لیست پزشکان
- جستجو بر اساس شهر، تخصص یا مدرک

### کاربر عادی
- تمام امکانات کاربر مهمان
- مشاهده زمان‌های ویزیت
- درخواست نوبت
- مشاهده نوبت‌های خود
- افزودن پزشک به علاقه‌مندی
- ارسال کامنت
- ویرایش پروفایل
- خروج از سامانه

### پزشک
- مشاهده نوبت‌ها
- ویرایش اطلاعات مطب
- تنظیم روزها و ساعات کاری
- مشاهده کامنت‌ها

---

## 🌐 مستند API ها

### احراز هویت

ثبت‌نام  
POST /auth/register

    {
      "username": "doctor1",
      "password": "123456",
      "role": "doctor",
      "phone": "09120000000",
      "medical_id": "MD123"
    }

ورود  
POST /auth/login

    {
      "username": "doctor1",
      "password": "123456"
    }

---

### API های کاربر مهمان

دریافت لیست پزشکان  
GET /doctors

Query Params (اختیاری):
- city
- specialty
- degree

---

### API های کاربر عادی
Header الزامی:

    Authorization: Bearer <JWT>

درخواست نوبت  
POST /appointments

    {
      "doctor_id": 1,
      "time": "2026-01-10T10:00:00"
    }

مشاهده نوبت‌های من  
GET /appointments/my

افزودن پزشک به علاقه‌مندی  
POST /favorites

    {
      "doctor_id": 1
    }

ارسال کامنت  
POST /comments

    {
      "doctor_id": 1,
      "content": "پزشک بسیار حرفه‌ای"
    }

ویرایش پروفایل  
PUT /profile

    {
      "first_name": "Ali",
      "last_name": "Ahmadi",
      "phone": "09120000000"
    }

---

### API های پزشک

مشاهده نوبت‌ها  
GET /doctor/appointments

ویرایش اطلاعات مطب  
PUT /doctor/profile

    {
      "address": "Tehran - Valiasr",
      "city": "Tehran",
      "specialty": "Cardiology",
      "degree": "MD"
    }

تنظیم ساعات کاری  
PUT /doctor/worktime

    {
      "work_days": "شنبه-یکشنبه",
      "work_hours": "08:00-14:00"
    }

مشاهده کامنت‌ها  
GET /doctor/comments

---

## 🐳 اجرای پروژه با Docker

    docker-compose up --build

---

## 🧪 سناریوی تست
1. ثبت‌نام کاربر
2. ورود و دریافت JWT
3. مشاهده پزشکان
4. درخواست نوبت
5. ورود پزشک
6. مشاهده نوبت‌ها



















### مستند API سرویس احراز هویت و کنترل دسترسی (Auth Service)                   



این سرویس مسئول ثبت‌نام، ورود، احراز هویت با JWT و کنترل دسترسی کاربران است. طبق صورت پروژه، کاربران می‌توانند یکی

 ازدو نقش زیر را داشته باشند:

 

user (کاربر عادی)

 

doctor (پزشک)

 

 

این سرویس هیچ اطلاعات دامنه‌ای مثل شهر، تخصص، ویزیت و… را نگه‌داری نمی‌کند و فقط منبع حقیقت هویت کاربران است.





### 🔐 احراز هویت با JWT                                                   



بعد از ورود موفق، یک JWT Token تولید می‌شود

 

این توکن در Header تمام درخواست‌های سایر سرویس‌ها ارسال می‌شود

 

سایر سرویس‌ها با استفاده از این توکن هویت و نقش کاربر را تشخیص می‌دهند





 

Header استاندارد:

 



```
<Authorization: Bearer <JWT_TOKEN
```









**ثبت نام کاربر / پزشک**

 

Endpoint

 

/register

 

توضیح

 

برای همه کاربران: username، password و role اجباری است

 

اگر نقش doctor باشد، احراز هویت پزشک با شماره نظام پزشکی و شماره تلفن انجام می‌شود





```Body(json)
{
,  "username": "ali"
,  "password": "123456"
,  "role": "doctor"
,  "medical_number": "12345"
  "phone": "09123456789
}
```



```result
{
 "message": "registered successfully"
}
```

**curl**



```curl
curl --location 'http://127.0.0.1:5000/register' \
--header 'Content-Type: application/json' \
--data '{
    "username":"alireza",
    "password":"1234",
    "role":"user"
}'
```

**ورود (Login)**

 

Endpoint

 

/login

 

توضیح

 

در صورت صحیح بودن اطلاعات، JWT Token تولید می‌شود

 

این توکن برای دسترسی به سایر سرویس‌ها استفاده می‌شود





**Body(json)**



```Body
{
,  "username": "ali"
  "password": "123456"
}

```

**پاسخ موفق**



```
{
,"<token": "<JWT_TOKEN"
  "role": "user"
}
```

**curl**



```
curl --location 'http://127.0.0.1:5000/login' \
--header 'Content-Type: application/json' \
--data '{
    "username":"alireza",
    "password":"1234"
}'
```

## مستند Doctor Service                                                  

 

**مشاهده وقت‌های ویزیت پزشک**



**Endpoint:**

visits/



```Heder
<Headers: Authorization: Bearer <JWT
```

دکوریتورها: login_required + doctor_required



```
curl --location 'http://127.0.0.1:5001/visits' \
header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJyb2xlIjoiZG9jdG9yIiwiZXhwIjoxNzY2MDA4NjY1fQ.B4XeeoVfbLezfrfIOcvCv9ybLDzYniwM4xLq4uqHzIM'
```

**خروجی نمونه:**



```
[
{
"id": 1,
    "patient_id": 5,
    "date": "2025-12-20",
    "time": "10:00",
    "status": "pending"
}
]
```

**مشاهده برنامه کاری پزشک**



**Endpoint**: GET /schedule



```
<Headers: Authorization: Bearer <JWT
```

دکوریتورها: login_required + doctor_required



```
curl -H "Authorization: Bearer <JWT>" http://localhost:5001/schedule
```

**خروجی نمونه:**



```
{
,    "work_days": "Mon,Tue,Thu"
    "work_hours": "08:00-12:00,13:00-17:00,08:00-22:00"
}
```

**بروزرسانی برنامه کاری پزشک**



**Endpoint:**PUT /schedule



```
<Headers: Authorization: Bearer <JWT
```

دکوریتورها: login_required + doctor_required



**(json)Body:**

```
{
,  "work_days": "Mon,Tue,Thu"
  "work_hours": "08:00-12:00,13:00-17:00"
}
```

**خروجی نمونه:**



```
{
    "message": "Schedule updated successfully"
}
```

**curl:**

```curl
curl --location --request PUT 'http://127.0.0.1:5001/schedule' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJyb2xlIjoiZG9jdG9yIiwiZXhwIjoxNzY2MDA4NjY1fQ.B4XeeoVfbLezfrfIOcvCv9ybLDzYniwM4xLq4uqHzIM' \
--data '{
    "work_days":"Mon,Tue,Thu",
    "work_hours":"08:00-12:00,13:00-17:00,08:00-22:00"
}'
```

**مشاهده کامنت های مرتبط با خود**



**Endpoint:**GET /comments



```
<Headers: Authorization: Bearer <JWT
```

دکوریتورها: login_required + doctor_required



**خروجی نمونه:**



```
[
  {
    "user_id": 12,
    "comment": "دکتر بسیار خوش‌برخورد بود",
    "created_at": "2025-01-08"
  }
]
```

**تعغیر مشخصات مطب** 



**Endpoint:**PUT /clinic-info



```
<Headers: Authorization: Bearer <JWT
```

دکوریتورها: login_required + doctor_required



**(json)Body:**



```
{
  "phone": "09123456789",
  "address": "تهران، خیابان ولیعصر، پلاک ۱۰"
}
```

**خروجی نمونه:**



```
{
    "message": "Clinic info updated"
}
```



**تعغیر مشخصات پروفایل**



 PUT /doctor-profile **:Endpoint**



```
<Headers: Authorization: Bearer <JWT
```

دکوریتورها: login_required + doctor_required



**(json)Body:**



```
{
    "city":"Mashhad",
    "specialty":"head"
}
```

**خروجی نمونه:**



```
{
    "message": "profile info updated"
}
```



### **مستند User Service (پنل کاربران عادی)**                                   

Service مسئول ارائه امکانات کاربران عادی سامانه می‌باشد. این سرویس امکان مشاهده پزشکان، رزرو و مشاهده ویزیت‌ها، مدیریت علاقه‌مندی‌ها، ارسال کامنت و مدیریت اطلاعات کاربری را فراهم می‌کند.

 

این سرویس برای انجام برخی عملیات از Doctor Service استفاده می‌کند 



**مشاهده لیست پزشکان (با فیلتر)**



**Endpoints**:GET /doctors



Query Parameters (اختیاری):

| نام       | توضیح              |
| --------- | ------------------ |
| city      | فیلتر بر اساس شهر  |
| specialty | فیلتر بر اساس تخصص |



**نمونه درخواست:**



```
curl "http://localhost:5002/doctors?city=Tehran&specialty=Cardiology
```

**پاسخ نمونه**



```
[
  {
    "doctor_id": 1,
    "city": "Tehran",
    "specialty": "Cardiology"
  }
]

```

**درخواست رزرو ویزیت**



**Endpoint**:POST /visits



```
<Headers: Authorization: Bearer <JWT
```

**Body**

```
{
  "doctor_id": 1,
  "date": "2025-01-10",
  "time": "10:30"
}

```

**پاسخ**

```
{
    "message": "Visit booked successfully",
    "visit_id": 2
}
```



**مشاهده ویزیت‌های رزرو شده کاربر**



**Endpoint**:GET /my_visits



```
<Headers: Authorization: Bearer <JWT
```

**پاسخ نمونه**



```
[
  {
    "doctor_id": 1,
    "date": "2025-01-10",
    "time": "10:30",
    "status": "accepted"
  }
]

```

**افزودن پزشک به لیست علاقه‌مندی‌ها**



**Endpoint**:POST /favorite



```
<Headers: Authorization: Bearer <JWT
```





**Body**

```
{
  "doctor_id": 1
}

```

**پاسخ**



```
{
  "message": "Doctor added to favorites"
}

```

**ارسال کامنت برای پزشک**



**Endpoint**:POST /comment



```
<Headers: Authorization: Bearer <JWT
```





**Body**



```
{
  "doctor_id": 1,
  "content": "دکتر بسیار خوش برخورد و حرفه‌ای بودند"
}

```

**پاسخ**



```
{
  "message": "Comment added"
}

```

**ثبت یا ویرایش اطلاعات کاربر**



**Endpoint**:POST / PUT /profile



```
<Headers: Authorization: Bearer <JWT
```

**Body**



```
{
  "first_name": "Ali",
  "last_name": "Ahmadi",
  "phone": "09121234567"
}

```



**پاسخ**



```
{
    "message": "Profile saved successfully"
}
```
