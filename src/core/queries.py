from motor.motor_asyncio import AsyncIOMotorCollection


class Q:
    def __init__(self, query: dict):
        self.query = query

    def __and__(self, other: "Q") -> "Q":
        return Q({"$and": [self.query, other.query]})

    def __or__(self, other: "Q") -> "Q":
        return Q({"$or": [self.query, other.query]})

    # 단일 필드용 편의 메서드
    @classmethod
    def in_(cls, field: str, value):
        return Q(cls._auto_in(field, value))

    # 여러 필드 한꺼번에
    @classmethod
    def filter(cls, **kwargs):
        cond = {}
        for k, v in kwargs.items():
            cond.update(cls._auto_in(k, v))
        return Q(cond)

    @classmethod
    def or_(cls, **kwargs):
        return Q({"$or": [{k: v} for k, v in kwargs.items()]})

    @classmethod
    def and_(cls, **kwargs):
        return Q({"$and": [{k: v} for k, v in kwargs.items()]})

    @staticmethod
    def _auto_in(field: str, value):
        """값이 여러개이면 $in, 단일이면 그대로"""
        if isinstance(value, str) and "," in value:
            value = [v.strip() for v in value.split(",") if v.strip()]
        if isinstance(value, (list, tuple, set)):
            return {field: {"$in": list(value)}}
        return {field: value}

    def __repr__(self):
        return f"Q({self.query})"


class BaseQueries:
    def __init__(self, collection: AsyncIOMotorCollection) -> None:
        self.collection = collection

    def _make_filter(self, **kwargs) -> dict:
        return {k: v for k, v in kwargs.items() if v is not None}

    async def find_one(self, **kwargs):
        filter = self._make_filter(**kwargs)
        return await self.collection.find_one(filter)

    async def find_and_update(self, data: dict, query: Q | None = None, **kwargs):
        if query:
            return await self.collection.find_one_and_update(
                query.query, {"$set": data}
            )
        else:
            filter = self._make_filter(**kwargs)
            return await self.collection.find_one_and_update(filter, {"$set": data})

    async def find(self, query: Q | None = None, **kwargs):
        if query:
            return await self.collection.find(query.query).to_list(length=None)
        filter = self._make_filter(**kwargs)
        return await self.collection.find(filter).to_list(length=None)

    async def create(self, data: dict):
        return await self.collection.insert_one(data)

    async def delete(self, query: Q):
        return await self.collection.delete_one(query.query)

    async def exists(self, query: Q):
        return await self.collection.count_documents(query.query) > 0
