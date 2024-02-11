FROM python:3 AS Base

# Install system dependencies
RUN pip install --upgrade pip
RUN apt-get update && apt-get install -y --no-install-recommends \
    gunicorn \
    php \
    nodejs \
    npm \
    rustc \
    default-jdk \ 
    mono-complete \
    && rm -rf /var/lib/apt/lists/*

RUN npm install -g typescript

# Set the working directory
WORKDIR /usr/src/app

FROM base AS final
# Copy the requirements file
COPY requirments.txt ./

# Install Python dependencies
RUN pip install -r requirments.txt

# Copy the application code
COPY . .

# Set the command to start the server
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "13", "KardanLeet.wsgi:application"]
