from fastapi import FastAPI, status, Query
from fastapi import HTTPException
from models import Product, Order
from typing import Union, Annotated
from bson import ObjectId
from db import products_collection, orders_collection
app = FastAPI()


@app.post("/products", status_code=status.HTTP_201_CREATED)
async def create_product(products : Product):
    
    products_dict = products.model_dump(); 

    result = await products_collection.insert_one(products_dict); 
   
   
    return {"id" : str(result.inserted_id)}


@app.get("/products")
async def get_products(
    name : Annotated[str | None, Query()] = None,    
    size : Annotated[str | None, Query()] = None, 
    limit: Annotated[int ,  Query( ge=1 , le=100)] = 10 , 
    offset : Annotated[int, Query(ge=0)] = 0
    ) :

    filter = {}
    if name : 
        filter["name"] = {"$regex" : name, "$options" :"i"}
    if size : 
        filter["sizes.size"] = size 
    
    #total filtered records
    total = await products_collection.count_documents(filter)
    
    
    result = []
    cursor  =   products_collection.find(filter, {"sizes": 0}).sort("_id").skip(offset).limit(limit)

    result = await cursor.to_list(length=limit)

    final_result = []
    
    for doc in result:
        _id = str(doc.pop("_id"))
        doc = {"id": _id, **doc}
        final_result.append(doc)

    

    #pagination 
    next_offset = offset + limit if (offset + limit) < total else None
    prev_offset = max(offset - limit, 0) if offset > 0 else None
    
   
    return {
        "data": final_result,
        "page" :{
            "next" : next_offset, 
            "limit" : limit,
            "previous" : prev_offset
        }
    }




# @app.post("/orders", status_code=status.HTTP_201_CREATED )
# async def create_order(order : Order):

#     product_ids = [ObjectId(item.productId) for item in order.items]

#     print(product_ids)
#     cursor_existing_products =  products_collection.find({
#         "_id" : {"$in" :product_ids}
#     })

#     existing_products  = await cursor_existing_products.to_list(length=None)
#     print(existing_products)
#     #creating map
#     products_dict = {}
     
#     for p in existing_products:
#         products_dict[str(p["_id"])] = p 

#     print(products_dict)
#     for item in order.items:

#         pid = item.productId
#         print(pid)
#         if pid not in products_dict:
#             raise HTTPException(status_code=404 , detail=f"Product {pid} not found.")
        
#         available_qty = products_dict[pid]["sizes.quantity"]
#         if item.qty > available_qty :
#             raise HTTPException (
#                 status_code= 404 ,
#                 detail = f"Product {pid} has only {available_qty} in stock."
#             )
        


#     # updating quantities 

#     for item in order.items:
#         await products_collection.update_one(
#             {"_id": ObjectId(item.productId)},
#             {"$inc": {"quantity": -item.qty}}
#         )    

    
#     order_dict = order.model_dump(); 

#     result = await orders_collection.insert_one(order_dict);

#     return {"id" : str(result.inserted_id)}
   








    
   

