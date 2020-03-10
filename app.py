from flask import Flask
import demo
import json
app = Flask(__name__)

@app.route("/")
def home():
    return '''
    <!DOCTYPE html>
    <html>
        <head>
        <title>Tasks</title>
        </head>
        <body>
        <h1>Report Data</h1>
        </body>
    </html> 
    '''

@app.route("/get_shift_left_data/")
def get_task():
    return demo.get_graph_three_data()

app.run(port=5000, host='0.0.0.0')