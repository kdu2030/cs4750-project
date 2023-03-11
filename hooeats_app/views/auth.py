
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, JsonResponse
from hooeats_app.db_utils.database import HooEatsDatabase
from json import loads
import hashlib
import traceback
import json
from django.urls import reverse

def signup(request: HttpRequest) -> HttpResponse:
    return render(request, "hooeats_app/signup.html")

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
        return redirect(reverse("signup"), "hooeats_app/signup.html", {"error": "We were unable to connect to our servers. Please try again."})
    
    
    

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
