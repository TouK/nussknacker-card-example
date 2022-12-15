FROM python:3.10

WORKDIR /app
ADD requirements.txt .
RUN pip install -r requirements.txt \
    && rm -rf /root/.cache
COPY . .
CMD ["python", "generate.py"]
