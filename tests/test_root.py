def test_root(client):
    res = client.get("/")

    assert res.status_code == 200

    assert res.json().get("Documentation") == {
                'Swagger UI': 'http://127.0.0.1:8000/docs', 
                'ReDoc': 'http://127.0.0.1:8000/redoc'
                }
    