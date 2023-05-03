import requests 
import json

class Trashitem:
  def __init__(self, trash_id, name, tokens, minweight, maxweight):
    self.trash_id = trash_id
    self.name = name
    self.tokens = tokens
    self.minweight = minweight
    self.maxweight = maxweight  
  def __str__(self):
    return str(self.trash_id) + self.name + str(self.tokens) + str(self.minweight) + str(self.maxweight)
 
trash_list = []

def get_all_trash(): 
  url = 'https://recycling.student.isf.edu.hk:81/nglist'
  myobj = {'get_type': 'trash', 'sessionid': '123'}
  x = requests.post(url, json = myobj, verify=False)

  print(x.content)
  
  decoded_thing = json.loads(x.content)

  for i in range(len(decoded_thing["results"])):
    get_class = decoded_thing["results"][i]
    trash_list.append(Trashitem(get_class["item_id"], get_class["item_name"], get_class["bucks_change"], get_class["min_weight"], get_class["max_weight"]))

def get_all_trash_manual():
    trash_list.append(Trashitem(0, "Nothing", 0, 1, 10))
    trash_list.append(Trashitem(1, "Metal", 10, 1, 10))
    trash_list.append(Trashitem(2, "Paper", 10, 1, 10)) 
    trash_list.append(Trashitem(3, "Plastic", 10, 1, 10))
    trash_list.append(Trashitem(4, "Trash", 0, 1, 10))


#get_all_trash()
get_all_trash_manual()
for i in range (len(trash_list)):
  print(trash_list[i])
