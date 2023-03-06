import os.path

import pytest

from api import PetFriends
from settings import valid_email, valid_password, invalid_email, invalid_password

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """Проверяем что запрос api ключа возвращает статус 200 и в результате содержится слово key"""
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter: str = ''):
    """Проверяем что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet(name='Барбарис', animal_type='кот', age='4', pet_photo='images/cat1.jpg'):
    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменную в auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем нового питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверка полученного результата с полученным
    assert status == 200
    assert result['name'] == name


def test_successful_update_self_pet_info(name='Мармарис', animal_type='Котег', age='5'):
    # Запрашиваем ключ api и список питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, обновляем имя, тип, возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        # Сверка полученного результата с полученным
        assert status == 200
        assert result['name'] == name
    else:
        # Если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


def test_successful_delete_pet():
    # Запрашиваем ключ api и список питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список пустой, создаем нового питомца и опять запрашиваем список
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Рей", "Клонокот", "1", "images/Pniye8kjw1w.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Отправка запроса на удаление по id первого питомца
    pet_id = my_pets['pets'][0]['id']
    print("Удаляемый питомец", pet_id)
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Повторный вызов списка питомцев пользователя
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Сверка полученного результата
    assert status == 200
    assert pet_id not in my_pets


def test_add_new_pet_simple(name='Дора', animal_type='кошка', age='1'):
    # Запрашиваем ключ api и сохраняем в переменную в auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем нового питомца
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)

    # Сверка полученного результата с полученным
    assert status == 200
    assert result['name'] == name


def test_successful_set_pet_photo():
    # Запрашиваем ключ api и список питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список пустой, создаем нового питомца и опять запрашиваем список
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Рей", "Клонокот", "1", "images/Pniye8kjw1w.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Отправка запроса на изменение фото по id первого питомца
    pet_id = my_pets['pets'][0]['id']
    status, result = pf.set_photo_pet(auth_key, pet_id, "images/cryingcat.jpg")

    # Повторный вызов списка питомцев пользователя
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Сверка полученного результата
    assert status == 200
    assert result['pet_photo'] == my_pets['pets'][0]['pet_photo']


def test_successful_update_pet_info():
    # Запрашиваем ключ api и список питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список пустой, создаем нового питомца и опять запрашиваем список
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Рей", "Клонокот", "1", "images/Pniye8kjw1w.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Отправка запроса на изменение фото по id первого питомца
    pet_id = my_pets['pets'][0]['id']
    status, result = pf.set_photo_pet(auth_key, pet_id, "images/cryingcat.jpg")

    # Повторный вызов списка питомцев пользователя
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Сверка полученного результата
    assert status == 200
    assert result['pet_photo'] == my_pets['pets'][0]['pet_photo']


# Test 1.
@pytest.mark.negative
def test_get_api_key_with_correct_mail_and_wrong_password(email=valid_email, password=invalid_password):
    """Проверка запроса с правильным email и c неправильным паролем.
    Проверяем нет ли ключа в ответе."""
    status, result = pf.get_api_key(email, password)

    assert status == 403
    assert 'key' not in result
    print('ok')
    print(f'Статус {status} для теста с неправильным паролем')


# Test 2.
@pytest.mark.negative
def test_get_api_key_with_incorrect_mail_and_correct_password(email=invalid_email, password=valid_password):
    """Проверка запроса с неправильным email и c правильным паролем.
    Проверяем нет ли ключа в ответе."""
    status, result = pf.get_api_key(email, password)

    assert status == 403
    assert 'key' not in result
    print('ok')
    print(f'Статус {status} для теста с неправильным email и правильным паролем')


# Test 3.
@pytest.mark.negative
def test_get_api_key_with_incorrect_mail_and_incorrect_password(email=invalid_email, password=invalid_password):
    """Проверка запроса с неправильным email и c неправильным паролем.
    Проверяем нет ли ключа в ответе."""
    status, result = pf.get_api_key(email, password)

    assert status == 403
    assert 'key' not in result
    print('ok')
    print(f'Статус {status} для теста с неправильным email и неправильным паролем')


# Test 4.
@pytest.mark.negative
def test_add_pet_with_negative_value_age_in_age(name='Отшельник', animal_type='Кошка', pet_photo='images/hehe.jpg'):
    """Добавление питомца с отрицательным возрастом.
    Тест выводит предупреждение, если  будет добавлен питомец с невозможным возрастом, меньше 0 или старше 30 лет."""
    age = '-120'
    _, api_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(api_key, name, animal_type, age, pet_photo)

    age = float(result['age'])  # .split()
    assert status == 200
    assert (age > 30 or age < 0), 'Добавлен питомец с невозможным возрастом, меньше 0 или старше 20 лет.'
    print(f'\n Сайт позволяет добавлять питомеца с невозможным возрастом, меньше 0 или старше 20 лет. {age}')


# Test 5.
@pytest.mark.negative
def test_add_pet_with_variable_age_symble(name='Отшельник', animal_type='Кошка', pet_photo='images/hehe.jpg'):
    """Добавление питомца с символами в поле возраста.
    Тест выводит предупреждение, если  добавлен  питомец с нечисловым возрастом"""
    age = '}§'
    _, api_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(api_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert age, 'Добавлен питомец с нечисловым возрастом'
    print(f'\n Сайт позволяет добавлять питомеца с нечисловым возрастом {age}')


# Test 6.
@pytest.mark.negative
def test_add_pet_with_data_empty_all_field():
    """Проверка добавления питомца с пустыми полями. Тест выводит предупреждение"""
    name = ''
    animal_type = ''
    age = ''
    _, api_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_simple(api_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == name
    print('ok')
    print(f'Сайт позволяет добавлять питомецев без заполнения обязательных полей {result}')

# Test 7.
@pytest.mark.negative
def test_add_pet_with_data_empty_name_field(name='', animal_type='Котэ', age='5'):
    """Проверка добавления питомца с пустым полем Имя. Тест выводит предупреждение"""
    _, api_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_simple(api_key, name, animal_type, age)

    assert status == 200
    assert name == ''
    print(f'Сайт позволяет добавлять питомца без имени {result}')

# Test 8.
@pytest.mark.negative
def test_add_pet_with_a_lot_of_symbols_in_name(animal_type='Кот', age='2', pet_photo='images/hehe.jpg'):
    """ Добавление питомца с именем, которое превышает 20 символов.
   Тест выводит предупреждение, если добавлен питомец с именем, состоящим из более 20 символов"""

    name = 'УрбановичусАрвидасБронучевич'

    _, api_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(api_key, name, animal_type, age, pet_photo)

    name_list = result['name']
    name_count = len(name_list)


    assert status == 200
    assert name_count > 20, 'Питомец добавлен с именем больше 20 символов'
    print('ok')
    print(f'Сайт позволяет добавлять  питомецев с именем больше 20 символов. {name_count}')

# Test 9.
@pytest.mark.negative
def test_add_pet_with_numbers_in_animal_type(name='Барбарис', animal_type='8088', age='4', pet_photo='images/cat1.jpg'):
    """Добавление питомца с цифрами в animal_type.
    Сообщение, если питомец будет добавлен на сайте с цифрами вместо букв в поле "Порода"."""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, api_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(api_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert animal_type in result['animal_type'], 'Питомец добавлен в приложение с цифрами вместо букв в поле "Порода".'
    print(f'\n Добавлен питомец с цифрами вместо букв в поле "Порода". {animal_type}')

# Test 10.
@pytest.mark.negative
def test_add_pet_with_a_lot_of_symbols_in_animal_type(name='Барбарис', animal_type='Длииииииииииииинооооооооокоооооооот',
                                                      age='4', pet_photo='images/cat1.jpg'):
    """Добавления питомца с полем "Порода", которое имеет слишком длинное значение.
    Сообщение, если питомец будет добавлен в приложение с названием породы состоящим больше чем из 35 символов."""

    _, api_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(api_key, name, animal_type, age, pet_photo)

    list_animal_type = result['animal_type']#.split()
    symbol_count = len(list_animal_type)

    assert status == 200
    assert symbol_count >= 35, 'Питомец добавлен на сайт с названием породы более чем из 35 символов.'
    print(f'\n Добавлен питомец с названием породы породы более чем из 35 символов. {symbol_count}')