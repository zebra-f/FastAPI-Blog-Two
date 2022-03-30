def test_get_posts(client):
    res = client.get('/posts/')

    assert res.status_code == 200


def test_create_post(client_authorized):
    res = client_authorized.post('/posts/', json={
        "title": "Test Title 1",
        "content": "Test Content 1",
        "published": True
    })

    assert res.status_code == 201