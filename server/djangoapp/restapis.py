from email import message
from unittest import result
import requests
import json
from django.http import HttpResponseRedirect, HttpResponse
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
# from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
# from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions


def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        response = requests.get(url, headers={'Content-Type': 'application/json'},
                                params=kwargs)
    except:
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


def post_request(url, json_payload, **kwargs):
    response = requests.post(url, params=kwargs,  headers={
                             'Content-Type': 'application/json', 'X-Debug-Mode': 'true'}, json=json_payload)
    print(json.dumps(json_payload, indent=4))
    print(response)
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


def get_dealer_reviews_from_cf(url, dealerId):
    results = []
    json_result = get_request(url+"?dealerId="+str(dealerId))
    reviews = json_result["review"]
    # sentiment = analyze_review_sentiments(review_obj.review)

    for dealer_review in reviews:
        if(dealer_review['purchase'] == False):
            review_obj = DealerReview(
                dealership=dealer_review["dealership"],
                name=dealer_review["name"],
                purchase=dealer_review["purchase"],
                review=dealer_review["review"],
                sentiment="teste")
        else:
            review_obj = DealerReview(
                dealership=dealer_review["dealership"],
                name=dealer_review["name"],
                purchase=dealer_review["purchase"],
                review=dealer_review["review"],
                id=dealer_review["id"],
                purchase_date=dealer_review["purchase_date"],
                car_make=dealer_review["car_make"],
                car_model=dealer_review["car_model"],
                car_year=dealer_review["car_year"],
                sentiment="teste"
            )

        results.append(review_obj)
    return results
