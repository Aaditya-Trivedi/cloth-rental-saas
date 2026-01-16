class ShopDatabaseRouter:
    """
    Routes shop app models to dynamically assigned shop databases
    """

    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'shop':
            return hints.get('shop_db')
        return 'default'

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'shop':
            return hints.get('shop_db')
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, **hints):
        if app_label == 'shop':
            return db != 'default'
        return db == 'default'
