FROM python:3.7-alpine

WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install Pillow dependencies
RUN apk --no-cache add \
    build-base \
    python3 \
    python3-dev \
    # wget dependency
    openssl \
    # dev dependencies
    bash \
    git \
    py3-pip \
    sudo \
    # Pillow dependencies
    freetype-dev \
    fribidi-dev \
    harfbuzz-dev \
    jpeg-dev \
    lcms2-dev \
    openjpeg-dev \
    tcl-dev \
    tiff-dev \
    tk-dev \
    zlib-dev

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

# install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN LDFLAGS=-L/usr/lib/x86_64-linux-gnu/ pip install --no-binary pillow pillow
RUN pip install -r requirements.txt
COPY . /app/

# run entrypoint.sh
#ENTRYPOINT ["/app/entrypoint.sh"]