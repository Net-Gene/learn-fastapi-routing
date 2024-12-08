import abc

from dtos.categories import UpdateCategoryDtoReq


class CategoryServiceBase(abc.ABC):
    @abc.abstractmethod
    def get_all(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def get_all_categories_with_products(self, page: int, category_id: int):
        raise NotImplementedError()

    def add(self, req, user):
        raise NotImplementedError()

    def update(self, req: UpdateCategoryDtoReq, category_id: int):
        raise NotImplementedError()
