FROM ubuntu:xenial

ENV ARCH "x86_64-unknown-linux-gnu"
ENV DOWNLOAD_URL "https://static.rust-lang.org/rustup/dist"
ENV PATH="$PATH:~/.cargo/bin"

ARG RUST_VERSION

RUN apt-get update\
  && echo "path: '${PATH}'"\
  && /usr/bin/apt-get -y install apt-utils apt-file wget

RUN mkdir -p /usr/share/rustup/log\
  && cd /usr/share/rustup/ \
  && date +"%F %T - %s" > log/rustup_install_$(date +"%F").log\
  && echo $(date +"%F %T") "- rustup: downloading ..." | tee -a log/rustup_install_$(date +"%F").log\
  && wget -S ${DOWNLOAD_URL}/${ARCH}/rustup-init.sha256 2>&1 | tee -a log/rustup_install_$(date +"%F").log\
  && wget -S ${DOWNLOAD_URL}/${ARCH}/rustup-init 2>&1 | tee -a log/rustup_install_$(date +"%F").log\
  && echo $(date +"%F %T") "- rustup: download checking ..." | tee -a log/rustup_install_$(date +"%F").log\
  && CHKOK=`sha256sum -c rustup-init.sha256` \
  && echo $CHKOK | tee -a log/rustup_install_$(date +"%F").log \
  && if [ -z "$(echo -n $CHKOK | grep -io 'ok')" ]; then echo $(date +"%F %T") "- rustup: download failed"; false; fi \
  && echo $(date +"%F %T") "- rustup: download OK" | tee -a log/rustup_install_$(date +"%F").log\
  && chmod a+x rustup-init && mv rustup-init /usr/local/bin/ \
  && date +"%F %T - %s" >> log/rustup_install_$(date +"%F").log

#Install additional compiler libraries
RUN apt-get -y install gcc clang clang-8 make pkg-config m4

#Install additional forest dependencies
RUN apt-get -y install libssl-dev ocl-icd-opencl-dev
RUN groupadd rust \
  && useradd rust_builder -g rust -md /home/rust-build
USER rust_builder
RUN mkdir -p /home/rust-build/project/ \
  && mkdir -p /home/rust-build/log \
  && cd /home/rust-build/ \
  && date +"%F %T - %s" > log/rustup-init_install_$(date +"%F").log\
  && echo $(date +"%F %T") "- rustup-init: launching ..." | tee -a log/rustup-init_install_$(date +"%F").log\
  && rustup-init -y --no-modify-path 2>&1 | tee -a log/rustup-init_install_$(date +"%F").log
  #&& source ${HOME}/.cargo/env

# Install Rust Version according to Build Argument
RUN if [ -n "$RUST_VERSION" ]; then\
  echo "* Requested Rust Compiler Version:" $RUST_VERSION ;\
  echo "* Install Rust Compiler requested Version ..." ;\
  ${HOME}/.cargo/bin/rustup install $RUST_VERSION ;\
  ${HOME}/.cargo/bin/rustup default $RUST_VERSION ;\
	${HOME}/.cargo/bin/rustup toolchain uninstall stable ;\
  echo "* Rust Compiler Version:" && ${HOME}/.cargo/bin/rustc --version ;\
  echo "* RustUp Show:" && ${HOME}/.cargo/bin/rustup show ;\
  fi

WORKDIR /home/rust-build/project/
