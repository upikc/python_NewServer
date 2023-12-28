import dataclasses

@dataclasses.dataclass
class Product:
    name: str
    category: str
    count: str
    price: int
    description: str
    creator: str
    img: str

@dataclasses.dataclass
class User:
    login: str
    password: str
    id: int

@dataclasses.dataclass
class RecoveryClass:
    products_with_sold: str
    user: User
