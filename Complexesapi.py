# Complexes

import requests

from dbconnection_project1 import dbwrite

url = "https://api.sportradar.com/tennis/trial/v3/en/complexes.json?api_key=UIHu7awT0hFy9PmXnCx27EOdLWksoz8yrB3z8WsD"

headers = {"accept": "application/json"}

response = requests.get(url, headers=headers)

print(response.status_code)
if response.status_code==200:
    data=response.json()
    l2=data.get("complexes")
    def escape_single_quotes(text):
        if text:
            return text.replace("'", "''")  # Replace single quotes with two single quotes
        return text
    def escape_hi_quotes(text):
        if text:
            return text.replace("-", " ")  
        return text
    for item in l2:
        id=item.get("id")
        name=item.get("name")
        
           
        
        escape_name=escape_single_quotes(name)
        query1="INSERT INTO `project1`.`complexes` (`complex_id`,`complex_name`) VALUES ('"+id+"','"+escape_name+"') "
        
        dbwrite(query1)
        
        venues=item.get("venues")
        if venues:
            for items in venues:
                ven_id=items.get("id")
                ven_name=items.get("name")
                venue_name=escape_single_quotes(ven_name)
                
                city_name=items.get("city_name")
                
                country_name=items.get("country_name")
                country_code=items.get("country_code")
                timezone=items.get("timezone")  
            
                hi_name=escape_single_quotes(city_name)
                query2="INSERT INTO `project1`.`venues` (`venue_id`, `venue_name`, `city_name`, `country_name`, `country_code`,`timezone`,`complex_id`) VALUES ('"+ven_id+"','"+venue_name+"','"+hi_name+"','"+country_name+"','"+country_code+"','"+timezone+"','"+id+"')"
               

                #query2="INSERT INTO `project1`.`venues` (`venue_id`, `venue_name`, `city_name`, `country_name`, `country_code`,`timezone`,`complex_id`) VALUES ('"+ven_id+"','"+ven_name+"','"+city_name+"','"+country_name+"','"+country_code+"','"+timezone+"','"+id+"')"
                dbwrite(query2)


   
    
        
        
        
        
       
        
        
    


