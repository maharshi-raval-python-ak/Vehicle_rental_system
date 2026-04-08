FROM python:3.10.12

WORKDIR /backend

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

# RUN chmod +x entrypoint.sh && \
#     sed -i 's/\r$//' entrypoint.sh


# ENTRYPOINT ["./entrypoint.sh"]

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]