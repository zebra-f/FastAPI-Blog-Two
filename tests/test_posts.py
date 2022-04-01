from app import schemas


def test_get_posts(client, test_posts):
    response = client.get('/posts/')

    assert len(response.json()) == len(test_posts)
    assert response.status_code == 200

    posts_map = map(lambda post: schemas.PostResponse(**post), response.json())

    i = 0
    for post in posts_map:
        assert post.user_id == test_posts[i].user_id
        assert post.title == test_posts[i].title
        assert post.content == test_posts[i].content
        i += 1

    
def test_create_post(client_authorized):
    response = client_authorized.post('/posts/', json={
        "title": "test title 1",
        "content": "test tontent 1",
        "published": True
    })

    assert response.status_code == 201


def test_get_post(client, test_posts):
    
    for post in test_posts:
        response = client.get(f'/posts/{post.id}')
        
        assert response.status_code == 200
        
        post_response = schemas.PostResponse(**response.json())
        assert post_response.id == post.id        


# AUTHENTICATION
def test_delete_post(client_authorized, test_posts):
    
    for post in test_posts:
        response = client_authorized.delete(f'/posts/{post.id}')
        
        assert response.status_code == 204


# AUTHENTICATION
def test_update_post(client_authorized, test_posts):
    
    for post in test_posts:
        response = client_authorized.put(f'/posts/{post.id}', json={
            "title": post.title + " updated",
            "content": post.content + " updated",
            "published": not post.published
        })
        
        assert response.status_code == 201

        post_response = schemas.PostResponse(**response.json())
        assert post_response.title == post.title
        assert post_response.content == post.content
        assert post_response.published == post.published