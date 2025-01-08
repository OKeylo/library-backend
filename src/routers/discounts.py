from fastapi import APIRouter, Depends, HTTPException
from queries.core import AsyncCore
from schemas import DiscountsAddDTO, DiscountsUpdateDTO, DiscountsDTO
from models import discounts


router = APIRouter(tags=["discounts"])

@router.get("/discounts")
async def get_discounts():
    discounts_list = await AsyncCore.select(discounts, DiscountsDTO)
    
    return discounts_list

@router.post("/discounts")
async def create_discount(discount: DiscountsAddDTO = Depends()):
    new_discount_id = await AsyncCore.insert_discount(discount)

    return {"id": new_discount_id}

@router.put("/discounts/{id}")
async def update_discount(subscription: str, sub_level: int, update_data: DiscountsUpdateDTO = Depends()):
    updated_discount_id = await AsyncCore.update_discount(subscription, sub_level, update_data)

    return {"id": updated_discount_id}

@router.delete("/discounts/{id}")
async def delete_discount(subscription: str, sub_level: int):
    deleted_discount_id = await AsyncCore.delete_discount(subscription, sub_level)

    if not deleted_discount_id:
        raise HTTPException(404, "Скидка с такими полями не найден!") 

    return {"id": deleted_discount_id}