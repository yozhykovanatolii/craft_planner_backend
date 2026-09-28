from pydantic import BaseModel, ConfigDict
from datetime import datetime

class CraftPlanBaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    target_item_name: str
    target_item_quantity: int
    status: str
    created_at: datetime
    
class CraftPlanInfoSchema(CraftPlanBaseSchema):
    available_ingredients: dict
    ingredients_to_craft: dict
    required_components: dict
    