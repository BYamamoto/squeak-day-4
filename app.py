from flask import (
    Flask,
    render_template,
    session,
    redirect,
    request,
    url_for
)
import urllib
import requests
import json
from oauth import sign_url

app = Flask(__name__)

YELP_SEARCH_URL = 'http://api.yelp.com/v2/search'

@app.route('/')
def index():
    # print request.args['data2']
    return render_template('index.html')


@app.route('/results', methods=['POST'])
def results():
    search_term = request.form['term']
    location = request.form['location']

    data = {
        'term': search_term,
        'location': location
    }
    query_string = urllib.urlencode(data)
    api_url = YELP_SEARCH_URL + "?" + query_string
    signed_url = sign_url(api_url)
    response = requests.get(signed_url)
    json_response = json.loads(response.text)

    return render_template('results.html',
                            search_term=search_term,
                            location=location,
                            businesses=json_response['businesses'])


@app.route('/save', methods=["POST"])
def save():
    return request.form['name']

if __name__ == '__main__':
    app.run(debug=True)
