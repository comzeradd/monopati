FROM ubuntu:24.04

LABEL org.opencontainers.image.source="https://codeberg.org/comzeradd/monopati" \
      org.opencontainers.image.description="A minimalistic static content generator" \
      org.opencontainers.image.licenses="GPL-3.0-or-later" \
      org.opencontainers.image.vendor="Nikos Roussos" \
      org.opencontainers.image.title="monopati"

RUN export DEBIAN_FRONTEND="noninteractive" && \
    apt-get -y update && \
    apt-get -y install wget git python3 python3-pip && \
    apt-get clean && \
    pip install --break-system-packages monopati

WORKDIR /app

CMD ["monopati"]
