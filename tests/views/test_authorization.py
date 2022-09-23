

def test_index_page__not_logged_in(client):
    res = client.get('/favorites/movies')
    assert res.status_code == 401


def test_index_page__logged_in(client):
    with client:
        client.post('auth/login', data=dict(email='test@mail.com', password='qwertY'))
        res = client.get('/favorites/movies')
        assert res.status_code == 200
