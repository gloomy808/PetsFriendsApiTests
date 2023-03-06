import requests
import json
from requests_toolbelt.multipart.encoder import MultipartEncoder

class PetFriends:
    def __init__(self):
        self.base_url = "https://petfriends.skillfactory.ru"

    def get_api_key(self, email, password):
        """Метод делает запрос к API сервера и возвращает статус запроса и результат в формате
                JSON с уникальным ключем пользователя, найденного по указанным email и паролем"""
            headers = {'email': email, 'password': password}
            res = requests.get(self.base_url+'/api/key', headers=headers)
            status = res.status_code
            result = ""
            try:
                result = res.json()
            except:
                result = res.text
            return status, result

    def get_list_of_pets(self, auth_key, filter):
        """Метод делает запрос к API сервера и возвращает статус запроса и результат в формате JSON
               со списком наденных питомцев, совпадающих с фильтром. На данный момент фильтр может иметь
               либо пустое значение - получить список всех питомцев, либо 'my_pets' - получить список
               собственных питомцев"""
        headers = {'auth_key': auth_key['key']}
        filter = {'filter': filter}

        res = requests.get(self.base_url+'/api/pets', headers=headers, params=filter)
        status = res.status_code
        print(auth_key)
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def add_new_pet(self, auth_key: json, name: str, animal_type: str, age: str, pet_photo: str) -> json:
        """В данном методе отправляем(POST) на сервер данные о добавленном питомце
        и возвращаем статус запроса и результат на сервер в формате JSON с данными добавленного питомца"""
        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age,
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        res = requests.post(self.base_url+'/api/pets', headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
            print(result)
        return status, result

    def update_pet_info(self, auth_key: json, pet_id: str, name: str, animal_type: str, age: str) -> json:
        """В данном методе отправляем(PUT) запрос на сервер об обновлении данных питомца по указанному pet_id
        и возвращаем статус запроса и результат на сервер в формате JSON с обновленными данными питомца"""
        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age,
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        res = requests.put(self.base_url + '/api/pets/' + pet_id, headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def delete_pet(self, auth_key: json, pet_id: str) -> json:
        """В данном методе отправляем(DELETE) запрос на сервер об удалении питомца по указанному pet_id"""

        headers = {'auth_key': auth_key['key']}

        res = requests.delete(self.base_url + '/api/pets/' + pet_id, headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def add_new_pet_simple(self, auth_key: json, name: str, animal_type: str, age: str) -> json:
        """В данном методе отправляем(POST) на сервер данные о добавленном питомце без фото
        и возвращаем статус запроса и результат на сервер в формате JSON с данными добавленного питомца"""
        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        res = requests.post(self.base_url+'/api/create_pet_simple', headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
            print(result)
        return status, result


    def set_photo_pet(self, auth_key: json, pet_id: str, pet_photo: str) -> json:
        """В данном методе отправляем(DELETE) запрос на сервер об удалении питомца по указанному pet_id"""
        data = MultipartEncoder(
            fields={
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        res = requests.post(self.base_url + '/api/pets/set_photo/' + pet_id, headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result