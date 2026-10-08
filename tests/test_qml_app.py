def test_qml_frontend_files_exist():
    from pathlib import Path
    root=Path(__file__).resolve().parents[1]
    assert (root/"qml"/"Main.qml").exists()
    assert (root/"app"/"mobile_backend.py").exists()
    assert "ApplicationWindow" in (root/"qml"/"Main.qml").read_text(encoding="utf-8")
