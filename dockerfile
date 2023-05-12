# Base image
FROM openjdk:8-jdk-slim

# Install Python and Flask dependencies
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    pip3 install flask

# Install required packages
RUN apk add --update wget tar bash python3 python3-dev build-base

# Set the working directory
WORKDIR /app

# Install Spark and Kafka
ENV SPARK_VERSION 3.1.1
ENV HADOOP_VERSION 3.2
RUN curl -L https://downloads.apache.org/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz | tar -xvz -C /opt && \
    mv /opt/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION} /opt/spark
ENV PATH $PATH:/opt/spark/bin
ENV PYTHONPATH $PYTHONPATH:/opt/spark/python/lib/py4j-0.10.9-src.zip:/opt/spark/python/

ENV KAFKA_VERSION 2.8.0
RUN curl -L https://downloads.apache.org/kafka/${KAFKA_VERSION}/kafka_2.13-${KAFKA_VERSION}.tgz | tar -xvz -C /opt && \
    mv /opt/kafka_2.13-${KAFKA_VERSION} /opt/kafka
ENV PATH $PATH:/opt/kafka/bin

# Install ZooKeeper
ENV ZOOKEEPER_VERSION 3.7.0
RUN curl -L https://downloads.apache.org/zookeeper/zookeeper-${ZOOKEEPER_VERSION}/apache-zookeeper-${ZOOKEEPER_VERSION}-bin.tar.gz | tar -xvz -C /opt && \
    mv /opt/apache-zookeeper-${ZOOKEEPER_VERSION}-bin /opt/zookeeper
ENV PATH $PATH:/opt/zookeeper/bin


# Copy the Kafka configuration files
COPY kafka_config/zookeeper.properties /opt/kafka/zookeeper.properties
COPY kafka_config/server.properties /opt/kafka/server.properties

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
