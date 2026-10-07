from app.backup_manager import backup_database_safe,restore_database_safe

def backup_database():
    return backup_database_safe()

def restore_database(source):
    result=restore_database_safe(source)
    return result["database"],result["emergency"]
