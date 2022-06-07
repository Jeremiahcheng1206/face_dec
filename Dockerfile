ARG TAG
FROM ghcr.io/deephaven/server:edge

RUN apt-get update

RUN apt-get -y install curl wget ffmpeg libsm6 libxext6 && \
    pip install face_recognition opencv-python tensorflow tensorflow_hub

RUN mkdir /object_detection && \
    wget -P /object_detection https://raw.githubusercontent.com/gabrielcassimiro17/raspberry-pi-tensorflow/main/labels.csv && \
    wget -O /object_detection/efficientdet_lite2_detection_1.tar.gz https://tfhub.dev/tensorflow/efficientdet/lite2/detection/1?tf-hub-format=compressed

COPY app.d/ /app.d


