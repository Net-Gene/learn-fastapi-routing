from typing import Any

import jwt

from tools.token_tool_base import TokenToolBase


class SymmetricToken(TokenToolBase):
    # avain kannattaa oikeasti lukea .env-filusta
    # tai jostakin muusta vastaavasta tiedostosta, joka ei mene gitiin ikinä
    def create_token(self, payload: [str, Any]) -> str:
        token = jwt.encode(payload, key='supersecret', algorithm='HS512')

        return token