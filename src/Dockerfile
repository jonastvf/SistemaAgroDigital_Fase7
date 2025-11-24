FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /code

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        build-essential \
        curl \
        r-base \
    && R -e "install.packages(c('dplyr', 'jsonlite'), repos='https://cran.r-project.org')" \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /tmp/requirements.txt
RUN pip install --upgrade pip && pip install -r /tmp/requirements.txt

COPY app/ /code/app/

EXPOSE 5000

CMD ["bash", "-c", "python /code/app/ml/fase5_generate.py && python -m flask run --host=0.0.0.0 --port=5000"]
