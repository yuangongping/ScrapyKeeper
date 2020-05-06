# -*- coding: utf-8 -*-
from ScrapyKeeper.model.DataStorage import DataStorage


class DataStorageSrv:
    def add(self, args: dict):
        return DataStorage.save(args)
