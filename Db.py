اوکی، من بر اساس همان قالب و سبک مستند Auth Service، مستند Doctor Service را آماده کردم. این مستند شامل توضیح سرویس، دیتابیس، endpointها، ورودی/خروجی و نمونه curl است.


---

مستند Doctor Service

۱. معرفی سرویس

سرویس Doctor Service مسئول مدیریت پروفایل پزشکان، برنامه کاری و وقت‌های رزرو شده است.
این سرویس به صورت مستقل از سرویس احراز هویت عمل می‌کند و با سرویس Auth از طریق JWT و API Call ارتباط دارد.

مسئولیت‌های سرویس:

ایجاد و مدیریت پروفایل پزشک

مشاهده و بروزرسانی برنامه کاری

مشاهده لیست ویزیت‌ها

ارائه API برای کاربران عادی جهت مشاهده و رزرو وقت پزشکان



---

۲. دیتابیس

۲-۱. جدول DoctorProfile

فیلد	نوع	توضیح

id	Integer, PK	شناسه داخلی
auth_user_id	Integer, Unique, NotNull	شناسه کاربر از Auth Service
medical_number	String, Unique, NotNull	شماره نظام پزشکی
phone	String, NotNull	شماره تلفن
city	String	شهر محل مطب
specialty	String	تخصص پزشک
degree	String	مدرک تحصیلی
work_days	String	روزهای کاری (مثال: "Mon,Tue,Wed")
work_hours	String	ساعات کاری (مثال: "09:00-12:00,14:00-18:00")


۲-۲. جدول Visit

فیلد	نوع	توضیح

id	Integer, PK	شناسه ویزیت
patient_id	Integer	شناسه کاربر از User Service
doctor_id	Integer, FK	ارجاع به DoctorProfile
date	Date	تاریخ ویزیت
time	Time	زمان ویزیت
status	String	وضعیت ویزیت (pending/accepted/cancelled)



---

۳. Endpoints

۳-۱. مشاهده وقت‌های ویزیت پزشک

GET /visits
Headers: Authorization: Bearer <JWT>

دکوریتورها: login_required + doctor_required
خروجی نمونه:

[
  {
    "id": 1,
    "patient_id": 5,
    "date": "2025-12-20",
    "time": "10:00",
    "status": "pending"
  }
]

curl نمونه:

curl -H "Authorization: Bearer <JWT>" http://localhost:5001/visits


---

۳-۲. مشاهده برنامه کاری پزشک

GET /schedule
Headers: Authorization: Bearer <JWT>

خروجی نمونه:

{
  "work_days": "Mon,Tue,Wed",
  "work_hours": "09:00-12:00,14:00-18:00"
}

curl نمونه:

curl -H "Authorization: Bearer <JWT>" http://localhost:5001/schedule


---

۳-۳. بروزرسانی برنامه کاری پزشک

PUT /schedule
Headers: Authorization: Bearer <JWT>
Body:
{
  "work_days": "Mon,Tue,Thu",
  "work_hours": "08:00-12:00,13:00-17:00"
}

خروجی نمونه:

{"message": "Schedule updated successfully"}

curl نمونه:

curl -X PUT -H "Authorization: Bearer <JWT>" \
     -H "Content-Type: application/json" \
     -d '{"work_days":"Mon,Tue,Thu","work_hours":"08:00-12:00,13:00-17:00"}' \
     http://localhost:5001/schedule


---

۳-۴. ایجاد پروفایل پزشک (از Auth Service)

POST /create
Body:
{
  "auth_user_id": 1,
  "medical_number": "123456",
  "phone": "09123456789"
}

خروجی نمونه:

{"message": "Doctor profile created"}

curl نمونه:

curl -X POST -H "Content-Type: application/json" \
     -d '{"auth_user_id":1,"medical_number":"123456","phone":"09123456789"}' \
     http://localhost:5001/create


---

۴. نحوه استفاده

1. ابتدا کاربر در سرویس Auth ثبت نام و JWT دریافت می‌کند.


2. برای دکتر: پس از ثبت نام، اطلاعات پزشک از Auth Service به Doctor Service ارسال می‌شود (POST /create).


3. پزشک می‌تواند با JWT وارد Doctor Service شود و وقت‌ها و برنامه کاری خود را مدیریت کند.


4. کاربران عادی از طریق User Service می‌توانند وقت رزرو کنند (API Call به Doctor Service).




---

۵. نکات مهم

تمام دسترسی‌ها از طریق JWT کنترل می‌شوند.

دکوریتورهای login_required و doctor_required امنیت را تضمین می‌کنند.

ارتباط بین سرویس‌ها از طریق REST API Call انجام می‌شود.

جدول Visit وابسته به هر پزشک و کاربر است و هر درخواست باید ID مناسب را داشته باشد.



---

اگر بخوای، می‌تونم یک فایل PDF یا Word کامل مستند Doctor Service هم برات آماده کنم که قابل تحویل مستقیم باشه و شامل تمام جداول، endpointها، نمونه curl و توضیحات باشه.

میخوای برات آماده کنم؟

