import json
import xml.etree.ElementTree as ET
import yaml
import csv
import msgpack
import bson
from avro.datafile import DataFileReader, DataFileWriter
from avro.io import DatumReader, DatumWriter
import fastavro
import hexagon_pb2  # Make sure to have the generated ProtoBuf file

# Example Hexagon Data
hexagon_data = {
    "map_id": 1,
    "hexagon_id": 101,
    "position_relative": [3, 4],
    "position_absolute": [],
    "image_url": "/images/hexagon101.png",
    "hexagon_type": "Jungle",
    "hexagon_size": "Large",
    "hexagon_shape": "Flat",
    "contours": [
        {"type": "lake", "id": "LakeA"},
        {"type": "road", "id": "RoadB"},
        {"type": "border", "id": "BorderC"}
    ],
    "created_at": "2023-01-15T08:30:00Z",
    "updated_at": "2023-02-02T14:45:00Z"
}

# JSON Serialization
json_data = json.dumps(hexagon_data)
json_size = len(json_data)

# XML Serialization
xml_data = ET.Element("hexagon")
for key, value in hexagon_data.items():
    ET.SubElement(xml_data, key).text = str(value)
xml_data = ET.tostring(xml_data)
xml_size = len(xml_data)

# YAML Serialization
yaml_data = yaml.dump(hexagon_data, default_flow_style=False)
yaml_size = len(yaml_data)

# CSV Serialization
csv_data = ",".join(map(str, hexagon_data.values()))
csv_size = len(csv_data)

# ProtoBuf Serialization
protobuf_data = hexagon_pb2.Hexagon()
protobuf_data.map_id = hexagon_data["map_id"]
protobuf_data.hexagon_id = hexagon_data["hexagon_id"]
protobuf_data.position_relative.extend(hexagon_data["position_relative"])
protobuf_data.image_url = hexagon_data["image_url"]
protobuf_data.hexagon_type = hexagon_data["hexagon_type"]
protobuf_data.hexagon_size = hexagon_data["hexagon_size"]
protobuf_data.hexagon_shape = hexagon_data["hexagon_shape"]
for contour in hexagon_data["contours"]:
    protobuf_contour = protobuf_data.contours.add()
    protobuf_contour.type = contour["type"]
    protobuf_contour.id = contour["id"]
protobuf_data.created_at = hexagon_data["created_at"]
protobuf_data.updated_at = hexagon_data["updated_at"]
protobuf_data = protobuf_data.SerializeToString()
protobuf_size = len(protobuf_data)

# MessagePack Serialization
messagepack_data = msgpack.packb(hexagon_data)
messagepack_size = len(messagepack_data)

# BSON Serialization
bson_data = bson.dumps(hexagon_data)
bson_size = len(bson_data)

# Avro Serialization
avro_schema = {
    "type": "record",
    "name": "Hexagon",
    "fields": [
        {"name": "map_id", "type": "int"},
        {"name": "hexagon_id", "type": "int"},
        {"name": "position_relative", "type": {"type": "array", "items": "int"}},
        {"name": "position_absolute", "type": {"type": "array", "items": "int"}},
        {"name": "image_url", "type": "string"},
        {"name": "hexagon_type", "type": "string"},
        {"name": "hexagon_size", "type": "string"},
        {"name": "hexagon_shape", "type": "string"},
        {"name": "contours", "type": {"type": "array", "items": {
            "type": "record",
            "name": "Contour",
            "fields": [
                {"name": "type", "type": "string"},
                {"name": "id", "type": "string"}
            ]
        }}},
        {"name": "created_at", "type": "string"},
        {"name": "updated_at", "type": "string"}
    ]
}
"""
with open("hexagon.avro", "wb") as avro_file:
    fastavro.writer(avro_file, [hexagon_data], avro_schema)
with open("hexagon.avro", "rb") as avro_file:
    avro_size = len(avro_file.read())
"""
# Print Results
print(f"JSON Size: {json_size} bytes")
print(f"XML Size: {xml_size} bytes")
print(f"YAML Size: {yaml_size} bytes")
print(f"CSV Size: {csv_size} bytes")
print(f"ProtoBuf Size: {protobuf_size} bytes")
print(f"MessagePack Size: {messagepack_size} bytes")
print(f"BSON Size: {bson_size} bytes")
# print(f"Avro Size: {avro_size} bytes")
