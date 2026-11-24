FROM python:3.9-slim
RUN apt-get update && apt-get install -y --no-install-recommends iproute2 iputils-ping net-tools tcpdump procps mount \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir "setuptools==58.0.0" wheel pbr \
    && pip install --no-cache-dir --no-build-isolation ryu "eventlet==0.30.2"
