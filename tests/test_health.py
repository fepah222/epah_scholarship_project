def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "ok"
    assert data["application"] == "Epah Scholarship"
    assert data["database"] == "sqlite"


def test_homepage_loads(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Epah Scholarship" in response.data


def test_public_scholarship_directory_loads(client):
    response = client.get("/scholarships/")
    assert response.status_code == 200


def test_unknown_institution_profile_returns_404_not_server_error(client):
    response = client.get("/institutions/does-not-exist")
    assert response.status_code == 404
