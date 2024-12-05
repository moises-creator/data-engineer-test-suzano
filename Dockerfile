FROM quay.io/astronomer/astro-runtime:12.5.0

USER root

RUN pip install --no-cache-dir selenium requests

USER astro
