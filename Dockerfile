FROM python:3.7

WORKDIR /app

COPY requirements.txt /app

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 80

COPY ./otp_test /app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]