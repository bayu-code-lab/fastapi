from typing import Optional

import boto3
import uvicorn
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

import functions

app = FastAPI()

class LoginForm(BaseModel):
    phone_number_or_email: str
    notification_type: str

@app.post('/get_otp')
async def get_otp(LoginForm : LoginForm):
    try:
        result = await functions.check_phone_number_or_email(LoginForm.phone_number_or_email)
        if result['is_exist']:
            interval = await functions.get_interval(LoginForm.phone_number_or_email)
            if interval < 60:
                raise HTTPException(status.HTTP_404_NOT_FOUND, detail={'status': '404','message': 'silahkan tunggu 60 detik untuk meminta otp kembali!'})
            else:
                otp = await functions.generate_otp(6)
                await functions.UpdateOtp(result['data']['id'], otp)
                if LoginForm.notification_type == 'sms':
                    await functions.send_sms(LoginForm, otp)
                elif LoginForm.notification_type == 'email':
                    await functions.send_email(LoginForm, result['data']['full_name'],result['data']['email'], otp)
                elif LoginForm.notification_type == 'whatsapp':
                    await functions.send_whatsapp(LoginForm, otp)
                return {'status': '200', 'data': None, 'message': 'Your otp code has been sent,please check your sms or email!'}
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={'status': '404','message': 'Phone number or Email Not Found! !'})
    except Exception as e:
        #telegram chat bot here!
        raise e

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
