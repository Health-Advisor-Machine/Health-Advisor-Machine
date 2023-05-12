FROM python:3.8-slim-bullseye

RUN apt-get update && apt-get install -y curl

# Install Java
RUN apt-get update && apt-get install -y default-jdk

# Install Kafka
ENV KAFKA_HOME=/opt/kafka
RUN mkdir -p $KAFKA_HOME && \
    curl -sSL https://downloads.apache.org/kafka/3.4.0/kafka_2.12-3.4.0.tgz | tar xz --strip 1 -C $KAFKA_HOME

# Install Spark
ENV SPARK_HOME=/opt/spark
RUN mkdir -p $SPARK_HOME && \
    curl -sSL https://dlcdn.apache.org/spark/spark-3.4.0/spark-3.4.0-bin-hadoop3.tgz | tar xz --strip 1 -C $SPARK_HOME

RUN apt-get update && apt-get install -y build-essential

# Install Python dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt
RUN pip install kafka-python

# Copy the application code to the image
COPY . /app

# Set the working directory
WORKDIR /app

# Expose the Flask, Kafka application port
EXPOSE 5000
EXPOSE 2181 9092

# Start the application
ENTRYPOINT ["/bin/sh", "/app/docker.sh"]
CMD ["sh", "/app/docker.sh"]
