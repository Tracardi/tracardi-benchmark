FROM python:3.9

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:/app:$PATH"

RUN /opt/venv/bin/python3 -m pip install --upgrade pip

RUN mkdir -p app
WORKDIR /app

COPY requirements.txt .
RUN pip --default-timeout=240 install -r requirements.txt

COPY fake_data_maker ./fake_data_maker
COPY locustfile.py ./locustfile.py
WORKDIR /app

ENTRYPOINT ["locust"]
