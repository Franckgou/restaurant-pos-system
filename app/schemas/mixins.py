from pydantic import BaseModel, Field
from datetime import datetime

class TimestampMixinSchema(BaseModel):
    created_at: datetime = Field(description = "creation date")
    updated_at : datetime = Field(description= "time od the last update")

