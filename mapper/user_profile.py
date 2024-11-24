import inspect
from typing import Type, List

from pydantic import BaseModel

import models
from mapper.base_profile import BaseProfile


class UserProfile(BaseProfile):
    # Miksi exclude on __init__:n ulkopuolella?
    # initin ulkopuolella olet jäasenmuuttujat ovat staattisia (samoja kaikille instansseilel)
    exclude = ['HashedPassword', 'PasswordSalt', 'metadata', 'registry']

    # Type[BaseModel] tarkoittaa, että dst_type-muuttuja on itse tietotyyppi,
    # eikä BaseModel-tietotyyppinen muuttuja (instanssi)

    # BaseModel kattaa kaikki meidän Dto-objektit,
    # koska ne kaikki perivät Pydanticin BaseModel-luokan
    def __init__(self, dst_type: Type[BaseModel]):
        self.dst_type = dst_type

    # yksittäisen objektin muuttaminen
    def map(self, data: models.Users):
        significant_vars = self._get_significant_vars(data)
        # tässä luodaan self.dst_type:n tyyppinen instanssi alukuperäisen model instanssin tiedoilla
        # ja palautetaan se
        user_dto = self.dst_type(**significant_vars)

        return user_dto

    # listan objekteja muuttaminen
    def map_list(self, data: List[models.Users]):
        items = []

        for row in data:
            significant_vars = self._get_significant_vars(row)
            # tässä luodaan self.dst_type:n tyyppinen instanssi alukuperäisen model instanssin tiedoilla
            # ja lisätään se lisaan
            items.append(self.dst_type(**significant_vars))
        return items

    def _get_significant_vars(self, data):
        fields = {}
        # inspect.getmembetrs(data) hakee kaikki datan sisältämät muuttujat ja metodit. Ne ovat dictionaryssa

        for key, value in inspect.getmembers(data):
            # jos muuttuja  on private (alkaa __ tai _) se jätetään listauksesta ulkopuolelle
            # samoin, jos member on metodi (callable)
            # samoin jos muuttuja on exclude-listassa
            if not key.startswith('__') and not key.startswith('_') and not callable(
                    value) and key not in self.exclude:
                # lisätään fields-dictionaryyn kaikki julkiset muuttujat sekä niiden tyypit
                # koska tietokannassa kentät ovat CamelCasingilla, muutetaan ne alkamaan pienillä kirjaimilla

                fields[key.lower()] = type(value)

        v = vars(data)
        significant_vars = {}
        for key, value in v.items():
            # jos objektin muuttuja ei ole fields-dictionaryssa, sitä ei oteta listaukseen mukaan
            # eli hypätään se yli
            if key.lower() not in fields:
                continue
            significant_vars[key.lower()] = value
        return significant_vars
