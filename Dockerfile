FROM alpine:3.8.5

RUN apk update \
&& apk upgrade \
&& apk add bash \
&& apk add openjdk8-jre

RUN apk add python3 \
&& python3 -m ensurepip \
&& apk add py3-numpy \
&& apk add libc6-compat

COPY . .

RUN pip3 install -r requirements.txt

ENTRYPOINT [ "spark-submit", "prediction.py" ]
