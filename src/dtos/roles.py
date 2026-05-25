from pydantic import BaseModel, ConfigDict, Field;


class RoleCreateDTO(BaseModel):
    name: str;
    description: str | None = None;
    organization_id: str = Field(min_length=16, max_length=16);
    active: bool = True;


class RoleDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True);

    id: str = Field(min_length=16, max_length=16);
    name: str;
    description: str | None = None;
    organization_id: str = Field(min_length=16, max_length=16);
    active: bool = True;
