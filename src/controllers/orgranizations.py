from src.dtos.organizations import OrganizationCreateDTO;
from sqlalchemy.orm import Session;
from src.models.organizations import Organization;
from fastapi import HTTPException;
from src.utils.constants import ORGANIZATION_NOT_FOUND;

def get_all_organizations(db: Session):
    return db.query(Organization).all();

def add_organization(organization: OrganizationCreateDTO, db: Session):
    data = organization.model_dump();
    new_organization = Organization(**data);
    db.add(new_organization);
    db.commit();
    db.refresh(new_organization);
    return new_organization;

def get_organization_by_id(organization_id: str, db: Session):
    org = db.query(Organization).filter(Organization.id == organization_id).first()
    if org is None:
        raise HTTPException(status_code=404, detail=ORGANIZATION_NOT_FOUND);
    return org;

def delete_organization_by_id(organization_id: str, db: Session):
    org = db.query(Organization).filter(Organization.id == organization_id).first()
    if org is None:
        raise HTTPException(status_code=404, detail=ORGANIZATION_NOT_FOUND);
    db.delete(org);
    db.commit();
    return {"message": "Organization deleted successfully"};

def update_organization_by_id(organization_id: str, organization: OrganizationCreateDTO, db: Session):
    org = db.query(Organization).filter(Organization.id == organization_id).first()
    if org is None:
        raise HTTPException(status_code=404, detail=ORGANIZATION_NOT_FOUND);
    org.name = organization.name;
    org.description = organization.description;
    org.country = organization.country;
    org.active = organization.active;
    db.commit();
    db.refresh(org);
    return org;