FROM python:3.10
WORKDIR /server
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY src/ .
ENTRYPOINT ["uvicorn", "main:app"]