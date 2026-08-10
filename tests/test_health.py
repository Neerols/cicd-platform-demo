import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.main import app


def client():
    app.testing = True
    return app.test_client()


def test_health():
    c = client()
    resp = c.get("/health")
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "ok"


def test_index():
    c = client()
    resp = c.get("/")
    assert resp.status_code == 200
    assert "message" in resp.get_json()


def test_version():
    c = client()
    resp = c.get("/version")
    assert resp.status_code == 200
    assert "version" in resp.get_json()


def test_fail_endpoint():
    c = client()
    resp = c.get("/fail")
    assert resp.status_code == 500
