#!/usr/bin/env python3
"""Log stats"""
from pymongo import MongoClient


def helper(a: dict) -> int:
    """return log"""
    client = MongoClient('mongodb://127.0.0.1:27017')
    logs = client.logs.nginx
    return logs.count_documents(a)


def main():
    """ provides some stats about Nginx logs stored in MongoDB """
    print(f"{helper({})} logs")
    print("Methods:")
    print(f"\tmethod GET: {helper({'method': 'GET'})}")
    print(f"\tmethod POST: {helper({'method': 'POST'})}")
    print(f"\tmethod PUT: {helper({'method': 'PUT'})}")
    print(f"\tmethod PATCH: {helper({'method': 'PATCH'})}")
    print(f"\tmethod DELETE: {helper({'method': 'DELETE'})}")
    print(f"{helper({'method': 'GET', 'path': '/status'})} status check")
    print("IPs:")
    pipeline = [
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]
    for i in client.logs.nginx.aggregate(pipeline):
        print(f"\t{i.get('_id')}: {i.get('count')}")



if __name__ == "__main__":
    main()
