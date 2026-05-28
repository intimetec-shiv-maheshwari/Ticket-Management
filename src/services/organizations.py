from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.db.organizations import (
    create_organization as repo_create_organization,
    delete_organization as repo_delete_organization,
    get_all_organizations as repo_get_all_organizations,
    get_organization_by_id as repo_get_organization_by_id,
    update_organization as repo_update_organization,
)
from src.dtos.organizations import OrganizationCreateDTO
from src.models.organizations import Organization
from src.utils.constants import ORGANIZATION_NOT_FOUND


def get_all_organizations(db: Session):
    return repo_get_all_organizations(db)


def add_organization(organization: OrganizationCreateDTO, db: Session):
    data = organization.model_dump()
    new_organization = Organization(**data)
    return repo_create_organization(new_organization, db)


def get_organization_by_id(organization_id: str, db: Session):
    org = repo_get_organization_by_id(organization_id, db)
    if org is None:
        raise HTTPException(status_code=404, detail=ORGANIZATION_NOT_FOUND)
    return org


def delete_organization_by_id(organization_id: str, db: Session):
    org = repo_get_organization_by_id(organization_id, db)
    if org is None:
        raise HTTPException(status_code=404, detail=ORGANIZATION_NOT_FOUND)
    return repo_delete_organization(org, db)


def update_organization_by_id(organization_id: str, organization: OrganizationCreateDTO, db: Session):
    org = repo_get_organization_by_id(organization_id, db)
    if org is None:
        raise HTTPException(status_code=404, detail=ORGANIZATION_NOT_FOUND)
    org.name = organization.name
    org.description = organization.description
    org.country = organization.country
    org.active = organization.active
    return repo_update_organization(org, db)
