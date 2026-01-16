import os
import copy
from django.conf import settings
from django.core.management import call_command

def create_shop_database(db_name):
    """
    Create SQLite DB file, register it in settings, and apply migrations
    """

    shop_db_path = settings.BASE_DIR / 'shop_dbs'
    os.makedirs(shop_db_path, exist_ok=True)

    db_file = shop_db_path / f"{db_name}.sqlite3"

    if not os.path.exists(db_file):
        open(db_file, 'a').close()

    # 🔑 REGISTER DB TEMPORARILY FOR MANAGEMENT COMMANDS
    default_db = settings.DATABASES['default']
    settings.DATABASES[db_name] = copy.deepcopy(default_db)
    settings.DATABASES[db_name]['NAME'] = db_file

    # APPLY MIGRATIONS
    call_command(
        'migrate',
        'shop',
        database=db_name,
        interactive=False,
        verbosity=1
    )
