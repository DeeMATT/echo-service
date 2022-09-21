from pydantic import BaseModel, Field

class RateLimitSchema(BaseModel):
    rate_limit: str = Field(..., description="API Rate Limit")
