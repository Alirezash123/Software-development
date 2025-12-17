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

