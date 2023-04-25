import requests

#default bin_id: 'B2_1'
#default bin_password: '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92'
#receiver = student id
#type is a number. 1 = plastic, 2 = paper, 3 = metal, 4 = trash

def send_to_server(bin_id, bin_password, receiver, trash_type, image, success):
    url = 'https://recycling.student.isf.edu.hk:81/ngrecycle'
    myobj = {'bin_id': bin_id, 'bin_password': bin_password, 'receiver_id': receiver, 'type': str(trash_type), "image": image, 'success': succes}
s
    x = requests.post(url, json = myobj, verify=False)

    print(x.content)

    if x.text == '{"results" : "success"}':
        return True
    else:
        return False

