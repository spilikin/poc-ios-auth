from flask import Flask, jsonify

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)


# sanity check route
@app.route('/api/1.0/info', methods=['GET'])
def info():
    return jsonify({
        'description':'HealthID API',
        'version':'1.0'
    })

