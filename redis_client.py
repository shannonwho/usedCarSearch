import redis
import config
from redisearch import AutoCompleter, Suggestion, Client, Query, aggregation, reducers, IndexDefinition, TextField, NumericField, TagField, GeoFilter
import os 
# Connection Pooling 
connection = Client('usedCarIdx',host='redis-10959.c253.us-central1-1.gce.cloud.redislabs.com', port=os.environ['REDIS_PORT'], password=os.environ['REDIS_PASSWORD'], decode_responses=True, health_check_interval=30)
