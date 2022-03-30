def test_get_posts(client, test_posts):
    res = client.get('/posts/')
    print(res.json())
    assert res.status_code == 200


def test_create_post(client_authorized):
    res = client_authorized.post('/posts/', json={
        "title": "test title 1",
        "content": "test tontent 1",
        "published": True
    })

    assert res.status_code == 201