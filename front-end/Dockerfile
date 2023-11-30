FROM python:3.9

WORKDIR /app

COPY . /app
COPY ./cleaned_data.xlsx ./cleaned_data.xlsx
RUN python3.9 -m pip install -r requirements.txt

CMD ["sh", "-c", "sleep 10 && python landing.py"]