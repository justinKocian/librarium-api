import os
from pathlib import Path
from tests.test_factory import create_admin

UPLOADS_DIR = Path("/app/uploads")
TEMP_FILE = Path("/app/tests/test_cover.jpg")

def test_upload_cover_image(client):
    headers = create_admin(client)

    # Create dummy image file
    TEMP_FILE.write_bytes(os.urandom(1024))

    with open(TEMP_FILE, "rb") as f:
        res = client.post("/upload/cover", files={"file": ("test_cover.jpg", f)}, headers=headers)

    assert res.status_code == 200
    data = res.json()

    assert "cover_path" in data
    uploaded_path = Path("/app") / data["cover_path"]
    assert uploaded_path.exists()

    # Cleanup
    uploaded_path.unlink(missing_ok=True)
    TEMP_FILE.unlink(missing_ok=True)
