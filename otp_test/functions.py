from datetime import datetime, timedelta
from random import randint

import pytz
from pydantic import BaseModel

import producer
from connection import DbMongoManager


class LoginForm(BaseModel):
    phone_number_or_email: str
    notification_type: str

async def check_phone_number_or_email(phone_number_or_email: str):
    with DbMongoManager("mst_customer") as my_coll:
        result={}
        is_exist = True
        data=my_coll.aggregate([
                    {'$project':
                        {
                            'id':'$id',
                            'email':{'$toLower':'$email'},
                            'phone_number':'$phone_number',
                            'full_name':'$full_name',
                            'time_otp_request':'$time_otp_request'
                        }},
                    {'$match':{'$or':[
                        {'email':phone_number_or_email.lower()},
                        {'phone_number':phone_number_or_email}
                        ]}},
                    {'$limit':1}
                ])
        for i in data:
            result['id']=i['id']
            result['email']=i['email']
            result['phone_number']=i['phone_number']
            result['full_name']=i['full_name']
            result['time_otp_request']=i['time_otp_request']

        if result == {}:
            is_exist = False

        return {'is_exist': is_exist, 'data': result}

async def get_interval(phone_number_or_email: str):
    with DbMongoManager("mst_customer") as my_coll:
        request_time=None
        data=my_coll.aggregate([
                    {'$project':
                        {
                            'id':'$id',
                            'email':{'$toLower':'$email'},
                            'phone_number':'$phone_number',
                            'full_name':'$full_name',
                            'time_otp_request':'$time_otp_request',
                            # 'is_firts_login':'$is_firts_login'
                        }},
                    {'$match':{'$or':[
                        {'email':phone_number_or_email.lower()},
                        {'phone_number':phone_number_or_email}
                        ]}},
                    {'$limit':1}
                ])
        for i in data:
            request_time=i['time_otp_request']
        if(request_time==None or request_time==""):
            return 60
        else:
            current=datetime.utcnow()
            interval=current-request_time
            return interval.seconds

async def generate_otp(n: int):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

async def UpdateOtp(id: str, otp:str):
    with DbMongoManager("mst_customer")as my_coll:
        query={'id':id}
        new_value={ '$set': { 'otp_password': otp,'time_otp_request':datetime.utcnow() }}
        my_coll.update_one(query,new_value)

async def send_sms(LoginForm : any, otp : str):
    time = datetime.now(tz=pytz.timezone('Asia/Jakarta'))+timedelta(0,60)
    message='Kode verifikasi akun Bidbox.id kamu adalah {} Demi keamanan, jangan berikan kode verifikasi ini kepada siapa pun Berlaku hingga {}'.format(otp,time.strftime("%d/%m/%Y %H:%M"))
    await producer.send_message(
        {
            'notification_type': LoginForm.notification_type,
            'payload': {
                'message':message,
                'phone_number':LoginForm.phone_number_or_email.replace("+","")
            }
        }
    )

async def send_email(LoginForm : LoginForm, full_name : str, email : str, otp : str):
    await producer.send_message(
        {
            'notification_type':'email',
            'payload':{
                'subject':'Bidbox',
                'customer_email':email,
                'email_content':{
                    'kode_otp':otp,
                    'customer_name':full_name,
                    'frontend_base_url': settings.FRONTEND_BASE_URL
                },
                'template':"RequestOtp.html",
                'prefix':'request_otp'
            }
        }
    )


async def send_whatsapp(LoginForm : LoginForm, otp : str):
    time=datetime.now(tz=pytz.timezone('Asia/Jakarta'))+timedelta(0,60)
    await producer.send_message(
        {
            'notification_type':'whatsapp',
            'payload':{
                'otp':str(otp),
                'phone_number':LoginForm.phone_number_or_email,
                'date':time.strftime("%d/%m/%Y"),
                'time':time.strftime("%H:%M")
            }
        }
    )
