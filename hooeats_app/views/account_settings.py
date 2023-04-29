import hashlib
import json
from traceback import print_exc
from typing import Dict
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from hooeats_app.db_utils.database import HooEatsDatabase

profile_images = [
    "yhRFob.png",
    "yhR5iv.png",
    "yhRRWJ.png",
    "yhRAxa.png",
    "yhRYfR.png",
    "yhRalp.png",
    "yhRcUN.png",
    "yhR0JI.png",
    "yhR1Rt.png",
    "yhREOX.png",
    "yhRGbn.png",
    "yhRVxs.png",
    "yhRWWG.png",
    "yhRXsf.png",
    "yhRjf4.png",
    "yhRw0l.png",
    "yhRNg2.jpg",
    "yhReJS.jpg",
    "yhRk57.jpg",
    "yhRve9.jpg",
    "yhR8be.jpg",
    "yhRUzu.jpg",
    "yhRgWb.md.png"
]
    


def account_settings(request: HttpRequest, message: str = "") -> HttpResponse:
    context = {}
    full_img_urls = []

    if request.COOKIES.get("user") is None:
            return redirect(reverse("signin"))
    cookie_data = json.loads(request.COOKIES.get("user"))
    username = cookie_data["username"]
    for profile_image in profile_images:
        full_img_urls.append(f"https://iili.io/{profile_image}")
    context["profile_images"] = full_img_urls
    account_query = "SELECT email, profile_img FROM user WHERE username = ?;"
    try:
        database = HooEatsDatabase(secure=True)
        user_data = database.execute_secure(True, account_query, username)[0]
        context["email"] = user_data["email"]
        context["profile_img"] = user_data["profile_img"]
    except:
        context["error"] = "Unable to load account settings."
        context["email"] = cookie_data["email"]
        context["profile_img"] = cookie_data["profile_img"]
        print_exc()
    
    if message.find("Error: ") != -1:
         context["error"] = message
    elif message != "":
         context["message"] = message
    
    response = render(request, "hooeats_app/account-settings.html", context=context)
    if "error" not in context:
        user = {
             "email": context["email"],
             "profile_img": context["profile_img"],
             "username": username
        }
        response.set_cookie("user", json.dumps(user))
    
    return response

def update_account(request: HttpRequest) -> HttpResponse:
    message = ""
    if request.COOKIES.get("user") is None:
            return redirect(reverse("signin"))
    user_data = json.loads(request.COOKIES.get("user"))
    username = user_data["username"]
    profile_image = request.POST.get("profile_image")
    email = request.POST.get("email")
    update_account_query = "UPDATE user SET email = ?, profile_img = ? WHERE username = ?;"
    try:
         database = HooEatsDatabase(secure=True)
         database.execute_secure(False, update_account_query, email, profile_image, username)
         database.close()
         message = f"Successfully updated {username}'s account."
    except:
         print_exc()
         message = "Error: We were unable to update your account."
    return redirect(reverse("account_settings", args=[message]))
            
def change_password(request: HttpRequest) -> HttpResponse:
    user_data = json.loads(request.COOKIES.get("user"))
    username = user_data["username"]

    current_password = request.POST.get("current_password")
    current_password_hash = str(hashlib.sha512(bytearray(current_password, "ascii")).hexdigest())

    new_password = request.POST.get("password")
    new_password_hash = str(hashlib.sha512(bytearray(new_password, "ascii")).hexdigest())

    signin_query = "SELECT * FROM user WHERE username = ?"
    update_query = "UPDATE user SET password = ? WHERE username = ?"
    try:
        database = HooEatsDatabase(secure=True)
        signin_results = database.execute_secure(True, signin_query, username)
        if signin_results[0]["password"] != current_password_hash:
           return redirect(reverse("account_settings", args=["Your password is incorrect."]))
        database.execute_secure(False, update_query, new_password_hash, username)
        return redirect(reverse("account_settings", args=[f"Successfully updated the password to {username}'s account"]))
    except:
        print_exc()
        return redirect(reverse("account_settings", args=[f"Error: Unable to update password"]))
        