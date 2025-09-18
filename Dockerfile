FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app
ENV PYTHONUNBUFFERED=1
CMD ["gunicorn", "app.api:app", "-b", "0.0.0.0:5000", "--workers", "2"]
