from app.database import init_db
from app.seed import seed_content
from app.auth import set_parent_pin,verify_parent_pin,parent_pin_enabled
from app.services import get_child

def test_parent_pin_roundtrip():
    init_db(); seed_content()
    assert set_parent_pin("1234")
    assert parent_pin_enabled()
    assert verify_parent_pin("1234")
    assert not verify_parent_pin("9999")

def test_selected_child_exists():
    init_db(); seed_content()
    c=get_child()
    assert c and c.id>0
