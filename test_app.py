import pytest
import app as app_module


@pytest.fixture
def client(tmp_path, monkeypatch):
    test_db = tmp_path / "test_schedule.db"

    monkeypatch.setattr(
        app_module,
        "DATABASE",
        str(test_db),
    )

    app_module.init_db()

    return app_module.app.test_client()


def test_health(client):
    response = client.get("/health")

    assert response.status_code == 201
    assert response.get_json() == {"status": "ok"}


def test_add_schedule(client):
    response = client.post(
        "/add",
        data={
            "subject": "Operating Systems",
            "day": "Wednesday",
            "start": "14:00",
            "end": "15:00",
            "room": "C305",
        },
    )

    assert response.status_code == 302


def test_invalid_schedule_rejected(client):
    response = client.post(
        "/add",
        data={
            "subject": "",
            "day": "Thursday",
            "start": "10:00",
            "end": "11:00",
            "room": "C305",
        },
    )

    assert response.status_code == 400


def test_room_clash_rejected(client):
    first_response = client.post(
        "/add",
        data={
            "subject": "Operating Systems",
            "day": "Thursday",
            "start": "10:00",
            "end": "11:00",
            "room": "C305",
        },
    )

    assert first_response.status_code == 302

    clash_response = client.post(
        "/add",
        data={
            "subject": "Computer Architecture",
            "day": "Thursday",
            "start": "10:30",
            "end": "11:30",
            "room": "C305",
        },
    )

    assert clash_response.status_code == 200
    assert b"Room clash detected" in clash_response.data
