import uvicorn
from typing import Optional

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

import boto3
import functions

app = FastAPI()

class LoginForm(BaseModel):
    phone_number_or_email: str
    notification_type: str

@app.post('/send_otp')
async def post(LoginForm : LoginForm):
    credentials_exception = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Phone number or Email Not Found!",
    )
    result = await functions.check_phone_number_or_email(LoginForm.phone_number_or_email)
    if result['is_exist']:
        return result['data']
    else:
        raise credentials_exception

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)