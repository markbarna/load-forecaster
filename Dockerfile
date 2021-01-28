FROM python:3.8.7-slim-buster

# gcc and python-dev required for installing sagemaker-train package
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc python3-dev nginx ca-certificates \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED=TRUE
ENV PYTHONDONTWRITEBYTECODE=TRUE

# Set up the program in the image
# TODO: Create venv for model code only?
COPY requirements.txt /opt/ml/code/
WORKDIR /opt/ml/code
RUN pip install --no-cache-dir -r requirements.txt

COPY pipeline /opt/ml/code/pipeline/
COPY utils /opt/ml/code/utils/
COPY *.py /opt/ml/code/
COPY nginx.conf /opt/ml/code/

ENTRYPOINT ["python", "entrypoint_handler.py"]
