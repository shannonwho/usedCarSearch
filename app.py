from types import LambdaType
from flask import Flask, render_template, request, redirect, render_template, Response
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import Navbar, View
from redisearch import AutoCompleter, Suggestion, Client, Query, aggregation, reducers, IndexDefinition, TextField, NumericField, TagField, GeoFilter
# From our local file
from dataload import load_data
from os import environ
import redis
import json
import string
import geocoder
# import redis_client as rc
# import services



app = Flask(__name__)
bootstrap = Bootstrap(app)
nav = Nav(app)

topbar = Navbar('',
    View('Home', 'index'),
    View('Geo Search', 'geosearch'),
    View('Aggregation', 'show_agg')
)

nav.register_element('top', topbar)


if environ.get('REDIS_SERVER') is not None:
   redis_server = environ.get('REDIS_SERVER')
else:
   redis_server = 'redis-15167.c14210.us-west1-mz.gcp.cloud.rlrcp.com'

if environ.get('REDIS_PORT') is not None:
   redis_port = int(environ.get('REDIS_PORT'))
else:
   redis_port = '15167'

if environ.get('REDIS_PASSWORD') is not None:
   redis_password = environ.get('REDIS_PASSWORD')
else:
   redis_password = 'tp4obFGolrSQGIdywaGe0l0SHOhXWyIQ'

client = Client(
   'usedCarIdx',
   host=redis_server,
   password=redis_password,
   port=redis_port
   )

ac = AutoCompleter(
   'ac',
   conn = client.redis
   )



#Build an location obj for google map in a format as lat: -31.56391, lng: 147.154312
class location:
    def __init__(self, lon=0, lat=0):
        self.lat = lat
        self.lon = lon


""" Services """

def agg_by(field):
   ar = aggregation.AggregateRequest().group_by(field, reducers.count().alias('my_count')).sort_by(aggregation.Desc('@my_count'))
   return (client.aggregate(ar).rows)

def single_attribute_search(field, value):
   # Find the point within certain distance of a specified location
   #parameterize locations
   q = "@" + field + ":" + value
   return (client.search(Query(q)).docs)


def faceted_search(carmodel, startYear, endYear, startPrice, endPrice, color):
   if not startYear and not endYear and not startPrice and not endPrice:
      q = "@manufacturer:" + carmodel
   elif not startYear or not endYear:
      if not startYear:
         startYear = '-inf'
      elif not endYear:
         endYear = '+inf'
      q = "'@manufacturer:" + carmodel + + " @year:[" + startYear + "," + endYear + "]'"
   else:
      if not startPrice and not endPrice: 
         startPrice = '-inf'
         endPrice = '+inf'
      elif not endPrice:
         endPrice = '+inf'
      elif not startPrice:
         startPrice='-inf'
      q = "'@price:[" + startPrice + "," + endPrice + "] " + "@manufacturer:" + carmodel + " @year:[" + startYear + "," + endYear + "]"
   
   if color:
      if len(q)<1:
         q = "@paint_color:" +color
      else:
         q = q + " @paint_color:" + color

   print("faceted_search {}".format(q))

   res = client.search(Query(q).sort_by("price",asc=True).paging(0,25)).docs
   print ("faceted_search - res {} ".format(res))
   return res


def search_location(lon,lat,radius):
   #ft.searc.connection myIdx "@location:[-117.824722 33.685909 2000 m]" RETURN 4 id model manufacturer region LIMIT 0 3
   print("search_location - lon {}, lat {}, redius {}".format(lon,lat,radius))

   q = "@location:[" + lon + "," + lat + "," + radius + ",m]"
   print("location - q {}".format(q))
   # q = Query("").add_filter(GeoFilter('location', -117.824722, 33.68590, 200)).no_content()
   res = client.search(Query(q)).docs
   return (res)


""" VIEWS
Each view path pulls from it's associated template.  The main.html is a parent template 

Javascript files are associated by naming convention: home.html --> home.js
"""

@app.route('/')
def index():
   try:
      idx=client.info()
      print("Info : %", client.info())
      return render_template('search.html')
   except:
      load_data(redis_server, redis_port, redis_password)
      return render_template('search.html')


@app.route('/autocomplete')
def auto_complete():
    name = request.args.get('term')
    suggest = ac.get_suggestions(name, fuzzy = True)
    return(json.dumps([{'value': item.string, 'label': item.string, 'id': item.string, 'score': item.score} for item in suggest]))


@app.route('/display', methods = ['POST'])
def display():
   display = request.form
   print(display)
   query = faceted_search(display['manufacturer'], startYear="2015", endYear="2020", startPrice=display['startingPrice'], endPrice=display['endPrice'], color=display['color'])
   res=[]
   for item in query:
      # print ("item: - {}".format(item.__dict__))
      res.append(item.__dict__)
   print("res - size: {} - detais: {}".format(len(res), res))
   return render_template('results.html', result = res, search=display['manufacturer'], numOfResult=len(res))


@app.route('/geosearch', methods= ['GET'])
def geosearch():
   return render_template("geosearch.html")

@app.route('/georesult', methods=['POST'])
def georesult():

   display = request.form
   # curLoc = request.form['curLoc']
   # distance = request.form['distance']
   g = geocoder.arcgis('Mountain View, CA')
   currentLocLat = g.latlng[0]
   currentLocLng = g.latlng[1]
   # print("GEOCODER RETURN - (lat {} long {})".format(currentLocLat, currentLocLng))
   query = search_location(str(currentLocLng),str(currentLocLat),"2000")
   locList=[]
   resList = []
   loc={}
   for item in query:
      # print ("item: - {}".format(item.__dict__))
      resList.append(item.__dict__)
      # Create a new location object for Google Map Marker
      loc['lat'] = float(item.__dict__['lat'])
      loc['lng'] = float(item.__dict__['lon'])
      # print("loc - item {}".format(json.dumps(loc)))
      locList.append(loc)
   print("Locations - size: {}; ResultList - size: {}".format(locList, resList))
   return render_template("georesult.html", locations=locList, results=resList)



@app.route('/aggregate')
def show_agg():
   return render_template("aggregate.html")


"""
APIS
"""

@app.route('/showagg', methods = ['POST'])
def agg_show():
   a = request.form.to_dict()
   rows = agg_by(a['agg'])
   # Filter and Capitalize the strings
   rows=[(lambda x: [string.capwords(x[1]), x[3]])(x) for x in rows]
   return render_template('aggresults.html', rows = rows, field = a['agg'].replace("@", '').capitalize())


@app.route('/api/geosearch', methods= ['GET'])
def api_show_geo():
   display = request.form
   print('api_show_geo - {}'.format(display))
   g = geocoder.arcgis('Mountain View, CA')
   currentLocLat = g.latlng[0]
   currentLocLng = g.latlng[1]
   print("GEOCODER RETURN - (lat {} long {})".format(currentLocLat, currentLocLng))
   query = search_location(str(currentLocLng),str(currentLocLat),"5000")
   locList=[]
   resList = []
   loc={}
   for item in query:
      # print ("item: - {}".format(item.__dict__))
      resList.append(item.__dict__)
      # Create a new location object for Google Map Marker
      loc['lat'] = float(item.__dict__['lat'])
      loc['lng'] = float(item.__dict__['lon'])
      print("loc - item {}".format(json.dumps(loc)))
      locList.append(loc)
   print("Locations - size: {}; ResultList - size: {}".format(locList, resList))
   try:
      return Response(json.dumps(locList, indent=4, default=str),
                           mimetype='application/json', status=200)
   except Exception:
      app.logger.warn('request failed:', exc_info=True)
      return Response(json.dumps({'error': 'Attribute Error'}, indent=4, default=str), mimetype='application/json',
                     status=400)



@app.route('/api/post/<field>/<value>', methods = ['GET'])
def api_post_get(field,value):
   res = single_attribute_search(field, value)
   try:
      if len(res)==0:
         res = {'status':'no items were found' }
   except IndexError:
      res = {'status':'no items were found' }

   try:
      return Response(json.dumps(res, indent=4, default=str),
                           mimetype='application/json', status=200)
   except Exception:
      app.logger.warn('request failed:', exc_info=True)
      return Response(json.dumps({'error': 'Attribute Error'}, indent=4, default=str), mimetype='application/json',
                     status=400)



if __name__ == '__main__':
   bootstrap.init_app(app)
   nav.init_app(app)
   app.debug = True
   app.run(port=5000, host="0.0.0.0")
