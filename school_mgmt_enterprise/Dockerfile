
# Builder
FROM python:3.11-slim as builder
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Final image
FROM python:3.11-slim
WORKDIR /app
ENV PATH=/root/.local/bin:$PATH
COPY --from=builder /root/.local /root/.local
COPY . /app
ENV FLASK_APP=run.py
CMD ["gunicorn", "--config", "gunicorn.conf.py", "run:app"]
