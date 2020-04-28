

# docker build -t sagecontinuum/sage-cli .

# docker run -ti --net sage-storage-api_default sagecontinuum/sage-cli 

FROM python:3-alpine

WORKDIR /workdir

COPY . /workdir
RUN apk add git
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install .

ENTRYPOINT /bin/ash
