# Competitions
from dbconnection_project1 import dbwrite
import requests

url = "https://api.sportradar.com/tennis/trial/v3/en/competitions.json?api_key=UIHu7awT0hFy9PmXnCx27EOdLWksoz8yrB3z8WsD"

headers = {"accept": "application/json"}

response = requests.get(url, headers=headers)
print(response.status_code)
if response.status_code==200:
    data=response.json()
   # print(data)
    l1=data.get("competitions")

    for item in l1:
        id=item.get("id")
        name=item.get("name")
        type=item.get("type")
        gender=item.get("gender")
        category=item.get("category")
        category_id=category.get("id")
        category_name=category.get("name")

        query1="INSERT INTO `project1`.`categories` (`category_id`,`category_name`) VALUES ('"+category_id+"','"+category_name+"') "

        query2="INSERT INTO `project1`.`competitions` (`competition_id`, `competition_name`, `parent_id`, `type`, `gender`,`category_id`) VALUES ('"+id+"','"+name+"',null,'"+type+"','"+gender+"','"+category_id+"')"

        dbwrite(query1)

       

        dbwrite(query2)
        




