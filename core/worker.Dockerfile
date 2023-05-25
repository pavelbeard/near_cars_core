FROM python:3.11.0-slim-bullseye as builder

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .

RUN python3.11 -m venv /opt/venv; apt update; apt install gcc build-essential -y

ENV PATH=/opt/venv/bin:$PATH

RUN pip3.11 install $(grep -ivE "pywin32" requirements.txt)

# FINAL #
FROM python:3.11.0-slim-bullseye

RUN addgroup --system worker; \
        adduser --system worker; \
        usermod -aG worker worker

COPY --from=builder /opt/venv /opt/venv
ENV PATH=/opt/venv/bin:$PATH

ENV APP_HOME=/home/worker

WORKDIR $APP_HOME

COPY . $APP_HOME

RUN chown -R worker:worker $APP_HOME; chmod u+rwx -R $APP_HOME
USER worker
