from pydantic import BaseModel, Field, field_validator, ConfigDict


class CurrencyBase(BaseModel):
    id: int | None = None
    code: str = Field(
        pattern="^[a-zA-Z]{3}$", description="ISO 4217 currency code.", examples=["USD", "EUR"]
    )
    name: str = Field(min_length=2, max_length=40, examples=["US Dollar"])
    sign: str = Field(min_length=1, max_length=9, examples=["$"])


    @field_validator("code")
    @classmethod
    def code_to_uppercase(cls, value: str) -> str:
        return value.upper()
