
FROM python:3.10-slim

WORKDIR ${HOME}

ENV FLASK_APP=app.py

RUN apt-get update -y  \
    && apt-get install -y --no-install-recommends curl \
    && apt-get autoclean && apt-get autoremove \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY requirements.txt .

RUN python3 -m pip install --no-cache -r requirements.txt

COPY . .

ENTRYPOINT ["bash", "entrypoint.sh"]

CMD ["flask", "run", "-h", "0.0.0.0", "-p", "5000"]
