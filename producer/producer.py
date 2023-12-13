import asyncio
import json
import random
from aiokafka import AIOKafkaProducer
from pydantic import ValidationError

from models import WikiUpdate
from helpers import read_csv, validate_data


async def produce_message(producer, topic, key, message):
    """Produce a single message."""
    await producer.send_and_wait(topic, key=key, value=json.dumps(message).encode('utf8'))


async def main():
    kafka_config = {
        'bootstrap_servers': 'kafka:9092',
    }
    kafka_topic = 'WikiUpdates3'

    producer = AIOKafkaProducer(**kafka_config)
    await producer.start()

    try:
        for wiki_update in read_csv('wiki_updates.csv'):
            await produce_message(
                producer,
                kafka_topic,
                None,
                validate_data(model=WikiUpdate, data=wiki_update).model_dump(),
            )
            await asyncio.sleep(random.uniform(0, 1))
    finally:
        await producer.stop()


if __name__ == '__main__':
    asyncio.run(main())
