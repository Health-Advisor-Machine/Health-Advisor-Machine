FROM python:3.8-slim-buster

# Install Java
RUN apt-get update && apt-get install -y default-jdk

# Install Kafka
ENV KAFKA_HOME=/opt/kafka
RUN mkdir -p $KAFKA_HOME && \
    curl -sSL https://downloads.apache.org/kafka/2.8.1/kafka_2.12-2.8.1.tgz | tar xz --strip 1 -C $KAFKA_HOME

# Install Spark
ENV SPARK_HOME=/opt/spark
RUN mkdir -p $SPARK_HOME && \
    curl -sSL https://downloads.apache.org/spark/spark-3.1.2/spark-3.1.2-bin-hadoop3.2.tgz | tar xz --strip 1 -C $SPARK_HOME

# Install Python dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

# Copy the application code to the image
COPY . /app

# Set the working directory
WORKDIR /app

# Expose the Flask, Kafka application port
EXPOSE 5000
EXPOSE 2181 9092

# Start the application
ENTRYPOINT ["/bin/sh", "/app/start.sh"]
CMD ["sh", "/app/start.sh"]
