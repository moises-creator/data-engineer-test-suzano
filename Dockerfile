FROM quay.io/astronomer/astro-runtime:12.5.0  

USER root  

RUN pip install --no-cache-dir selenium requests  

COPY . /usr/local/airflow  
WORKDIR /usr/local/airflow  

RUN pip install --no-cache-dir -r requirements.txt  

USER astro  

CMD ["astro", "dev", "start"]