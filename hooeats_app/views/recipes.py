import json
from django.http import HttpRequest, JsonResponse
from hooeats_app.db_utils.database import HooEatsDatabase

def remove_bookmark(request: HttpRequest) -> JsonResponse:
    data = json.loads(request.body)
    delete_bookmark_query = "DELETE FROM bookmark_recipes WHERE recipe_id = ?;"
    try:
        database = HooEatsDatabase(secure=True)
        database.execute_secure(False, delete_bookmark_query, data["recipe_id"])
        database.close()
        return JsonResponse({"result": "Deletion Successful"})
    except:
        return JsonResponse({"result": "Database Error"})