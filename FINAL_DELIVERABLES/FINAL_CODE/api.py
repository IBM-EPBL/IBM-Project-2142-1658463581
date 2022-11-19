import http.client
import json

def image():
    conn = http.client.HTTPSConnection("spoonacular-recipe-food-nutrition-v1.p.rapidapi.com")
    headers = {'X-RapidAPI-Key': "fec580ab23msh31718969c3a7b57p13eb96jsn540037e80f67",
    'X-RapidAPI-Host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
    }
    conn.request("GET", "/food/images/classify?imageUrl=https%3A%2F%2Fspoonacular.com%2FrecipeImages%2F635350-240x150.jpg", headers=headers)
    res = conn.getresponse()
    data = res.read()
    dict = data.decode("utf-8")
    y = json.loads(dict)
    a=y["category"]
    conn.request("GET", "/recipes/guessNutrition?title="+str(a), headers=headers)
    res = conn.getresponse()
    data = res.read()
    result=data.decode("utf-8")
    cal=json.loads(result)
    calories=cal["calories"]
    output=calories["value"]
    print(output)


