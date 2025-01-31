import requests

from Scripts.dbconnection_project1 import dbwrite

url = "https://api.sportradar.com/tennis/trial/v3/en/double_competitors_rankings.json?api_key=UIHu7awT0hFy9PmXnCx27EOdLWksoz8yrB3z8WsD"

headers = {"accept": "application/json"}

response = requests.get(url, headers=headers)

print(response.status_code)
if response.status_code==200:
    data=response.json()
    l3=data.get("rankings")
    dict1=l3[0]
    dict2=l3[1]
    l4=dict1.get("competitor_rankings")
    for item in l4:
        competitor=item.get("competitor")
        comp_id=competitor.get("id", "") 
        comp_name=competitor.get("name", "") 
        country_name=competitor.get("country", "") 
        country_code=competitor.get("country_code", "") 
        abbreviation=competitor.get("abbreviation", "") 
        rank=item.get("rank", "")
        movement=item.get("movement", "") 
        points=item.get("points", "") 
        comp_played=item.get("competitions_played", "") 

        query1= ("INSERT INTO `project1`.`competitors` (`competitor_id`,`name`,`country`,`country_code`,`abbreviation`) VALUES ('"+comp_id+"','"+comp_name+"','"+country_name+"','"+country_code+"','"+ str(abbreviation) +"') " )

        query2 = (
            "INSERT INTO `project1`.`competitor_rankings` "
            "(`comp_rank`, `movement`, `points`, `competitions_played`, `competitor_id`) "
            "VALUES ('" + str(rank) + "', '" + str(movement) + "', '" + str(points) + "', '" + str(comp_played) + "', '" + str(comp_id) + "')"
        )
        
        dbwrite(query1)
        dbwrite(query2)






'''
query1="INSERT INTO `project1`.`competitors` (`competitor_id`,`name`,`country`,`country_code`,`abbreviation`) VALUES ('"+comp_id+"','"+comp_name+"','"+country_name+"','"+country_code+"','"+abbreviation+"') "

query2="INSERT INTO `project1`.`competitor_rankings` (`comp_rank`, `movement`, `points`, `competitions_played`,`competitor_id`) VALUES ('"+str(rank)+"','"+str(movement)+"','"+str(points)+"','"+str(comp_played)+"','"+str(comp_id)+"')"

dbwrite(query1)

dbwrite(query2)
'''