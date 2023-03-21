FROM python:3.10

# Install app
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /usr/src/app
ENV PYTHONPATH "${PYTHONPATH}:/usr/src"

# Startup script
COPY run_django.sh /usr/local/bin/
CMD ["run_django.sh"]
