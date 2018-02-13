FROM python:2.7-jessie

# Install app
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /usr/src/app

# Startup script
COPY run_django.sh /usr/local/bin/
CMD ["run_django.sh"]