FROM apache/airflow:2.0.1
COPY requirements.txt /requirements.txt
RUN pip3 install --user --upgrade pip3
RUN pip3 install --no-cache-dir --user -r /requirements.txt