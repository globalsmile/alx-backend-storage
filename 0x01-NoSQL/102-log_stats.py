"""
Improve 12-log_stats.py by adding the top 10 of the most present IPs in the collection nginx of the database logs:

The IPs top must be sorted (like the example below)

94778 logs
Methods:
    method GET: 93842
    method POST: 229
    method PUT: 0
    method PATCH: 0
    method DELETE: 0
47415 status check
IPs:
    172.31.63.67: 15805
    172.31.2.14: 15805
    172.31.29.194: 15805
    69.162.124.230: 529
    64.124.26.109: 408
    64.62.224.29: 217
    34.207.121.61: 183
    47.88.100.4: 166
    45.249.84.250: 160
    216.244.66.228: 150
    """
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
    client = MongoClient('mongodb://127.0.0.1:27017')
    logs = client.logs.nginx
    ips = logs.aggregate(pipeline)
    for ip in ips:
        print(f"\t{ip.get('_id')}: {ip.get('count')}")
    logs.close()


if __name__ == "__main__":
    main()
