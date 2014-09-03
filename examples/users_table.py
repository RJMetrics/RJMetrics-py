#!/usr/bin/env python

import rjmetrics.client

CLIENT_ID = 0000
API_KEY = 'your_api_key'

client = rjmetrics.client.Client(CLIENT_ID, API_KEY)

# let's define some fake users
fake_users = [
  {"id": 1, "email": "joe@schmo.com", "acquisition_source": "PPC"},
  {"id": 2, "email": "mike@smith.com", "acquisition_source": "PPC"},
  {"id": 3, "email": "lorem@ipsum.com", "acquisition_source": "Referral"},
  {"id": 4, "email": "george@vandelay.com", "acquisition_source": "Organic"},
  {"id": 5, "email": "larry@google.com", "acquisition_source": "Organic"}
]


def sync_user(client, user):
  # `id` is the unique key here, since each user should only
  # have one record in this table
  user["keys"] = ["id"]
  # table named "users"
  return client.push_data("users", [user])[0]


# make sure the client is authenticated before we do anything
if client.authenticate():
  for user in fake_users:
    # iterate through users and push data
    response = sync_user(client, user)
    if response.ok:
        print "Synced user with id ", user["id"]
    else:
        print "Failed to sync user with id ", user["id"]
