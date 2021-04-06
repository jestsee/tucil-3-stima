from flask import *
import sys
import json
from read import *
app = Flask(__name__)

@app.route("/")
def launch():
    return render_template("map.html")

@app.route('/postmethod', methods = ['POST'])
def get_post_javascript_data():
    jsdata = request.get_json()
    # cara akses data json
    # jsdata['coordinates'][idx]['lat'] nerima latitude
    # jsdata['coordinates'][idx]['lng'] nerima longitude
    arrOfCoords = []
    arrOfEdges = []
    for i in range(len(jsdata['coordinates'])):
        lat = jsdata['coordinates'][i]['lat']
        lng = jsdata['coordinates'][i]['lng']
        arrOfCoords.append([lat,lng])
    arrOfEdges = jsdata['edges']
    g = readData(arrOfEdges,arrOfCoords)
    start = int(jsdata['start'])
    goal = int(jsdata['finish'])
    sol = AStar(g,start,goal)
    cost = sol.pop()
    solution = {'solution': sol, 'cost': str("{:.4f}".format(cost)) + " km"}
    #print(solution)
    return json.dumps(solution)

if __name__ == "__main__":
    app.run()