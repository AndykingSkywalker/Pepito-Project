from flask import Flask, render_template, Response
from flask_cors import CORS, cross_origin
import requests
import time
import json

app = Flask(__name__)
CORS(app, origins=["http://localhost:5000"])

@app.route('/')
@cross_origin()
def index():
    return render_template('index.html')

@app.route('/sse')
@cross_origin()
def sse_stream():
    def generate():
        while True:
            data = {"event": "heartbeat", "time": int(time.time())}
            yield f"data: {json.dumps(data)}\n\n"
            time.sleep(10)
    return Response(generate(), mimetype='text/event-stream')

@app.route('/proxy/sse')
@cross_origin()
def proxy_sse():
    def generate():
        with requests.get('https://api.thecatdoor.com/sse/v1/events', stream=True) as r:
            for line in r.iter_lines():
                if line:
                    yield f"data: {line.decode('utf-8')}\n\n"
    return Response(generate(), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(debug=True)