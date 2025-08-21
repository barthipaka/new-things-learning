# Use minimal Python image
FROM python:3.11-slim

# Set timezone (optional)
ENV TZ=Asia/Kolkata

# Install system dependencies: cron, libpq-dev, tzdata
RUN apt-get update && \
    apt-get install -y cron libpq-dev tzdata && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone && \
    rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN python -m pip install --upgrade pip

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all application files (FastAPI + React + cron files)
COPY . /app

# Copy and set up cron schedule
COPY crontab.txt /etc/cron.d/reminder-cron
RUN chmod 0644 /etc/cron.d/reminder-cron && crontab /etc/cron.d/reminder-cron

# Create cron log file
RUN touch /var/log/cron.log

# Copy entrypoint script and make executable
COPY cron-entrypoint.sh /app/cron-entrypoint.sh
RUN chmod +x /app/cron-entrypoint.sh

# Expose FastAPI port
EXPOSE 8561

# Use entrypoint script to start both cron and FastAPI
CMD ["/app/cron-entrypoint.sh"]
