from pydantic import BaseModel


class ValidationErrorResponse(BaseModel):
    error: str


class UnexpectedErrorResponse(BaseModel):
    error: str
