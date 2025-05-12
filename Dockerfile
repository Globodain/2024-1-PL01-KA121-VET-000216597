FROM python:3.9

WORKDIR /app

# Install dependencies including watchdog for better file watching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir watchdog gunicorn pymysql cryptography

# Copy application files
COPY . .

# Set environment variables
ENV FLASK_APP=microblog.py
ENV FLASK_ENV=development
ENV FLASK_DEBUG=1

# Permissions and setup
RUN chmod +x boot.sh && \
    flask translate compile

EXPOSE 5000

ENTRYPOINT ["./boot.sh"]