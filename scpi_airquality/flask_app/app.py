# flask_web/app.py

from flask import Flask
import yaml
app = Flask(__name__)

@app.route('/pm25')
def hello_world():
    response_object={}
    response_object["pm2.5"]=10
    response_object["pm10"]=5
    return yaml.dump(response_object,Dumper=yaml.Dumper)
#return 'Hey, we have Flask in a Docker container!'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
