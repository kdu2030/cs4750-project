import json
from django.http import HttpRequest, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from hooeats_app.db_utils.database import HooEatsDatabase

def remove_bookmark(request: HttpRequest) -> JsonResponse:
    if request.COOKIES.get("user") is None:
            return JsonResponse({"result": "Authentication error"})
    user = json.loads(request.COOKIES.get("user"))["username"]
    data = json.loads(request.body)
    delete_bookmark_query = "DELETE FROM bookmark_recipes WHERE recipe_id = ? AND username=?;"
    try:
        database = HooEatsDatabase(secure=True)
        database.execute_secure(False, delete_bookmark_query, data["recipe_id"], user)
        database.close()
        return JsonResponse({"result": "Deletion Successful"})
    except:
        return JsonResponse({"result": "Database Error"})