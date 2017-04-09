import sqlalchemy
import pandas as pd
import json
import flask
from sqlalchemy import create_engine
from sqlalchemy import *
from flask import *
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)



@app.route("/get_names", methods=['GET'])
def get_names():
    namesQuery = "select name from Census_2010 limit 50;"
    namesResult = pd.read_sql_query(namesQuery, con=engine)
    namesArray = namesResult['name'].values
    namesJson = {'names':namesArray.tolist()}
    return jsonify(namesJson)

@app.route("/get_stats", methods=['GET', 'POST'])
def get_stats():
    print "hi"
    if request.method == 'POST':
        # print request.get_data()
        # print request.get_json()
        searchName = request.get_data()
        # searchName = raw_input("Input name:")
        searchName = searchName.upper()  # force uppercase
        searchName.replace(" ", "")  # remove spaces

        # SEARCH CENSUS
        print searchName
        censusQuery = "select * from Census_2010 where name='", searchName, "';"
        censusQuery = "".join(censusQuery)
        print censusQuery
        censusResult = pd.read_sql_query(censusQuery, con=engine)
        # result = pd.read_sql_query("select * from Census_2010 where name='BIRKY';", con = engine)
        print censusResult
        # CONVERT TO JSON
        censusJson = censusResult.to_json(orient="values")
        print censusJson

        # SEARCH ASIAN LIST
        asianQuery = "select * from asian_surnames where name='", searchName, "';"
        asianQuery = "".join(asianQuery)
        print asianQuery
        asianResult = pd.read_sql_query(asianQuery, con=engine)
        # result = pd.read_sql_query("select * from Census_2010 where name='BIRKY';", con = engine)
        print asianResult
        # CONVERT TO JSON
        asianJson = asianResult.to_json(orient="values")
        print asianJson

        #results = [censusJson, asianJson]
        #results ="".join(results)

        results = {"census": censusJson, "asian": asianJson}
        print "results:"
        # print results
        # resultsJson = results.to_json(orient="values")
        # print resultsJson
        print results

        return jsonify(results)
    else:
        return jsonify({'msg':'hi'})

if __name__ == "__main__":
    # BUILD DATABASE
    engine = create_engine('sqlite:///tutorial.db')

    app.run()





#CENSUS DATA
#df = pd.read_excel("Names_2010Census.xlsx")
#print df.head()
#df.to_sql(name='Census_2010', con = engine, if_exists = 'replace')
#print pd.read_sql("Census_2010", con = engine)
#ASIAN DATA
#df = pd.read_excel("asian_surnames.xlsx")
#df.to_sql(name='asian_surnames', con = engine, if_exists = 'replace')
#print pd.read_sql("asian_surnames", con = engine)
#SEARCH QUERY - need to be in all caps
#searchName = 'BIRKY'








#df.to_sql(name='test2_table', con = engine, if_exists = 'append')

#print pd.read_sql("test2_table", con = engine)

#print pd.read_sql("test_table", con = engine)
