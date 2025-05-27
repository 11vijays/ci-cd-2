FROM debian:11

# Install Python manually (since it's not a Python base)
RUN apt-get update && apt-get install -y \
    python3 python3-pip python3-venv \
    curl gnupg2 apt-transport-https \
    unixodbc unixodbc-dev gcc g++

# Install Microsoft ODBC Driver 18
RUN curl -sSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > /etc/apt/trusted.gpg.d/microsoft.gpg && \
    curl -sSL https://packages.microsoft.com/config/debian/11/prod.list -o /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql18 && \
    rm -rf /var/lib/apt/lists/*

# Set workdir
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy your app
COPY . .

# Expose port
EXPOSE 8000

# Run FastAPI app
CMD ["python3", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
