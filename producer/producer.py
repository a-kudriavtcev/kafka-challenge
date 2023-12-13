import asyncio
import json
from aiokafka import AIOKafkaProducer
from pydantic import ValidationError

from models import WikiUpdate
from helpers import read_csv, validate_data


async def produce_message(producer, topic, key, message):
    """Produce a single message."""
    await producer.send_and_wait(topic, key=key, value=json.dumps(message).encode('utf8'))


async def main():
    # Kafka broker configuration
    print("EXECUTING")
    kafka_config = {
        'bootstrap_servers': 'kafka:9092',  # Replace with your Kafka bootstrap servers
    }

    # Kafka topic
    kafka_topic = 'WikiUpdates3'  # Replace with your Kafka topic

    # Create an asynchronous Kafka producer instance
    producer = AIOKafkaProducer(**kafka_config)
    await producer.start()
    # i = 0

    try:
        for wiki_update in read_csv('wiki_updates.csv'):
            # i += 1
            # print("NUMBER OF EVENTS", i)

            await produce_message(
                producer,
                kafka_topic,
                None,
                validate_data(model=WikiUpdate, data=wiki_update).model_dump(),
            )
            # await asyncio.sleep(random.uniform(0, 1))
    finally:
        await producer.stop()


if __name__ == '__main__':
    asyncio.run(main())
