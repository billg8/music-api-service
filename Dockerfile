FROM alpine:latest
WORKDIR /app
COPY . /app
ENV FLASK_APP=main.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV API_KEY="756b869a57005cce1c8f8ba8c9d0bf48"
RUN apk update && apk upgrade
RUN apk add --no-cache gcc musl-dev linux-headers
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["flask", "run"]
