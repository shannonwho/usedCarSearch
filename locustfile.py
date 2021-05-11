from locust import HttpUser, User, TaskSet, task, web, runners, between, tag
# from locust.runners import MasterLocustRunner
from locust.contrib.fasthttp import FastHttpUser
from locust.stats import sort_stats
from locust.util.rounding import proper_round
# import json
from itertools import chain
try:
    # >= Py3.2
    from html import escape
except ImportError:
    # < Py3.2
    from cgi import escape
import simplejson as json
import os
import random
import string
import requests
# from rejson import Client, Path
# from demo.utils.sampleJSON import smallObj,bigObj,hugeObj
from faker import Faker
from faker.providers import company
from flask import jsonify
from flask import request,Response
from datetime import time
from datetime import datetime
from datetime import timedelta
from datetime import date
import enum
import uuid

#pull values from env vars
environment = os.environ['ENV']
# req_timeout_value = int(os.environ['LOAD_GEN_REQUEST_TIMEOUT']) if os.environ['LOAD_GEN_REQUEST_TIMEOUT'] else 50
# api_endpoint = 'http://app:5000/api/v1/'
api_endpoint = os.environ['API_ENDPOINT']
# https://faker.readthedocs.io/en/master/
fake = Faker()
fake.add_provider(company)

# Scrape data into Prometheus
import six
from itertools import chain
from locust import stats as locust_stats, runners as locust_runners
from locust import User, task, events
from prometheus_client import Metric, REGISTRY, exposition

"""Functions for tasks to be used in the Task set"""

# def get_id(pattern):
#     #use scan on the key level 
#     try:
#         resp = requests.get(api_endpoint + 'keys?pattern=' + pattern, verify=False)
#         r = resp.json()
#         keys = r.get('json')
#         return keys
#     except Exception as e:
#         return {'error':str(e)}

fields = ['type','feul','manufacturer','region', 'year']
randomType = ['SUV', "truck", "sedan", "convertible"]
manufacturer = ['acura', 'alfa-romeo', 'aston-martin', 'audi']
fuel = ['gas', 'electric']


""" Build the TaskSet """
class testOnSimpleSearch(TaskSet):
    @tag('searchByType')
    #@task(3)
    def searchByType(self):
        self.client.get('/api/post/{}/{}'.format("type", random.choice(randomType)),timeout=50, name='/api/v1/searchByType')

    @tag('searchByManufacturer')
    @task(3)
    def searchByManufacturer(self):
        self.client.get('/api/post/{}/{}'.format("manufacturer", random.choice(manufacturer)),timeout=50, name='/api/searchByManufacturer')

    # @tag('aggregation')
    # @task(3)
    # def aggregation(self):
    #     self.client.post('/api/v1/redisjson',
    #         data=json_doc,
    #         headers={'Content-Type': 'application/json'},
    #         timeout=50,
    #         name='/api/v1/aggregation')


""" Generate the load """

class GenerateLoad(FastHttpUser):
    # connection_timeout=100
    # network_timeout=50
    tasks = [testOnSimpleSearch]
    # min_wait = 5000
    # max_wait = 20000

