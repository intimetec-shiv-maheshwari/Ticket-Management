from pydantic import BaseModel, Field;

class OrganizationCreateDTO(BaseModel):
    name: str;
    description: str;
    country: str;
    active: bool = True;

class OrganizationDTO(BaseModel):
    id: str = Field(min_length=16, max_length=16);
    name: str;
    description: str;
    country: str;
    active: bool = True;