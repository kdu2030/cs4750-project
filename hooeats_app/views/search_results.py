from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, JsonResponse
from hooeats_app.db_utils.database import HooEatsDatabase
from typing import Dict, List
from datetime import datetime, timedelta
import json

def get_search_results_from_recipes(request: HttpRequest, keyword: str) -> JsonResponse:
    query = "SELECT * FROM recipe JOIN recipe_tags JOIN recipe_ingredients '\
    WHERE recipe_name LIKE ? OR steps LIKE ? OR ingredient LIKE ? OR tag LIKE ?"
    try:
        database = HooEatsDatabase(secure=True)
        search_result_data = database.execute_secure(True, query, keyword, keyword, keyword, keyword)
        return JsonResponse(search_result_data)
    except:
         error = {"result": "Database Error"}
         return JsonResponse(error)
