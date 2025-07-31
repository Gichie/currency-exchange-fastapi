from pydantic import BaseModel, Field, field_validator, ConfigDict


class CurrencyScheme(BaseModel):
    id: int
    code: str = Field(
        pattern="^[a-zA-Z]{3}$", description="ISO 4217 currency code.", examples=["USD", "EUR"]
    )
    name: str = Field(min_length=2, max_length=40, examples=["US Dollar"])
    sign: str = Field(min_length=1, max_length=9, examples=["$"])

    model_config = ConfigDict(from_attributes=True)

    @field_validator("code")
    @classmethod
    def code_to_uppercase(cls, value: str) -> str:
        return value.upper()
