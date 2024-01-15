FROM debian

ENV TINI_VERSION v0.19.0

ADD https://github.com/tsl0922/ttyd/releases/download/1.7.3/ttyd.x86_64 /bin/ttyd
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /sbin/tini

RUN chmod 755 /sbin/tini /bin/ttyd

RUN apt update && \
    apt install -y vim less sudo cron && \
    apt clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

ARG USER_1="guest"
ARG USER_2="alice"
ARG USER_3="bob"
ARG USER_4="carol"

ARG LEVEL_1_FLAG="<fill flag here>"
ARG LEVEL_2_FLAG="<fill flag here>"
ARG LEVEL_3_FLAG="<fill flag here>"
ARG LEVEL_4_FLAG="<fill flag here>"
ARG LEVEL_5_FLAG="<fill flag here>"
ARG LEVEL_6_FLAG="<fill flag here>"

ADD config/sudoers /etc/sudoers

RUN useradd -mk /etc/skel/ "${USER_1}"
RUN useradd -mk /etc/skel/ "${USER_2}"
RUN useradd -mk /etc/skel/ "${USER_3}"
RUN useradd -mk /etc/skel/ "${USER_4}"

COPY config/.bashrc /home/${USER_1}/.bashrc

RUN chmod 644 /home/${USER_1}/.bashrc && \
    chown ${USER_1} /home/${USER_1}/.bashrc && \
    chgrp ${USER_1} /home/${USER_1}/.bashrc

RUN mkdir /usr/rbin && \
    ln -s /usr/bin/ls /usr/rbin/ls && \
    ln -s /usr/bin/mv /usr/rbin/mv && \
    ln -s /usr/bin/cp /usr/rbin/cp && \
    chmod 777 /usr/rbin

# Level 1
USER ${USER_1}
RUN echo "${LEVEL_1_FLAG}" > /home/${USER_1}/level1.txt && \
    chmod 640 /home/${USER_1}/level1.txt

# Level 2
USER ${USER_1}
RUN echo "${LEVEL_2_FLAG}" > /home/${USER_1}/level2.txt && \
    chmod 000 /home/${USER_1}/level2.txt

# Level 3
USER ${USER_2}
RUN echo "${LEVEL_3_FLAG}" > /home/${USER_2}/level3.txt && \
    chmod 400 /home/${USER_2}/level3.txt && \
    echo "ls" > /home/${USER_2}/.bash_history && \
    echo "echo \"${LEVEL_3_FLAG}\" > level3.txt" >> /home/${USER_2}/.bash_history && \
    echo "exit" >> /home/${USER_2}/.bash_history && \
    chmod 644 /home/${USER_2}/.bash_history

# Level 4
USER ${USER_3}
RUN echo "${LEVEL_4_FLAG}" > /home/${USER_3}/level4.txt && \
    chmod 400 /home/${USER_3}/level4.txt

# Level 5
USER ${USER_4}
RUN echo "${LEVEL_5_FLAG}" > /home/${USER_4}/level5.txt && \
    chmod 400 /home/${USER_4}/level5.txt

# Level 6
USER root
RUN echo "${LEVEL_6_FLAG}" > /root/extra_credit.txt

ADD config/backup-cron /etc/cron.d/backup-cron
ADD config/backup.sh /usr/share/backup-script/backup.sh

RUN mkdir /root/backups && \
    chmod 544 /etc/cron.d/backup-cron && \
    chmod 777 /usr/share/backup-script && \
    chmod 755 /usr/share/backup-script/backup.sh && \
    crontab /etc/cron.d/backup-cron

USER root
ADD config/init.sh /usr/sbin/init.sh
RUN chmod +x /usr/sbin/init.sh

RUN ln -s /usr/bin/sudo /usr/rbin/sudo

WORKDIR /home/${USER_1}

EXPOSE 80
ENTRYPOINT ["/sbin/tini", "--", "/usr/sbin/init.sh"]

CMD [ "/bin/ttyd", "-p", "80", "-t", "titleFixed=CSCI 3403: Lab 2", "-t", "rendererType=webgl", "-t", "disableLeaveAlert=true", "/bin/rbash" ]