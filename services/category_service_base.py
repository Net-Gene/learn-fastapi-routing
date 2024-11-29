

import abc


class CategoryServiceBase(abc.ABC):
    @abc.abstractmethod
    def get_all(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def get_all_categories_with_products(self):
            raise NotImplementedError()