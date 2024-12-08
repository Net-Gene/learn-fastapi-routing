

import abc


class ProductServiceBase(abc.ABC):
    @abc.abstractmethod
    def get_all(self, page):
        raise NotImplementedError()

