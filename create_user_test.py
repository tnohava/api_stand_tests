
import sender_stand_request
import data

def get_user_body(first_name):
    current_body = data.user_body.copy()
    current_body["firstName"] = first_name
    return current_body

def positive_assert(first_name):
    user_body = get_user_body(first_name)

    user_response = sender_stand_request.post_new_user(user_body)

    assert user_response.status_code == 201

    response_json = user_response.json()
    assert "authToken" in response_json
    assert response_json["authToken"] != ""

    users_table_response = sender_stand_request.get_users_table()
    assert users_table_response.status_code == 200

    str_user = (
        user_body["firstName"] + "," +
        user_body["phone"] + "," +
        user_body["address"] + ",,," +
        response_json["authToken"]
    )

    assert users_table_response.text.count(str_user) == 1

def test_create_user_2_letter_in_first_name_get_success_response():
    positive_assert("Aa")


def negative_assert_symbol(first_name):
    user_body = get_user_body(first_name)

    response = sender_stand_request.post_new_user(user_body)

    print("Código recibido:", response.status_code)
    print("Respuesta del servidor:", response.text)

    assert response.status_code == 400

    assert response.json()["code"] == 400

    assert response.json()["message"] == (
        "Has introducido un nombre de usuario no válido. "
        "El nombre solo puede contener letras del alfabeto latino, "
        "la longitud debe ser de 2 a 15 caracteres."
    )

def negative_assert_no_firstname(user_body):
    response = sender_stand_request.post_new_user(user_body)

    assert response.status_code == 400, (
        f"Se esperaba 400, pero se obtuvo "
        f"{response.status_code}: {response.text}"
    )

# PRUEBA 2: Nombre con 15 letras
def test_create_user_15_letters_get_success_response():
    positive_assert("A" * 15)


# PRUEBA 3: Nombre con 1 letra
def test_create_user_1_letter_get_error_response():
    negative_assert_symbol("A")


# PRUEBA 4: Nombre con 16 letras
def test_create_user_16_letters_get_error_response():
    negative_assert_symbol("A" * 16)


# PRUEBA 5: Nombre con espacio
def test_create_user_with_space_get_error_response():
    negative_assert_symbol("A A")


# PRUEBA 6: Nombre con símbolo especial
def test_create_user_with_symbol_get_error_response():
    negative_assert_symbol("A@a")


# PRUEBA 7: Nombre con un número
def test_create_user_with_number_get_error_response():
    negative_assert_symbol("A1a")


# PRUEBA 8: Sin el campo firstName
def test_create_user_without_firstname_get_error_response():
    user_body = data.user_body.copy()
    user_body.pop("firstName", None)

    negative_assert_no_firstname(user_body)


# PRUEBA 9: Nombre vacío
def test_create_user_empty_first_name_get_error_response():
    user_body = get_user_body("")
    negative_assert_no_firstname(user_body)

# PRUEBA 10: Nombre de tipo numérico
def test_create_user_number_type_get_error_response():
    user_body = get_user_body(123)

    negative_assert_no_firstname(user_body)
