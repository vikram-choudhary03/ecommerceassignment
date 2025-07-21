from pydantic import BaseModel, ConfigDict, Field

from typing import List

class Size(BaseModel):
    size : str
    quantity : int

class Product(BaseModel): 
    name : str 
    prices : float 
    sizes : List[Size]


class Item(BaseModel):
    productId : str 
    qty : int 

class Order(BaseModel):
    userId : str 
    items : List[Item]


