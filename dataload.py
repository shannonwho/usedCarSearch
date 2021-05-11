from os import wait
from redisearch import AutoCompleter, Client, IndexDefinition, TextField, NumericField, GeoField,TagField, Suggestion
import csv

def load_data(redis_server, redis_port, redis_password):
   load_client = Client(
      'usedCarIdx',
      host=redis_server,
      password=redis_password,
      port=redis_port
   )
   load_ac = AutoCompleter(
   'ac',
   conn = load_client.redis
   )
   
   definition = IndexDefinition(
           prefix=['usedCar:']
           )
   
   load_client.create_index(
           (
               TextField("id", sortable=True),
               TextField("manufacturer", weight=5.0,phonetic_matcher='dm:en'),
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

   # manufacturer = ['acura', 'alfa-romeo', 'aston-martin', 'audi','jeep', 'jaguar','mazda','mercedes-benz','mitsubishi','mini','toyota','tesla','ford', 'ferrari', 'fiat', 'cadillac', 'chevrolet',
   #     'chrysler', 'porsche', 'ram', 'rover', 'lexus', 'lincoln', 'land rover', 'subaru', 'honda', 'hyundai', 'harley-davidson', 'nissan', 'gmc', 'volkswagen', 'volvo', 'dodge', 'infiniti', 'bmw',
   #     'buick', 'kia']
       
   # for m in manufacturer:
   #    load_ac.add_suggestions(Suggestion(m.replace('"', ''),  2.0))
   # with open('./usedCarsCA.csv', encoding='utf-8') as csv_file:
   #    csv_reader = csv.reader(csv_file, delimiter=',')
   #    line_count = 0
   #    for row in csv_reader:
   #       if line_count > 0:
   #          load_ac.add_suggestions(Suggestion(row[5].replace('"', ''),  2.0))
   #          wait(20)
   #       line_count += 1
   # load_ac.add_suggestions(Suggestion('alfa-romeo', 2.0)), Suggestion('aston-martin', 2.0), Suggestion('audi', 2.0), Suggestion('jeep', 2.0), Suggestion('jaguar', 2.0))
   # load_ac.add_suggestions(Suggestion('mazda', 2.0), Suggestion('mercedes-benz', 2.0), Suggestion('mitsubishi', 2.0), Suggestion('mini', 2.0), Suggestion('toyota', 2.0), 
   # Suggestion('tesla', 2.0), Suggestion('ford', 2.0), Suggestion('ferrari', 2.0), Suggestion('fiat', 2.0), Suggestion('cadillac', 2.0), Suggestion('chevrolet', 2.0),Suggestion('chrysler', 2.0),
   # Suggestion('porsche', 2.0),Suggestion('ram', 2.0),Suggestion('rover', 2.0),Suggestion('lexus', 2.0),Suggestion('lincoln', 2.0),Suggestion('land rover', 2.0),
   # Suggestion('subaru', 2.0),Suggestion('honda', 2.0),Suggestion('hyundai', 2.0),Suggestion('harley-davidson', 2.0),Suggestion('nissan', 2.0),Suggestion('gmc', 2.0),Suggestion('volkswagen', 2.0),
   # Suggestion('volvo', 2.0),Suggestion('dodge', 2.0),Suggestion('infiniti', 2.0),Suggestion('bmw', 2.0))

   # Finally Create the alias
   load_client.aliasadd("usedCar")