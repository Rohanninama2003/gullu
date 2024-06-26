from flask import Flask,request,jsonify
import  requests
import json
app = Flask(__name__)


@app.route('/',methods=['POST'])
def index():
    data=request.get_json()
    source_curr=data['queryResult']['parameters']['unit-currency']['currency']
    amount=data['queryResult']['parameters']['unit-currency']['amount']
    target_curr=data['queryResult']['parameters']['currency-name']

    cf= fetch_conversion_factor(source_curr,target_curr)
    final_amount=cf*amount

    response={
        'fulfillmentText':" {} {} is {} {}".format(amount,source_curr,final_amount,target_curr)
    }

    print(final_amount)
    return jsonify(response)
def fetch_conversion_factor(source_curr,target_curr):
    url="https://api.freecurrencyapi.com/v1/latest?apikey=fca_live_GmVTPWI9j65EgA6qP07ga45ld4DG2Eq9SWnb1eQg"
    response=requests.get(url)
    response=response.json()
    rates = response['data']

    # Retrieve rates for source and destination currencies
    source_rate = rates.get(source_curr)
    destination_rate = rates.get(target_curr)

    if source_rate is None or destination_rate is None:
        return None  # Handle the case where one of the currencies is not in the data

    # Calculate the conversion factor
    conversion_factor = destination_rate / source_rate

    return conversion_factor

