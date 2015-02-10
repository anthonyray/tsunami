import os
import cities
import datetime
import cassandraTest as cassandre
from flask import Flask, render_template, request,jsonify

tmpl_dir = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, template_folder=tmpl_dir)

japan_cities = getattr(cities,"cities")

@app.route('/')
def index():
    title = "Japan Tsunami Map"
    return render_template('index.html',title=title,japancities=japan_cities)

@app.route('/tsunami',methods=["POST"])
def tsunami():
    # Parsing the request
    lon = float(request.form["lon"])
    lat = float(request.form["lat"])
    dat1 = datetime.datetime.strptime(request.form["date"],"%Y-%m-%dT%H:%M")
    dat2 = dat1 + datetime.timedelta(minutes=10)
    radius = 500
    size_req_t = 1000000

    keyspace = "jap1"
    table = "bigtable"
    
    # Retrieving data from cassandra
    phones = cassandre.alertPhones(dat1,dat2,lat,lon,radius,size_req_t,table,keyspace)
    
    # Writing data to cassandra
    crea_offset = sys.argv[3]
    crea_loop = sys.argv[4]
    offset = int(crea_offset)
    for i in range(0,int(crea_loop)):
        if(i == 0):
            test = cassandre.multipleInsertCreation(data=phones[0:offset],table=str(table+'bis'))
            cassandre.multipleInsertExec(keyspace=keyspace_t,cmd=test)
            
        else:
            u = i*offset
            uu = u + offset
            test = cassandre.multipleInsertCreation(data=phones[u:uu],table=str(table+'bis'))
            cassandre.multipleInsertExec(keyspace=keyspace,cmd=test)
	
    return jsonify(status="node_down",phones=phones)


if __name__ == "__main__":
    app.run()

