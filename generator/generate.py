import itertools
import json
import os
import time
from datetime import datetime
from random import randrange
from uuid import uuid4

from confluent_kafka import Producer
from confluent_kafka.serialization import StringSerializer, SerializationContext, MessageField
from confluent_kafka.schema_registry import SchemaRegistryClient, RegisteredSchema
from confluent_kafka.schema_registry.json_schema import JSONSerializer


class MessageProducer:
    def __init__(self, topic_name):
        self.topic = topic_name
        schema_registry_url = os.getenv("SCHEMA_REGISTRY_URL", "http://localhost:3082")
        kafka_servers = os.getenv("KAFKA_ADDRESS", "localhost:3032")

        schema_registry_conf = {'url': schema_registry_url}
        schema_registry_client = SchemaRegistryClient(schema_registry_conf)

        schema: RegisteredSchema = schema_registry_client.get_latest_version(f"{topic}-value")
        to_edit = json.loads(schema.schema.schema_str)
        to_edit["title"] = "Stub"

        self.string_serializer = StringSerializer('utf_8')
        self.json_serializer = JSONSerializer(json.dumps(to_edit), schema_registry_client)

        self.producer = Producer({'bootstrap.servers': kafka_servers})

    @staticmethod
    def delivery_report(err, ctx):
        if err:
            print(f"Failed with {err} {ctx}")

    def send(self, obj, timestamp):
        self.producer.produce(topic=self.topic,
                              timestamp=timestamp,
                              key=self.string_serializer(str(uuid4()), SerializationContext(topic, MessageField.KEY)),
                              value=self.json_serializer(obj, SerializationContext(topic, MessageField.VALUE)),
                              on_delivery=self.delivery_report)

    def flush(self):
        self.producer.flush()


topic = "cain.001"

producer = MessageProducer(topic)


def send(timestamp: datetime,
         customer_id: str,
         postal_code: str,
         acquirer_id: str,
         amount: int,
         lat: float,
         lon: float,
         verification_modes,
         ecommerce: bool):
    producer.send({"Document": {
        "Header": {
            "MessageFunction": "REQU",
            "CreationDateTime": timestamp.isoformat(),
            "ProtocolVersion": "1",
            "InitiatingParty": {
                "Identification": "txt"
            }
        },
        "Body": {
            "Environment": {
                "Acquirer": {
                    "Identification": acquirer_id
                },
                "Card": {
                    "PAN": "42228888{random}777123".format(random=randrange(10000, 90000))
                },
                "Payer": {
                    "Customer": {
                        "CustomerIdentification": customer_id,
                        "Address": {
                            "Country": "PL",
                            "TownName": "Warsaw",
                            "PostalCode": postal_code
                        }
                    }
                },
                "CustomerDevice": {
                    "Device": {
                        "Type": "SECR",
                        "Location": {
                            "Latitude": str(lat),
                            "Longitude": str(lon)
                        }
                    }
                }
            },
            "Context": {
                "PointOfServiceContext": {
                    "CardDataEntryMode": "MGST",
                    "ECommerceIndicator": ecommerce
                },
                "TransactionContext": {
                    "MerchantCategoryCode": "1234"
                },
                "Verification": [{"Type": x} for x in verification_modes]
            },
            "Transaction": {
                "TransactionType": "AB",
                "TransactionIdentification": {
                    "LocalDateTime": timestamp.isoformat(),
                    "SystemTraceAuditNumber": "1234",
                    "RetrievalReferenceNumber": "123456789012",
                    "TransactionReference": str(uuid4())[:30]
                },
                "AccountTo": {
                    "AccountIdentification": "433434"
                },
                "TransactionAmounts": {
                    "TransactionAmount": {
                        "Amount": {
                            "amount": amount,
                            "currency": "PLN"
                        },
                        "Currency": "985"
                    }
                },
            }
        }
    }}, int(timestamp.timestamp() * 1000))


codes: list[str] = open("./codes.csv").readlines()

for count in itertools.count(1):
    if count % 100 == 0:
        print("{count} messages sent, flushing".format(count=count))
        producer.flush()

    customer = randrange(0, 500)
    code = codes[customer % len(codes)].replace("\n", "")
    verification_modes: list[list[str]] = [
        ["NPIN"],
        ["NPIN", "CRYP"],
        ["CRYP"],
        ["FPIN"],
        ["FPIN", "CRYP"],
        []
    ]
    send(datetime.now(),
         customer_id="id-{id}".format(id=customer),
         postal_code=code,
         acquirer_id="acqu" + str(randrange(20)),
         amount=randrange(20, 30),
         lat=50 + randrange(-100, 100) / 100,
         lon=20 + randrange(-200, 200) / 100,
         verification_modes=verification_modes[randrange(0, len(verification_modes))],
         ecommerce=randrange(5) > 2)
    time.sleep(0.01)

producer.flush()
