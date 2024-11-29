import inspect
from typing import Type, List

from pydantic import BaseModel

import models
from mapper.base_profile import BaseProfile


class CategoryProfile(BaseProfile):
    exclude = ['CategoryId', 'metadata', 'registry']

    def __init__(self, dst_type: Type[BaseModel]):
        self.dst_type = dst_type

    def map(self, data: models.Categories):
        significant_vars = self._get_significant_vars(data)
        category_dto = self.dst_type(**significant_vars)

        return category_dto

    # listan objekteja muuttaminen
    def map_list(self, data: List[models.Categories]):
        items = []

        for row in data:
            significant_vars = self._get_significant_vars(row)
            items.append(self.dst_type(**significant_vars))
        return items


    def _get_significant_vars(self, data):
        # Tarkista, onko "data" sanakirja
        if isinstance(data, dict):
            # Suodata pois avaimet, jotka alkavat '_sa_instance_state'
            return {key: value for key, value in data.items() if not key.startswith('_sa_instance_state')}
        
        # Jos se ei ole sanakirja, käsittele SQLAlchemy-ilmentymä tai muu olio
        def _pascal_to_snake_case(pascal_str: str) -> str:
            return ''.join(['_' + c.lower() if c.isupper() else c for c in pascal_str]).lstrip('_')

        # Kerää kohteen attribuutit (jos data on olio, kuten SQLAlchemy-malli)
        fields = {}
        for key, value in inspect.getmembers(data):
            if not key.startswith('__') and not key.startswith('_') and not callable(value) and key not in self.exclude:
                fields[key] = type(value)

        # Käytä SQLAlchemy-ilmentymän attribuutteja
        significant_vars = {}
        if hasattr(data, '__dict__'):  # Varmistetaan, että data on olio, jolla on __dict__
            v = {key: value for key, value in data.__dict__.items() if not key.startswith('_sa_instance_state')}
            for key, value in v.items():
                if key in fields:
                    snake_case_key = _pascal_to_snake_case(key)
                    significant_vars[snake_case_key] = value

        return significant_vars



