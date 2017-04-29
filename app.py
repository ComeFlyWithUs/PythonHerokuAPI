import os

from flask import Flask, jsonify, request, Response

from googleplaces import GooglePlaces, types, lang

YOUR_API_KEY = 'AIzaSyAUecZjZRw1lU4N0gIkQR07hG4tcV3AbOY'

google_places = GooglePlaces(YOUR_API_KEY)

app = Flask(__name__)

version = 0.1

def routes():
    output = {}
    for rule in app.url_map.iter_rules():
        fn = app.view_functions[rule.endpoint]
        doc = fn.__doc__
        if rule.rule.startswith('/' ):
            if  doc != None:
                output[rule.rule] = doc.strip()
            else:
                output[rule.rule] = "No docs found"
    return output

@app.route('/', methods=['GET'])
def index():
  """Output the defined routes"""
  return jsonify({
    'success': True,
    'version': version,
    'methods': routes()
  })

@app.route('/hello-world', methods=['GET'])
def helloWorld():
  """Hello world"""
  return jsonify({
    'success': True,
    'version': version,
    'data': {
      "mssg": "hello world"
    }
  })

@app.route('/google/<lat>/<lng>/<radius>')
def googleTest(lat, lng, radius):
  """google test"""
  places = []
  query_result = google_places.nearby_search(
    lat_lng={"lat":lat, "lng": lng},
    radius=int(radius), types=[types.TYPE_FOOD])

  if query_result.has_attributions:
      print(query_result.html_attributions)

  for place in query_result.places:
      place.get_details()
      print(str(place.international_phone_number))
      print(str(place.international_phone_number))
      print(str(place.url))
      place_details = {
          "name": place.name,
          "position": {
              "lat": float(place.geo_location["lat"]),
              "lng": float(place.geo_location["lng"])
          },
          "phone": {
              "local": place.local_phone_number,
              "internation": place.international_phone_number
          },
          "url": place.url,
          "photos": []
      }
      for photo in place.photos:
          photo.get(maxheight=500, maxwidth=500)
          place_details["photos"].append(photo.url)
      places.append(place_details)

  return jsonify({
    'success': True,
    'version': version,
    'data': places
  })


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000, debug=True)