import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions


def get_request(url, **kwargs):
    api_key = kwargs.get('apiKey')
    print("GET from {} ".format(url))
    try:
        if api_key:
            params = dict()
            params["text"] = kwargs["text"]
            params["version"] = kwargs["version"]
            params["features"] = kwargs["features"]
            params["return_analyzed_text"] = kwargs["return_analyzed_text"]
            response = requests.get(
                url, params=params,
                headers={'Content-Type': 'application/json'},
                auth=HTTPBasicAuth('apikey', api_key))
        else:
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except:
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


def post_request(url, json_payload, **kwargs):
    print(json_payload)
    response = requests.post(url, params=kwargs,  headers={
        'Content-Type': 'application/json', 'X-Debug-Mode': 'true'}, json=json_payload)

    return response


def get_dealers_from_cf(url):
    results = []
    json_result = get_request(url)
    dealerList = json_result["dealerships"]
    for dealer in dealerList:
        dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                               id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                               short_name=dealer["short_name"],
                               st=dealer["st"], zip=dealer["zip"])
        results.append(dealer_obj)
    return results


get_dealers_from_cf(
    "https://1d0da0bd.us-south.apigw.appdomain.cloud/api/dealership")


def get_dealers_by_state_from_cf(url, state):
    results = []
    json_result = get_request(url+"?state="+str(state))
    dealerList = json_result["dealerships"]
    for dealer in dealerList:
        dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                               id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                               short_name=dealer["short_name"],
                               st=dealer["st"], zip=dealer["zip"])
        results.append(dealer_obj)
    return results


def get_dealer_by_id_from_cf(id):
    url = "https://1d0da0bd.us-south.apigw.appdomain.cloud/api/dealership"
    fullUrl = url+"?dealerId="+str(id)
    json_result = get_request(fullUrl)
    dealer = json_result['dealerships']

    if json_result:
        dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                               id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                               short_name=["short_name"],
                               st=dealer["st"], zip=dealer["zip"])

    return dealer_obj


def analyze_review_sentiments(dealerreview):
    url = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/1a31bf71-5ded-4c6c-bad0-84a1bd18fcb9"
    api_key = "hla2WzbVV2swmwgyc9KptJyUkvMN8qNhR0Dxwdz8pEDw"
    authenticator = IAMAuthenticator(api_key)

    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2022-04-07',
        authenticator=authenticator
    )

    natural_language_understanding.set_service_url(url)

    response = natural_language_understanding.analyze(text=dealerreview, features=Features(
        sentiment=SentimentOptions(targets=[dealerreview]))).get_result()
    sentiment = response['sentiment']['document']['label']
    return sentiment


def get_dealer_reviews_from_cf(id):
    results = []
    url = "https://1d0da0bd.us-south.apigw.appdomain.cloud/api/review"
    json_result = get_request(url+"?dealerId="+str(id))

    if 'error' in json_result:
        return {"error": "User not found"}

    reviews = json_result["review"]

    for dealer_review in reviews:
        if(dealer_review['purchase'] == False):
            review_obj = DealerReview(
                id=dealer_review["id"],
                dealership=dealer_review["dealership"],
                name=dealer_review["name"],
                purchase=dealer_review["purchase"],
                review=dealer_review["review"],
                sentiment=analyze_review_sentiments(dealer_review['review']),
                purchase_date="",
                car_make="",
                car_model="",
                car_year="")
        else:

            review_obj = DealerReview(
                id=dealer_review["id"],
                dealership=dealer_review["dealership"],
                name=dealer_review["name"],
                purchase=dealer_review["purchase"],
                review=dealer_review["review"],
                sentiment=analyze_review_sentiments(dealer_review['review']),
                purchase_date=dealer_review["purchase_date"],
                car_make=dealer_review["car_make"],
                car_model=dealer_review["car_model"],
                car_year=dealer_review["car_year"],

            )

        results.append(review_obj)
    return results
