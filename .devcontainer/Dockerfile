# Use an alpine base image smaller than ubuntu
FROM alpine:3.20

# Install necessary packages and tools
RUN apk add --no-cache bash curl git unzip nano make musl-utils musl-locales tzdata openssh python3 py3-pip && \ 
    python3 -m venv /venv && \
    . /venv/bin/activate  && \
    python3 /workspaces/cointtracker/mybtcwallet/seed.py




# Set the default shell to bash
ENV SHELL /bin/bash

# Set shell as bash
SHELL ["/bin/bash", "-c"]

RUN ln -s /usr/share/zoneinfo/America/Phoenix /etc/localtime

RUN rm -r /usr/share/zoneinfo/Africa && \
    rm -r /usr/share/zoneinfo/Antarctica && \
    rm -r /usr/share/zoneinfo/Arctic && \
    rm -r /usr/share/zoneinfo/Asia && \
    rm -r /usr/share/zoneinfo/Atlantic && \
    rm -r /usr/share/zoneinfo/Australia && \
    rm -r /usr/share/zoneinfo/Europe  && \
    rm -r /usr/share/zoneinfo/Indian && \
    rm -r /usr/share/zoneinfo/Mexico && \
    rm -r /usr/share/zoneinfo/Pacific && \
    rm -r /usr/share/zoneinfo/Chile && \
    rm -r /usr/share/zoneinfo/Canada

ENV TZ America/Phoenix

ENV LANG=en_US.UTF-8 \
    LANGUAGE=en_US:en \
    LC_ALL=en_US.UTF-8

# Verify locale settings
# locale configuration is important to make bash 
# work properly with newlines and such
RUN locale -a && echo "Locale setup completed."

# Run arch specificexpectations for specific arch (x86_64, arm64, aarch64)
COPY ./arch_spec_install_script.sh /scripts/

RUN chmod +x /scripts/arch_spec_install_script.sh

# installing oh my bash - https://github.com/ohmybash/oh-my-bash
RUN curl -fsSL https://raw.githubusercontent.com/ohmybash/oh-my-bash/master/tools/install.sh | bash

# customize the bash shell ans set vscode theme
RUN sed -i 's/^OSH_THEME=.*/OSH_THEME="vscode"/' ~/.bashrc

RUN /scripts/arch_spec_install_script.sh

RUN apk add docker-cli
