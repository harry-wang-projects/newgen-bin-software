import requests
import pickle
import base64

#default bin_id: 'B2_1'
#default bin_password: '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92'
#receiver = student id
#type is a number. 1 = plastic, 2 = paper, 3 = metal, 4 = trash

id_default = "B2_1"
password_default = "8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92"


def send_to_server(bin_id, bin_password, receiver, trash_type, image, weight, success):

    pickle_img = pickle.dumps(image)
    sending = base64.b64encode(pickle_img).decode('ascii')

    print("id:", receiver)
    print("type:", type(receiver))

    url = 'https://recycling.student.isf.edu.hk:81/ngrecycle'
    myobj = {'bin_id': bin_id, 'bin_password': bin_password, 'receiver_id': receiver, 'type': str(trash_type), "image": sending, 'weight': str(weight), 'success': str(success)}
    x = requests.post(url, json = myobj, verify=False)

    print("results:")
    print(x.content)

    if x.text == '{"results" : "success"}':
        return True
    else:
        return False

def send_to_server_new(bin_id, bin_password, receiver, trash_type, weight, success):
    img_array = get_pic_array()


    url = 'https://recycling.student.isf.edu.hk:81/ngrecycle'
    myobj = {'bin_id': bin_id, 'bin_password': bin_password, 'receiver_id': receiver, 'type': str(trash_type), "image": base64.b64encode(img_array).decode('ascii'), 'weight': str(weight), 'success': str(success)}
    x = requests.post(url, json = myobj, verify=False)

    print("results:")
    print(x.content)

    if x.text == '{"results" : "success"}':
        return True
    else:
        return False

#send_to_server(id_default, password_default, "0012113", 2, "sdfa", 12, 1)
