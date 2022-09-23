from flask import request


def test_root_status(test_client) -> None:
    """ Checking whether the desired status code is obtained """
    response = test_client.get('/', follow_redirects=True)
    assert response.status_code == 200, "Status code is wrong"


def test_users_status(test_client) -> None:
    """ Checking whether the desired status code is obtained """
    token = request.headers['Authorization'].split("Bearer ")[-1]
    response = test_client.get('/favorites/movies', headers={f'Authorization: Bearer {token}'}, follow_redirects=True)
    print(request.headers)
    assert response.status_code == 200, "Status code is wrong"
