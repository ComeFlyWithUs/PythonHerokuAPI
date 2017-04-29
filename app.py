import os

from flask import Flask, jsonify, request, Response

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
  return jsonify({
    'success': True,
    'version': version,
    'methods': routes()
  })

@app.route('/hello-world', methods=['GET'])
def helloWorld():
  return jsonify({
    'success': True,
    'version': version,
    'data': {
      "mssg": "hello world"
    }
  })


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000, debug=True)
