from multiprocessing import context
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarModel
from .restapis import post_request, get_dealers_from_cf, get_dealer_reviews_from_cf, get_dealers_by_state_from_cf
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging


# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)


# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request


def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/login.html', context)
    else:
        return render(request, 'djangoapp/login.html', context)

# Create a `logout_request` view to handle sign out request


def logout_request(request):
    context = {}
    if request.method == "GET":
        logout(request)
        return redirect("/djangoapp")

# Create a `registration_request` view to handle sign up request


def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.debug("{} is new user".format(username))
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships


def get_dealerships(request):
    context = {}
    if request.method == "GET":
        url = "https://1d0da0bd.us-south.apigw.appdomain.cloud/api/dealership"
        dealerList = get_dealers_from_cf(url)
        context['dealership_list'] = dealerList
        return render(request, 'djangoapp/index.html', context)


def get_dealerships_by_state(request, state):
    context = {}
    if request.method == "GET":
        url = "https://1d0da0bd.us-south.apigw.appdomain.cloud/api/dealership"
        dealerList = get_dealers_by_state_from_cf(url, state)
        context['dealership_list'] = dealerList
        return render(request, 'djangoapp/index.html', context)


def get_dealer_details(request, dealerId):
    context = {}
    if request.method == "GET":
        url = "https://1d0da0bd.us-south.apigw.appdomain.cloud/api/review"
        reviews = get_dealer_reviews_from_cf(url, dealerId)
        context['dealer_reviews'] = reviews
    return render(request, 'djangoapp/dealer_details.html', context)


def add_review(request, dealerId):
    context = {}
    url = "https://1d0da0bd.us-south.apigw.appdomain.cloud/api/review?dealerId=" + \
        str(dealerId)
    # dealer = get_dealer_reviews_from_cf(url, dealerId)
    # context["dealer"] = dealer
    review = dict()
    review['name'] = "My Name"
    review['dealership'] = dealerId
    review['review'] = "My first review"
    review['purchase'] = False
    if review['purchase']:
        review['purchsae_date'] = "input"
        review['car_make'] = "input"
        review['car_model'] = "input"
        review['car_year'] = "input"

    json_payload = dict()

    json_payload = review

    # if request.method == 'POST':
    if request.user.is_authenticated:
        newPost = post_request(url, json_payload)
        context['dealer_reviews'] = newPost
    return render(request, "djangoapp/dealer_details.html", context)
    # else:
    #     return render(request, 'djangoapp/add_review.html', context)
