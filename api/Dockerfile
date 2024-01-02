FROM python:3.10

RUN apt-get update && \
    apt-get install -y \
        build-essential \
        make \
        gcc \
        bash \
        sudo && \
    apt-get upgrade -y && \
    pip install --upgrade pip && \
    # Clean up package lists to reduce image size
    rm -rf /var/lib/apt/lists/* 

RUN pip install pika \
                pymongo \
                tensorflowjs \
                flask \
                jax==0.4.21 \
                jaxlib==0.4.21 \
                gunicorn

#RUN rm -f /var/lib/docker/overlay2/7l7ccvw4vgr5em987kwye93nn/merged/lib
#RUN mkdir -p uploads tmp converted
RUN mkdir -p lib uploads tmp converted
COPY /app.py .
COPY /consumer.py .
COPY /convert.sh .
COPY /startup.sh .
COPY /configuration.yaml .
COPY /lib ./lib/


EXPOSE 5000

ENTRYPOINT [ "/bin/bash" ]
CMD [ "startup.sh" ]



