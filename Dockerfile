FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && rm -rf /usr/local/lib/python3.13/site-packages/pip \
                  /usr/local/lib/python3.13/site-packages/pip-*.dist-info \
                  /usr/local/bin/pip*

COPY . .

ENV PYTHONPATH=/app/src
ENV FLASK_APP=company_website

EXPOSE 7000

CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:7000", "--access-logfile", "-", "wsgi:app"]
