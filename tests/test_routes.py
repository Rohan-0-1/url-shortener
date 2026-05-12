import pytest

import shortener as sh
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@pytest.fixture(autouse=True)
def reset_store():
    sh.clear()
    yield
    sh.clear()


class TestShortenRoute:
    def test_valid_url_returns_200(self, client):
        res = client.post("/shorten", json={"url": "https://example.com"})
        assert res.status_code == 200

    def test_response_contains_code(self, client):
        res = client.post("/shorten", json={"url": "https://example.com"})
        data = res.get_json()
        assert "code" in data
        assert len(data["code"]) == 6

    def test_response_contains_short_url(self, client):
        res = client.post("/shorten", json={"url": "https://example.com"})
        data = res.get_json()
        assert "short_url" in data
        assert data["short_url"].startswith("/")

    def test_missing_body_returns_400(self, client):
        res = client.post("/shorten")
        assert res.status_code == 400

    def test_missing_url_field_returns_400(self, client):
        res = client.post("/shorten", json={"link": "https://example.com"})
        assert res.status_code == 400

    def test_empty_url_returns_400(self, client):
        res = client.post("/shorten", json={"url": "   "})
        assert res.status_code == 400

    def test_same_url_returns_same_code(self, client):
        url = "https://example.com"
        res1 = client.post("/shorten", json={"url": url})
        res2 = client.post("/shorten", json={"url": url})
        assert res1.get_json()["code"] == res2.get_json()["code"]

    def test_different_urls_return_different_codes(self, client):
        res1 = client.post("/shorten", json={"url": "https://github.com"})
        res2 = client.post("/shorten", json={"url": "https://gitlab.com"})
        assert res1.get_json()["code"] != res2.get_json()["code"]


class TestRedirectRoute:
    def test_valid_code_returns_302(self, client):
        res = client.post("/shorten", json={"url": "https://example.com"})
        code = res.get_json()["code"]
        redirect_res = client.get(f"/{code}")
        assert redirect_res.status_code == 302

    def test_valid_code_redirects_to_original_url(self, client):
        url = "https://example.com"
        res = client.post("/shorten", json={"url": url})
        code = res.get_json()["code"]
        redirect_res = client.get(f"/{code}")
        assert redirect_res.location == url

    def test_unknown_code_returns_404(self, client):
        res = client.get("/unknwn")
        assert res.status_code == 404

    def test_404_response_contains_error_message(self, client):
        res = client.get("/unknwn")
        data = res.get_json()
        assert "error" in data
