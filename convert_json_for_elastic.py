import json

with open('/Users/jofy/Dropbox/Skola/VI_vyhladavanie_informacii/Zadanie1/FIIT-VI-zadanie-1/data_to_parser.json', 'r') as f:
    data_json = json.load(f)



for i, value in enumerate(data_json):
    try:
        data_json[i]['film_length'] = int(value['film_length'])
        data_json[i]['film_year'] = int(value['film_year'])
        data_json[i]['film_average'] = int(value['film_average'])
    except:
        del data_json[i]
    



data = {}
data = []

for c, value in enumerate(data_json, 1):
    data.append("{\"index\":{\"_id\":\"%d\"}}" %c)
    data.append(json.dumps(value))


with open('/Users/jofy/Dropbox/Skola/VI_vyhladavanie_informacii/Zadanie1/FIIT-VI-zadanie-1/data_for_elastic.json', 'w') as f:
    for value in data:
        f.write(value + "\n")


# curl -H "Content-Type: application/json" -XPOST "localhost:9200/books/_bulk?pretty&refresh" --data-binary "@data_film.json"
# sudo spctl --master-disable

