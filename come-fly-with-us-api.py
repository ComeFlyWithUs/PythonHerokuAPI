from flask import Flask, jsonify, request, Response

app = Flask(__name__)


def routes():
    output = {}
    for rule in app.url_map.iter_rules():
        fn = app.view_functions[rule.endpoint]
        doc = fn.__doc__
        if rule.rule.startswith('/'):
            if  doc != None:
                output[rule.rule] = doc.strip()
            else:
                output[rule.rule] = "No docs found"
    return output

@app.route('/')
def index():
    return jsonify({
        'success': True,
        'version': 0.1,
        'methods': routes()
    })

@app.route('/hello-world')
def helloWorld():
    returnDict = {
        "mssg": "hello world"
    }
    return jsonify({
        'success': True,
        'version': 0.1,
        'data': returnDict
    })

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",threaded=True)
