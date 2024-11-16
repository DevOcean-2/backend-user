FROM python:3.12

ARG KAKAO_CLIENT_ID
ARG KAKAO_CLIENT_SECRET
ARG KAKAO_REDIRECT_URI
ARG JWT_SECRET_KEY

ENV KAKAO_CLIENT_ID=${KAKAO_CLIENT_ID} \
    KAKAO_CLIENT_SECRET=${KAKAO_CLIENT_SECRET} \
    KAKAO_REDIRECT_URI=${KAKAO_REDIRECT_URI} \
    JWT_SECRET_KEY=${JWT_SECRET_KEY} \
    PYTHONPATH="/balbalm"

WORKDIR /balbalm

COPY alembic /balbalm/alembic
COPY app /balbalm/app
COPY alembic.ini /balbalm
COPY main.py /balbalm
COPY Makefile /balbalm
COPY requirements.txt /balbalm

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

EXPOSE 8000
EXPOSE 5432

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--log-level", "warning"]