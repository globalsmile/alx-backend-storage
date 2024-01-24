#!/usr/bin/env python3
""" log stats """
from pymongo import MongoClient


if __name__ == "__main__":
    """ provides some stats about Nginx logs stored in MongoDB """
    client = MongoClient('mongodb://127.0.0.1:27017')
    logs_collection = client.logs.nginx
    print("{} logs".format(logs_collection.count_documents({})))
    print("Methods:")
    print("\tmethod GET: {}".format(
        logs_collection.count_documents({"method": "GET"})))
    print("\tmethod POST: {}".format(
        logs_collection.count_documents({"method": "POST"})))
    print("\tmethod PUT: {}".format(
        logs_collection.count_documents({"method": "PUT"})))
    print("\tmethod PATCH: {}".format(
        logs_collection.count_documents({"method": "PATCH"})))
    print("\tmethod DELETE: {}".format(
        logs_collection.count_documents({"method": "DELETE"})))
    print("{} status check".format(
        logs_collection.count_documents({"method": "GET", "path": "/status"})))
    print("IPs:")
    pipeline = [
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]
    ips = logs_collection.aggregate(pipeline)
    for ip in ips:
        print("\t{}: {}".format(ip.get("_id"), ip.get("count")))