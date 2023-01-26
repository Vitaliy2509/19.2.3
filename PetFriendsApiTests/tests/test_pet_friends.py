from api import PetFriends
from settings import valid_email, valid_password, n_email, n_password, n_auth_key, neg_auth_key
import os

pf = PetFriends()
def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result
def test_get_all_pets_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0

def test_add_new_pet_with_valid_data(name='Барбоскин', animal_type='двортерьер',
                                     age='4', pet_photo='images/Photo.jpg'):

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert result['name'] == name

def test_successful_delete_self_pet():

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/Photo-0005.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert status == 200
    assert pet_id not in my_pets.values()

def test_successful_update_self_pet_info(name='Мурзик', animal_type='Котэ', age=5):

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("There is no my pets")

def test_add_new_pet_without_photo_valid_data(name="Муха", animal_type="кошка", age="5"):

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    assert status == 200
    assert result["name"] == name


def test_set_photo_pet(pet_photo="images/Photo-0005.jpg"):

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets["pets"]) > 0:
        status, result = pf.set_photo_pet(auth_key, my_pets["pets"][0]["id"], pet_photo)

        assert status == 200
        assert result["pet_photo"]
    else:
        raise Exception("No pets")

def test_get_api_key_for_data_user_empty(email=n_email, password=n_password):

    status, result = pf.get_api_key(email, password)

    assert status == 403
    assert "key" not in result


def test_get_api_key_for_password_user_empty(email=valid_email, password=n_password):

    status, result = pf.get_api_key(email, password)

    assert status == 403
    assert "key" not in result

def test_get_all_pets_with_empty_key(filter=""):

    status, result = pf.get_list_of_pets(n_auth_key, filter)

    assert status == 403


def test_get_all_pets_with_incorrect_key(filter=""):

    status, result = pf.get_list_of_pets(neg_auth_key, filter)

    assert status == 403


def test_add_new_pet_empty_data(name="", animal_type="", age="", pet_photo="images/Photo-0083.jpg"):

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert result["name"] == name

def test_add_new_pet_incorrect_age(name="Том", animal_type="мышка", age="-1", pet_photo="images/Photo.jpg"):

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert result["age"] == age
def test_delete_not_your_pet():

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, all_pets = pf.get_list_of_pets(auth_key, "")

    if len(all_pets["pets"]) > 0:
        pet_id = all_pets["pets"][0]["id"]
        status, _ = pf.delete_pet(auth_key, pet_id)

        assert status == 200
        assert pet_id not in all_pets.values()
    else:
        raise Exception("No pets")

def test_add_new_pet_without_photo_empty_data(name="", animal_type="", age=""):

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200
    assert result["name"] == name
def test_update_not_your_pet_info(name="<Бонни>", animal_type="маус", age="1"):

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, all_pets = pf.get_list_of_pets(auth_key, "")

    if len(all_pets["pets"]) > 0:
        status, result = pf.update_pet_info(auth_key, all_pets["pets"][0]["id"], name, animal_type, age)

        assert status == 200
        assert result["name"] == name
    else:
        raise Exception("No pets")