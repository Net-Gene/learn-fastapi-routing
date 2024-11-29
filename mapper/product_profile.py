import inspect
from typing import Type, List

from pydantic import BaseModel

import models
from mapper.base_profile import BaseProfile


class ProductProfile(BaseProfile):
    exclude = ['CategoryId', 'metadata', 'registry']

    def __init__(self, dst_type: Type[BaseModel]):
        self.dst_type = dst_type

    def map(self, data: models.Products):
        significant_vars = self._get_significant_vars(data)
        product_dto = self.dst_type(**significant_vars)

        return product_dto

    # listan objekteja muuttaminen
    def map_list(self, data: List[models.Products]):
        items = []

        for row in data:
            significant_vars = self._get_significant_vars(row)
            items.append(self.dst_type(**significant_vars))
        return items

    def _get_significant_vars(self, data):
        def _pascal_to_snake_case(pascal_str: str) -> str:
            return ''.join(['_' + c.lower() if c.isupper() else c for c in pascal_str]).lstrip('_')

        fields = {}

        # Kerää kohteen attribuutit
        for key, value in inspect.getmembers(data):
            if not key.startswith('__') and not key.startswith('_') and not callable(value) and key not in self.exclude:
                fields[key] = type(value)

        # Muunna kenttien nimet ja kerää merkittäviä muuttujia
        v = vars(data)
        significant_vars = {}
        for key, value in v.items():
            if key not in fields:
                continue
            snake_case_key = _pascal_to_snake_case(key)
            significant_vars[snake_case_key] = value

        return significant_vars

