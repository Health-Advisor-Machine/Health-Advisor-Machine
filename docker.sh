
#!/bin/bash

/opt/kafka/bin/zookeeper-server-start.sh /opt/kafka/config/zookeeper.properties &
/opt/kafka/bin/kafka-server-start.sh /opt/kafka/config/server.properties &

sleep 10 &

/opt/kafka/bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic test &
/opt/kafka/bin/kafka-console-producer.sh --broker-list localhost:9092 --topic test &
/opt/kafka/bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic test &

python3 app.py
