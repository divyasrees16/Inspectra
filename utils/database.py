# utils/database.py

from influxdb import InfluxDBClient
from datetime import datetime, timezone
import uuid


def write_to_influx_v1(json_data):

    client = InfluxDBClient(host='localhost', port=8086)
    client.switch_database('defects')

    # UTC timestamp in nanoseconds
    dt_utc = datetime.now(timezone.utc)
    timestamp = int(dt_utc.timestamp() * 1e9)

    model_type = json_data["model_info"]["type"]
    defect_types = json_data["summary"]["defect_types"]

    image_id = str(uuid.uuid4())
    total_defects = json_data["summary"]["total_defects"]

    point = {
        "measurement": "defect_counts",
        "tags": {
            "image_id": image_id,
            "model": model_type
        },
        "time": timestamp,
        "fields": {
            "total_defects": total_defects
        }
    }

    for class_name in [
        'crease', 'crescent_gap', 'inclusion', 'oil_spot',
        'punching_hole', 'rolled_pit', 'silk_spot',
        'waist_folding', 'water_spot', 'welding_line'
    ]:
        point["fields"][class_name] = defect_types.get(class_name, 0)

    client.write_points([point])