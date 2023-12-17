import requests
from pprint import pprint
from urllib.parse import urlencode
import json

with open("token_VK.txt", "r") as file:
    token_VK = file.readline()

class VKAPIclient:
    API_BASE_URL = 'https://api.vk.com/method'
    TOKEN = token_VK

    def __init__(self,user_id):
        self.user_id = user_id
    
    def get_commons_params(self):
        return {
            'access_token':self.TOKEN,
            'v': '5.199'}
    
    def get_photos(self):
        params = self.get_commons_params()
        params.update({'owner_id':self.user_id, 'album_id':'profile', 'extended':1})
        response = requests.get(f'{self.API_BASE_URL}/photos.get',params=params)
        return response.json()
    
    def photo_url_dict(self):
        photo_info = self.get_photos()
        photo_dict = {}
        json_list = []
        for photo in photo_info['response']['items']:
            for size in photo['sizes']:
                if size['type'] == 'w'and len(photo_dict) < 5:
                    if photo['likes']['count'] not in list(photo_dict.keys()):
                        photo_dict[photo['likes']['count']] = size['url']
                        json_list.append({'file_name':f'{photo['likes']['count']}.jpg', 'size':size['type']})
                    else:
                        photo_dict[(f'{photo['likes']['count']} {photo['date']}')] = size['url']
                        json_list.append({'file_name':f'{photo['likes']['count']} {photo['date']}.jpg', 'size':size['type']})
                elif size['type'] == 'z'and len(photo_dict) < 5:
                    if photo['likes']['count'] not in list(photo_dict.keys()):
                        photo_dict[photo['likes']['count']] = size['url']
                        json_list.append({'file_name':f'{photo['likes']['count']}.jpg', 'size':size['type']})  

        with open("photo_file.json", "w") as write_file:
            json.dump(json_list, write_file)
    
        return photo_dict
    
class YaDiskClient:
    API_BASE_URL = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
    
    def __init__(self,token):
        self.token = token

    def create_folder(self):
        params = {'path':'SavePhoto'}
        headers = {'Authorization': f'OAuth {self.token}'}
        response = requests.put('https://cloud-api.yandex.net/v1/disk/resources',params=params,headers=headers)
        print (f"Создана папка:SavePhoto") 

    def upload_photo(self, url, name):

        params = {'url':f'{url}','path': f'SavePhoto/{name}.jpg', 'overwrite': 'false' }
        headers = {'Authorization': f'OAuth {self.token}'}
        response = requests.post(self.API_BASE_URL,params=params,headers=headers) 
        print (f'Фотография {name} загружена в папку SavePhoto')

               
def save_photo(id_client,token):
    vk_client = VKAPIclient(id_client)
    disk = YaDiskClient(token)
    photo_dict = vk_client.photo_url_dict()
    disk.create_folder()
    for photo in photo_dict:
        disk.upload_photo(photo_dict[photo],photo)
      

if __name__ == '__main__':
    with open("token_YD.txt", "r") as file:
        token_YD = file.readline()
    save_photo(26373730,token_YD)
    