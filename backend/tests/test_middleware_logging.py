import os
import time
import logging
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_logging_middleware_invoked(caplog):
    with caplog.at_level(logging.INFO):
        response = client.get("/")
        assert response.status_code == 200

        log_found = any("status_code" in record.message for record in caplog.records)
        assert log_found, "LoggingMiddleware did not emit expected log"

@pytest.mark.asyncio
async def test_startup_log_emitted(caplog):
    with caplog.at_level(logging.INFO):
        async with app.router.lifespan_context(app):
            pass
        assert any("Application startup complete." in r.message for r in caplog.records)

def test_cors_headers_present():
    origin = "http://example.com"
    response = client.options(
        "/",
        headers={
            "Origin": origin,
            "Access-Control-Request-Method": "GET",
        },
    )
    assert response.status_code == 200
    assert response.headers.get("access-control-allow-origin") == origin

def test_log_written_to_file():
    log_file = "backend/logs/app.log"

    # Make sure a log is generated
    client.get("/")
    time.sleep(0.1)  # Ensure log flush

    assert os.path.exists(log_file)
    with open(log_file) as f:
        content = f.read()
        assert "status_code" in content
