from redisearch import AutoCompleter, Client, IndexDefinition, TextField, NumericField, GeoField,TagField, Suggestion
import redis_client as rc
import csv

def load_data():
#    load_client = Client(
#       'usedCarIdx',
#       host=redis_server,
#       password=redis_password,
#       port=redis_port
#    )
   load_ac = AutoCompleter(
   'ac',
   conn = rc.connection.redis
   )
   
   definition = IndexDefinition(
           prefix=['usedCar:']
           )
   rc.connection.create_index(
           (
               TextField("id", sortable=True),
               TextField("manufacturer", sortable=True),
               TextField('model', sortable=True),
               TextField('type', sortable=True),
               NumericField('price', sortable=True),
               NumericField('year', sortable=True),
               TextField('region', sortable=True),
               TextField('state', sortable=True),
               TextField('title_status', sortable=True),
               TextField('url', sortable=True),
               TextField('paint_color',sortable=True),
               TextField('transmission',sortable=True),
               TextField('fuel',sortable=True),
               GeoField('location'),
               NumericField('mileage', sortable=True),
               TagField('tags')
               ),        
       definition=definition)

   with open('./usedCarsCA.csv', encoding='utf-8') as csv_file:
      csv_reader = csv.reader(csv_file, delimiter=',')
      line_count = 0
      for row in csv_reader:
         if line_count > 0:
            load_ac.add_suggestions(Suggestion(row[5].replace('"', ''),  2.0))
            # load_client.redis.hset(
            #         "fortune500:%s" %(row[1].replace(" ", '')),
            #         mapping = {
            #             'title': row[1],
            #             'company': row[1],
            #             'rank': row[0],
            #             'website': row[2],
            #             'employees': row[3],
            #             'sector': row[4],
            #             'tags': ",".join(row[4].replace('&', '').replace(',', '').replace('  ', ' ').split()).lower(),
            #             'industry': row[5],
            #             'hqcity': row[8],
            #             'hqstate': row[9],
            #             'ceo': row[12],
            #             'ceoTitle': row[13],
            #             'ticker': row[15],
            #             'revenues': row[17],
            #             'profits': row[19],
            #             'assets': row[21],
            #             'equity': row[22]

            #    })
         line_count += 1
   # Finally Create the alias
   rc.connection.aliasadd("usedCar")