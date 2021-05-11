riot-file import usedCarsCA.csv --header --process location="#geo(lon,lat)" --skip-limit 1 hset --keyspace usedCar --keys id
gunicorn --chdir ./demo --workers 4 --threads 2 -b 0.0.0.0:5000 'demo.app:app'
gunicorn --workers 4 --threads 2 -b 0.0.0.0:5000 'demo.app:app'