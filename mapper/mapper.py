from typing import Annotated

from fastapi.params import Depends

from dtos.users import UserDto
from mapper.base_profile import BaseProfile
from mapper.profile_factory import create_user_profile


class Mapper:
    # Mapper-luokka sisältää kaikki profile-objektit, sekä map-metodin
    # jossa käytetään profiilikohtaista map / map_list-metodia
    def __init__(self, profiles: dict[str: BaseProfile]) -> None:
        self.profiles = profiles

    def map(self, _type, data):
        if _type not in self.profiles.keys():
            raise Exception('Profile missing')

        if isinstance(data, list):
            return self.profiles[_type].map_list(data)
        else:
            return self.profiles[_type].map(data)


# factory mapperin luomiseen
def create_mapper() -> Mapper:
    # kun sinulle tulee lisää profiileja, lisää ne tähän
    profiles = {
        # UserDto no tietotyyppi, johon tällä profiililla (user_dto) pystyy mäppäämään
        'user_dto': create_user_profile(UserDto)
    }
    return Mapper(profiles)


# luodaan Mapperille typealias, jota voidaan käyttää controllerissa
ResponseMapper = Annotated[Mapper, Depends(create_mapper)]
