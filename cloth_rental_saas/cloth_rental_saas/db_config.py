import copy
from django.conf import settings
from master.models import ShopRegistry

def load_shop_databases():
    """
    Dynamically add shop databases to Django DATABASES
    """
    shop_db_path = settings.BASE_DIR / 'shop_dbs'

    default_db = settings.DATABASES['default']

    for shop in ShopRegistry.objects.filter(is_active=True):
        db_config = copy.deepcopy(default_db)
        db_config['NAME'] = shop_db_path / f"{shop.db_name}.sqlite3"
        settings.DATABASES[shop.db_name] = db_config
