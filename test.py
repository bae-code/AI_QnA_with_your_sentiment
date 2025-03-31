from dataclasses import dataclass
from pydantic import BaseModel


@dataclass
class DataItem:
    price: int


class PydanticItem(BaseModel):
    price: int


# dataclass는 그냥 들어감
data_item = DataItem(price="3000")  # ❗ 통과
print(f"data_item: {data_item}")
# pydantic은 에러 발생
pydantic_item = PydanticItem(price="3000")  # ✅ 자동 캐스팅 → int(3000)
print(f"pydantic_item: {pydantic_item}")
pydantic_item = PydanticItem(price="삼천원")  # ❌ ValidationError
print(f"pydantic_item: {pydantic_item}")
