from flask import Flask
from faker import Faker
import random
app = Flask(__name__)

def createFakeUpdate():
    update_object = {
        "name": Faker().name(),
        "version": Faker().name(),
        "info": Faker().name(),
        "url": "https://example.com",
        "property_files": [
            {
                "filename": Faker().name(),
                "offset": random.randint(1, 10000),
                "size": random.randint(1, 100000)
            },
            {
                "filename": Faker().name(),
                "offset": random.randint(1, 10000),
                "size": random.randint(1, 100000)
            },
            {
                "filename": Faker().name(),
                "offset": random.randint(1, 10000),
                "size": random.randint(1, 100000)
            },
            {
                "filename": Faker().name(),
                "offset": random.randint(1, 10000),
                "size": random.randint(1, 100000)
            }
        ]
    }
    return update_object

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def hello(path):
    return createFakeUpdate()