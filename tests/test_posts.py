from app import schemas


def test_get_posts(client, test_posts):
    res = client.get('/posts/')

    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200

    posts_list = list(map(lambda post: schemas.PostResponse(**post), res.json()))

    i = 0
    for post in posts_list:
        assert post.user_id == test_posts[i].user_id
        assert post.title == test_posts[i].title
        assert post.content == test_posts[i].content
        i += 1

    


def test_create_post(client_authorized):
    res = client_authorized.post('/posts/', json={
        "title": "test title 1",
        "content": "test tontent 1",
        "published": True
    })

    assert res.status_code == 201