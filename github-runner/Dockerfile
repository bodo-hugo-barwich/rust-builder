FROM ubuntu:24.04

ARG UID=1000
ARG GID=1000

RUN apt-get update\
	&& apt-get -y install sudo\
	&& apt-get -y install git cpanminus python3-yaml python3-git

RUN group_name=`getent group ${GID}` || true ;\
	echo "Group (${GID}): '$group_name'";\
	if [ -n "$group_name" ]; then group_name=`echo "$group_name" | cut -d: -f1`; groupmod -n github $group_name; else groupadd -g ${GID} github; fi;\
	user_name=`getent passwd ${UID}` || true ;\
	echo "User (${UID}): '$user_name'";\
	if [ -n "$user_name" ]; then user_name=`echo "$user_name" | cut -d: -f1`; usermod -l runner -c "GitHub Runner" $user_name; mv /home/$user_name /home/runner; else useradd runner -u ${UID} -g github -md /home/runner; fi;

USER runner

RUN mkdir -p /home/runner/project/ \
  && mkdir -p /home/runner/log

WORKDIR /home/runner/project/
