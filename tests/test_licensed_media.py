from app.licensed_media import LICENSED_MEDIA, catalog, get_item
def test_licensed_catalog_has_attribution_and_source():
    assert len(LICENSED_MEDIA)>=3
    for item in LICENSED_MEDIA:
        assert item["id"] and item["url"] and item["source_page"]
        assert item["license"] and item["attribution"]
        assert item["language"] in ("ar","en")
def test_catalog_reports_local_state():
    rows=catalog()
    assert len(rows)==len(LICENSED_MEDIA)
    assert all("downloaded" in row and "local_path" in row for row in rows)
    assert get_item("does_not_exist") is None
