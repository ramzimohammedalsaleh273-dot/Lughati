from pathlib import Path
from PySide6.QtCore import QUrl
from PySide6.QtQml import QQmlApplicationEngine
from app.mobile_backend import AppBackend

def create_qml_app(app):
    engine=QQmlApplicationEngine()
    backend=AppBackend()
    engine.rootContext().setContextProperty("appBackend",backend)
    qml=Path(__file__).resolve().parents[1]/"qml"/"Main.qml"
    engine.load(QUrl.fromLocalFile(str(qml)))
    if not engine.rootObjects():
        raise RuntimeError("تعذر تحميل واجهة لغتي")
    app._qml_engine=engine
    app._backend=backend
    return app
