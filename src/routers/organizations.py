from fastapi import APIRouter, Depends;
from ..dtos.organizations import OrganizationCreateDTO, OrganizationDTO;
from ..services.organizations import get_all_organizations, add_organization, get_organization_by_id, delete_organization_by_id, update_organization_by_id;
from ..utils.db import get_db;
router = APIRouter(prefix="/organizations", tags=["Organizations"]);

@router.get("/", response_model=list[OrganizationDTO])
def get_organizations(db= Depends(get_db)):
    return get_all_organizations(db);

@router.get("/{organization_id}", response_model=OrganizationDTO)
def organization_by_id(organization_id: str, db= Depends(get_db)):
    return get_organization_by_id(organization_id, db);

@router.post("/", response_model=OrganizationDTO)
def create_organization(data: OrganizationCreateDTO, db= Depends(get_db)):
    return add_organization(data, db);

@router.put("/{organization_id}", response_model=OrganizationDTO)
def update_organization(organization_id: str, data: OrganizationCreateDTO, db= Depends(get_db)):
    return update_organization_by_id(organization_id, data, db);

@router.delete("/{organization_id}", response_model=dict)
def delete_organization(organization_id: str, db= Depends(get_db)):
    return delete_organization_by_id(organization_id, db);