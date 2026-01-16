import os
from django.conf import settings
from django.core.management import call_command
from cloth_rental_saas.db_config import load_shop_databases

def create_shop_database(db_name):
    """
    Create SQLite DB file and apply migrations
    """
    db_path = settings.BASE_DIR / 'shop_dbs' / f"{db_name}.sqlite3"

    if not os.path.exists(db_path):
        open(db_path, 'a').close()

    # Reload DB configs before migrate
    load_shop_databases()

    call_command(
        'migrate',
        database=db_name,
        interactive=False,
        verbosity=0
    )
