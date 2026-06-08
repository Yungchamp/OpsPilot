FROM ubuntu:24.04

WORKDIR /app

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
      python3 python3-pip python3-venv git ca-certificates && \
    rm -rf /var/lib/apt/lists/*

COPY . .

RUN python3 -m pip install --upgrade pip setuptools wheel
RUN python3 -m pip install ./

CMD ["python3", "-m", "opspilot.cli", "health"]
