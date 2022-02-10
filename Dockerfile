FROM python:3
WORKDIR /tmp
COPY requirements.txt .
RUN pip install gunicorn
RUN pip install -r requirements.txt

WORKDIR /app
COPY main.py .
ENV TANK_API=
ENV IDS=
ENV LAT=
ENV LNG=
ENV RAD=
EXPOSE 80

CMD ["gunicorn", "--bind", "0.0.0.0:80", "main:app", "-w", "1", "--threads", "1"]