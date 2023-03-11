
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseRedirect
from hooeats_app.db_utils.database import HooEatsDatabase
from json import loads
import hashlib
import traceback
import json
from django.urls import reverse

def signup(request: HttpRequest) -> HttpResponse:
    return render(request, "hooeats_app/signup.html")

def signup_error(request: HttpRequest, error: str) -> HttpResponse:
    return render(request, "hooeats_app/signup.html", {"error": error})

def signin_error(request: HttpRequest, error: str) -> HttpResponse:
    return render(request, "hooeats_app/signin.html", {"error": error})

def signin(request: HttpRequest) -> HttpResponse:
    return render(request, "hooeats_app/signin.html")

def handle_signin(request: HttpRequest) -> HttpResponse:
    username = request.POST.get("username")
    password = request.POST.get("password")
    password_hash = str(hashlib.sha512(bytearray(password, "ascii")).hexdigest())
    signin_query = f"SELECT * FROM user WHERE username = '{username}'"
    try:
        database = HooEatsDatabase()
        signin_results = database.execute(signin_query)
        if len(signin_results) == 0:
            return redirect(reverse("signin_error", args=["User does not exist."]))
        if signin_results[0]["password"] != password_hash:
           return redirect(reverse("signin_error", args=["Your password is incorrect"]))
        user_dict = {"username": username, "email": signin_results[0]["email"], "profile_img": signin_results[0]["profile_img"]}
        response = redirect(reverse("index"), "hooeats_app/index.html", {"user_dict": user_dict})
        response.set_cookie("user", json.dumps(user_dict))
        return response
    except Exception as e:
        traceback.print_exc()
        return redirect(reverse("signin_error", args=["We were unable to verify your account. Please try again."]))
        

def handle_signup(request: HttpRequest) -> HttpResponse:
    username = request.POST.get("username")
    email = request.POST.get("email")
    password = request.POST.get("password")
    password_hash = str(hashlib.sha512(bytearray(password, "ascii")).hexdigest())
    profile_img = "https://iili.io/yhRgWb.md.png"
    signup_query = f"INSERT INTO user (username, email, password, profile_img) VALUES ('{username}', '{email}', '{str(password_hash)}', '{profile_img}')"
    database = HooEatsDatabase()
    try: 
        database.execute(signup_query, expect_results=False)
        database.close()
        user_dict = {"username": username, "email": email, "profile_img": profile_img}
        response = redirect(reverse("index"), "hooeats_app/index.html", {"user_dict": user_dict})
        response.set_cookie("user", json.dumps(user_dict))
        return response
    except Exception as e:
        traceback.print_exc()
        return redirect(reverse("signup_error", args=["We were unable to create your account. Please try again."]))
    
    
    

def signup_valid(request: HttpRequest) -> JsonResponse:
    data = loads(request.body)
    email = data["email"]
    username = data["username"]
    email_query = f"SELECT email FROM user WHERE email = '{email}';"
    username_query = f"SELECT username FROM user WHERE username = '{username}'";
    try:
        database = HooEatsDatabase()
        emails = database.execute(email_query)
        usernames = database.execute(username_query)
        database.close()
        if len(usernames) == 0 and len(emails) == 0:
            return JsonResponse({"result": "Signup Valid"})
        if len(usernames) != 0:
            return JsonResponse({"result": "Duplicate Username"}) 
        return JsonResponse({"result": "Duplicate Email"})
    except Exception as e:
        print(e)
        return JsonResponse({"result": "Database Failure"})
