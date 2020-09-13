from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_sms_get_otp_success():
    response = client.post("/get_otp", json={'phone_number_or_email': '+6281297126699', 'notification_type': 'sms'})
    assert response.status_code == 200
    assert response.json() == {'status': '200', 'data': None, 'message': 'Your otp code has been sent,please check your sms or email!'}

def test_sms_get_otp_failed():
    response = client.post("/get_otp", json={'phone_number_or_email': '+6281297126699', 'notification_type': 'sms'})
    assert response.status_code == 404
    assert response.json() == {"detail":{"status":"404","message":"silahkan tunggu 60 detik untuk meminta otp kembali!"}}

def test_sms_get_otp_invalid_format_phone_number():
    response = client.post("/get_otp", json={'phone_number_or_email': '6281297126699', 'notification_type': 'sms'})
    assert response.status_code == 404
    assert response.json() == {"detail":{"status":"404","message":"Phone number or Email Not Found!"}}