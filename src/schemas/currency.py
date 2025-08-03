from pydantic import BaseModel, ConfigDict, Field, field_validator


class CurrencyScheme(BaseModel):
    id: int | None = None
    code: str = Field(
        pattern="^[a-zA-Z]{3}$", description="ISO 4217 currency code.", examples=["USD", "EUR"]
    )
    name: str = Field(min_length=1, max_length=40, examples=["US Dollar"])
    sign: str = Field(min_length=1, max_length=8, examples=["$"])

    model_config = ConfigDict(from_attributes=True)

    @field_validator("code")
    @classmethod
    def code_to_uppercase(cls, code: str) -> str:
        return code.upper()
