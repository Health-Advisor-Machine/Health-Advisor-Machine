# Base image, openjdk:8-jdk-alpine is an official Docker image from Docker Hub that
# provides a lightweight Linux distribution (Alpine Linux) with OpenJDK 8 (Java Development Kit)
FROM openjdk:8-jdk-alpine

# Install required packages
# --update is an option that tells apk to update the package index before installing packages.
# wget, tar, and bash are required for downloading and extracting Kafka, Spark
RUN apk add --update wget tar bash python3 python3-dev build-base

# Set the working directory
WORKDIR /app

# Download and install Kafka
ENV KAFKA_VERSION=2.8.0
ENV SCALA_VERSION=2.13
RUN wget https://downloads.apache.org/kafka/${KAFKA_VERSION}/kafka_${SCALA_VERSION}-${KAFKA_VERSION}.tgz && \
    tar -xzf kafka_${SCALA_VERSION}-${KAFKA_VERSION}.tgz && \
    mv kafka_${SCALA_VERSION}-${KAFKA_VERSION} /opt/kafka && \
    rm kafka_${SCALA_VERSION}-${KAFKA_VERSION}.tgz

# Copy the Kafka configuration files
COPY kafka_config/zookeeper.properties /opt/homebrew/etc/kafka/zookeeper.properties
COPY kafka_config/server.properties /opt/homebrew/etc/kafka/server.properties

# Copy the Flask application code
COPY app.py /app/

# Copy the requirements file and install dependencies
COPY requirements.txt /app/
RUN pip3 install -r requirements.txt

# Expose the Flask, Kafka application port
EXPOSE 5000
EXPOSE 2181 9092

# Start app shell scripts
COPY start-app.sh /app/
CMD ["sh", "/app/start-app.sh"]
