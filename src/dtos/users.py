from pydantic import BaseModel, ConfigDict, Field;


class UserLoginDTO(BaseModel):
    email: str;
    password: str;


class UserCreateDTO(BaseModel):
    name: str;
    email: str;
    password: str;
    organization_id: str = Field(min_length=16, max_length=16);
    role_id: str = Field(min_length=16, max_length=16);
    active: bool = True;


class UserDTO(BaseModel):
    id: str = Field(min_length=16, max_length=16);
    name: str;
    email: str;
    organization_id: str = Field(min_length=16, max_length=16);
    role_id: str = Field(min_length=16, max_length=16);
    active: bool = True;
