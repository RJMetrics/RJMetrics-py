#!/usr/bin/env python

import rjmetrics.client

CLIENT_ID = 0000
API_KEY = 'your_api_key'

client = rjmetrics.client.Client(CLIENT_ID, API_KEY)

fake_orders = [
  {"id": 1, "user_id": 1, "value": 58.40,  "sku": "milky-white-suede-shoes"},
  {"id": 2, "user_id": 1, "value": 23.99,  "sku": "red-button-down-fleece"},
  {"id": 3, "user_id": 2, "value": 5.00,   "sku": "bottle-o-bubbles"},
  {"id": 4, "user_id": 3, "value": 120.01, "sku": "zebra-striped-game-boy"},
  {"id": 5, "user_id": 5, "value": 9.90,   "sku": "kitten-mittons"}
]


def sync_order(client, order):
  order["keys"] = ["id"]
  return client.push_data("orders", [order])[0]


# make sure the client is authenticated before we do anything
if client.authenticate():
  for order in fake_orders:
    # iterate through users and push data
    response = sync_order(client, order)
    if response.ok:
        print "Synced order with id ", order["id"]
    else:
        print "Failed to sync order with id ", order["id"]
