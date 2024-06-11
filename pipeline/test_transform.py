from transform import get_botanist_detail
from unittest.mock import patch, MagicMock

@pytest.fixture
def example_data():
    return {
        "botanist": {
            "email": "eliza.andrews@lnhm.co.uk",
            "name": "Eliza Andrews",
            "phone": "(846)669-6651x75948"
        },
        "images": {
            "license": 451,
            "license_name": "CC0 1.0 Universal (CC0 1.0) Public Domain Dedication",
            "license_url": "https://creativecommons.org/publicdomain/zero/1.0/",
            "medium_url": "https://perenual.com/storage/image/upgrade_access.jpg",
            "original_url": "https://perenual.com/storage/image/upgrade_access.jpg",
            "regular_url": "https://perenual.com/storage/image/upgrade_access.jpg",
            "small_url": "https://perenual.com/storage/image/upgrade_access.jpg",
            "thumbnail": "https://perenual.com/storage/image/upgrade_access.jpg"
        },
        "last_watered": "Mon, 10 Jun 2024 13:23:01 GMT",
        "name": "Bird of paradise",
        "origin_location": [
            "5.27247",
            "-3.59625",
            "Bonoua",
            "CI",
            "Africa/Abidjan"
        ],
        "plant_id": 8,
        "recording_taken": "2024-06-11 13:00:09",
        "scientific_name": [
            "Heliconia schiedeana 'Fire and Ice'"
        ],
        "soil_moisture": 15.478956774353875,
        "temperature": 11.483367104821191
    }
