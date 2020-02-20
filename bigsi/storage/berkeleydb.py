from bigsi.storage.base import BaseStorage
from bigsi.constants import DEFAULT_BERKELEY_DB_STORAGE_CONFIG
from bsddb3 import db
import os

class BerkeleyDBStorage(BaseStorage):
    @staticmethod
    def get_db_open_mode(storage_config):
        open_flag = storage_config.get("flag", "r")
        open_flag_is_valid = open_flag in "cr"
        assert open_flag_is_valid

        if open_flag == "c":
            return db.DB_CREATE
        else:
            return db.DB_RDONLY


    def __init__(self, storage_config=None):
        if storage_config is None:
            storage_config = DEFAULT_BERKELEY_DB_STORAGE_CONFIG
        self.storage_config = storage_config

        self.storage = db.DB()

        GB = 1024 * 1024 * 1024
        self.storage.set_cachesize(
            int(storage_config.get("hashsize", 204800) / GB),
            int(storage_config.get("hashsize", 204800) % GB))

        db_open_mode = BerkeleyDBStorage.get_db_open_mode(storage_config)

        self.storage.open(storage_config["filename"], None, db.DB_HASH, db_open_mode)

    def __repr__(self):
        return "berkeleydb Storage"

    def delete_all(self):
        self.storage.close()
        try:
            os.remove(self.storage_config["filename"])
        except FileNotFoundError:
            pass
        BerkeleyDBStorage.__init__(self, storage_config=self.storage_config)

    def sync(self):
        self.storage.sync()
