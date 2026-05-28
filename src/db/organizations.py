from sqlalchemy.orm import Session

from src.models.organizations import Organization


def get_all_organizations(db: Session):
    return db.query(Organization).all()


def get_organization_by_id(organization_id: str, db: Session):
    return db.query(Organization).filter(Organization.id == organization_id).first()


def create_organization(organization: Organization, db: Session):
    db.add(organization)
    db.commit()
    db.refresh(organization)
    return organization


def update_organization(organization: Organization, db: Session):
    db.commit()
    db.refresh(organization)
    return organization


def delete_organization(organization: Organization, db: Session):
    db.delete(organization)
    db.commit()
    return {"message": "Organization deleted successfully"}
