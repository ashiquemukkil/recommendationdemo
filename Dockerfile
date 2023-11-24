FROM python:3.9

WORKDIR /project


RUN python3.9 -m pip install --upgrade pip
COPY ./requirements.txt ./requirements.txt
RUN python3.9 -m pip install -r requirements.txt

COPY ./main.py ./main.py
COPY ./router ./router
COPY ./config.py ./config.py

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
