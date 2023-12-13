import asyncio
import json
import random
from aiokafka import AIOKafkaProducer
from pydantic import ValidationError

from models import WikiUpdate
from helpers import read_csv, validate_data

KAFKA_CONFIG = {
    'bootstrap_servers': 'kafka:9092',
}
KAFKA_TOPIC = 'WikiUpdates'


async def produce_message(producer, topic, key, message):
    await producer.send_and_wait(topic, key=key, value=json.dumps(message).encode('utf8'))


async def main():
    producer = AIOKafkaProducer(**KAFKA_CONFIG)
    await producer.start()

    for wiki_update in read_csv('wiki_updates.csv'):
        try:
            validated_data = validate_data(model=WikiUpdate, data=wiki_update).model_dump()
        except ValidationError:
            print("Invalid data")
            continue

        await produce_message(
            producer,
            KAFKA_TOPIC,
            None,
            validated_data,
        )
        await asyncio.sleep(random.uniform(0, 1))

    await producer.stop()


if __name__ == '__main__':
    asyncio.run(main())
