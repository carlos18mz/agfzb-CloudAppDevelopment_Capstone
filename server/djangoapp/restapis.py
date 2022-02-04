from unittest import result
import requests
import json
from .models import CarMake, CarModel, CarDealer, DealerReview

from requests.auth import HTTPBasicAuth


api_key = "HI-H3s5bmcSqfdX6leH3lBMwk3axiWhsoKDRNtMrC_AS"
urlnlu = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/a5afa9da-db34-4aff-9356-813fa833e5e5/v1/analyze?version=2020-08-01"

# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
  print("kwargs : ",kwargs)
  print("GET from {} ".format(url))
  #params = dict()
  #params["text"] = kwargs["text"]
  #params["version"] = kwargs["version"]
  #params["features"] = kwargs["features"]
  #params["return_analyzed_text"] = kwargs["return_analyzed_text"]
  response = None
  try:
    # Call get method of requests library with URL and parameters
    if(api_key):
      response = requests.get(url, params=kwargs, headers={'Content-Type': 'application/json'},auth=HTTPBasicAuth('apikey', api_key))
    else:
      response = requests.get(url, params=kwargs, headers={'Content-Type': 'application/json'})
  
  except:
    # If any error occurs
    print("Network exception occurred")
  status_code = response.status_code
  print("With status {} ".format(status_code))
  json_data = json.loads(response.text)
  return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, payload, **kwargs):
    print(url)
    print(payload)
    print(kwargs)
    try:
        response = requests.post(url, params=kwargs, json=payload)
    except Exception as e:
        print("Error" ,e)
    print("Status Code ", {response.status_code})
    data = json.loads(response.text)
    return data

def get_dealers_from_cf(url, **kwargs):
  results = []
  json_result = get_request(url)
  if json_result:
      print("json : ",json_result)
      dealers = json_result["entries"]
      for dealer in dealers:
          dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                                  id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                                  short_name=dealer["short_name"],
                                  st=dealer["st"], zip=dealer["zip"])
          results.append(dealer_obj)

  return results


def xstr(s):
  return '' if s is None else str(s)

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
def get_dealer_reviews_from_cf(url, dealerId):
  print("dealerId : ",dealerId)
  results = []
  json_result = get_request(url)
  if json_result:
    reviews = json_result["entries"]
    for review in reviews:
      #purchase_date = '' if review["purchase_date"] is None else str(review["purchase_date"]) 
      reviews_obj = DealerReview(dealership=review["dealership"], name=review["name"], purchase=review["purchase"],
                                  review=review["review"], purchase_date="purchase_date", car_make="car_make",
                                  car_model="car_model", car_year="car_year", car_sentiment=analyze_review_sentiments(review["review"]), id=review["id"]) 
      results.append(reviews_obj)
      
  #results2 = list(filter(lambda x: str(x.dealership) == str(dealerId), results))
  #print("results2 ", len(results2))
  return results



# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
def analyze_review_sentiments(dealerreview, **kwargs):
  #get_request(urlnlu)
  params = json.dumps({"text": dealerreview, "features": {"sentiment": {}}})
  response = requests.post(urlnlu, params=params, headers={'Content-Type': 'application/json'},
                                    auth=HTTPBasicAuth('apikey', api_key))
  try:
    sentiment=response.json()['sentiment']['document']['label']
    return sentiment
  except:
    return "neutral"

