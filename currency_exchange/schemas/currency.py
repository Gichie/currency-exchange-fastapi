from pydantic import BaseModel, Field, field_validator


class CurrencySchema(BaseModel):
    code: str = Field(
        pattern="^[a-zA-Z]{3}$", description="ISO 4217 currency code.", examples=["USD", "EUR"]
    )
    name: str = Field(min_length=3, max_length=40, examples=["US Dollar"])
    sign: str = Field(max_length=9, examples=["US Dollar"])

    @field_validator("code")
    @classmethod
    def code_to_uppercase(cls, value: str) -> str:
        return value.upper()
