FROM ubuntu:18.04
ENV DEBIAN_FRONTEND=noninteractive
COPY ./install_deps.sh ./
RUN chmod +x ./install_deps.sh && ./install_deps.sh
COPY ./install_bigsi.sh ./
RUN chmod +x ./install_bigsi.sh && ./install_bigsi.sh
ENV PATH /root/miniconda/bin:$PATH
