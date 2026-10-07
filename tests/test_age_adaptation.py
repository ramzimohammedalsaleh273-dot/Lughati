from app.age_adaptation import AGE_GROUPS,age_guidance,adapt_activity

def test_age_adaptation():
    assert len(AGE_GROUPS)==5
    for age in AGE_GROUPS:
        assert age_guidance(age,"ar")
        assert age_guidance(age,"en")
        assert "التكييف العمري" in adapt_activity("نشاط",age,"ar")
