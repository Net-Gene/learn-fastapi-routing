import inspect
from typing import List, Type

from pydantic import ValidationError, BaseModel
from datetime import datetime

import models
from mapper.base_profile import BaseProfile


class OrderProfile(BaseProfile):
    exclude = ['metadata', 'registry']

    def __init__(self, dst_type: Type[BaseModel]):
        self.dst_type = dst_type

    def map(self, data: models.Orders):
        significant_vars = self._get_significant_vars(data)

        # Muunna päivämäärä-aika-kentät (esim. luotu_päivämäärä) päivämäärä-aika-objekteiksi tarvittaessa

        if 'created_date' in significant_vars:
            significant_vars['created_date'] = self._convert_to_datetime(significant_vars['created_date'])

        if 'confirmed_date' in significant_vars and significant_vars['confirmed_date']:
            significant_vars['confirmed_date'] = self._convert_to_datetime(significant_vars['confirmed_date'])

        if 'removed_date' in significant_vars and significant_vars['removed_date']:
            significant_vars['removed_date'] = self._convert_to_datetime(significant_vars['removed_date'])

        try:
            # Yritä luoda OrderDto-objekti

            order_dto = self.dst_type(**significant_vars)
        except ValidationError as e:
            # Käsittele vahvistusvirhettä sulavasti

            return {"error": f"Validation failed: {e.errors()}"}

        return order_dto

    def map_list(self, data: List[models.Orders]):
        items = []
        for row in data:
            significant_vars = self._get_significant_vars(row)
            # Sama päivämäärän ja ajan muunnos kuin kartassa

            if 'created_date' in significant_vars:
                significant_vars['created_date'] = self._convert_to_datetime(significant_vars['created_date'])

            if 'confirmed_date' in significant_vars and significant_vars['confirmed_date']:
                significant_vars['confirmed_date'] = self._convert_to_datetime(significant_vars['confirmed_date'])

            if 'removed_date' in significant_vars and significant_vars['removed_date']:
                significant_vars['removed_date'] = self._convert_to_datetime(significant_vars['removed_date'])

            try:
                # Yritä luoda OrderDto-objekti

                items.append(self.dst_type(**significant_vars))
            except ValidationError as e:
                # Käsittele vahvistusvirhettä sulavasti

                return {"error": f"Validation failed: {e.errors()}"}

        return items

    def _convert_to_datetime(self, date_str):
        """Helper function to convert string to datetime"""
        if date_str == "CURRENT_TIMESTAMP":
            return datetime.now()  # Käytä nykyistä päivämäärää ja aikaa

        if isinstance(date_str, str):
            try:
                # Kokeile jäsentää ISO 8601 -muotoa (T ja sekuntien murto-osat)

                return datetime.fromisoformat(date_str)
            except ValueError:
                # Varajäsenen manuaaliseen muotoon

                return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        return date_str

    def _get_significant_vars(self, data):
        def _pascal_to_snake_case(pascal_str: str) -> str:
            return ''.join(['_' + c.lower() if c.isupper() else c for c in pascal_str]).lstrip('_')

        fields = {}

        # Kerää kohdeobjektin attribuutit

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
