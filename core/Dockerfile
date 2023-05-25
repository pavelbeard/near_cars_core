FROM python:3.11.0-slim-bullseye as builder

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .

RUN python3.11 -m venv /opt/venv; apt update; apt install gcc build-essential -y

ENV PATH=/opt/venv/bin:$PATH

RUN pip3.11 install $(grep -ivE "pywin32" requirements.txt)

# FINAL #
FROM python:3.11.0-slim-bullseye

RUN mkdir -p /home/core_app; \
        addgroup --system core_app; \
        adduser --system core_app; \
        usermod -aG core_app core_app

COPY --from=builder /opt/venv /opt/venv
ENV PATH=/opt/venv/bin:$PATH

ENV APP_HOME=/home/core_app
RUN apt update; apt install curl net-tools netcat-openbsd -y; \
        mkdir $APP_HOME; mkdir $APP_HOME/logs; mkdir $APP_HOME/staticfiles

WORKDIR $APP_HOME

COPY . $APP_HOME

RUN chown -R core_app:core_app $APP_HOME; chmod u+rwx -R $APP_HOME
USER core_app

EXPOSE 8000
