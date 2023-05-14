from typing import List

from sqlalchemy import and_
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from src.database.models import Contact, User
from src.schemas import ContactModel


async def get_contacts(limit: int, offset: int, user: User, db: Session):
    contacts = db.query(Contact).filter(Contact.user_id ==
                                        user.id).limit(limit).offset(offset).all()
    return contacts


async def get_contact_by_id(contact_id: int, user: User, db: Session):
    contact = db.query(Contact).filter(
        and_(Contact.id == contact_id, Contact.user_id ==
             user.id)).first()
    return contact


async def get_contact_by_email(contact_email: str, user: User, db: Session):
    contacts = db.query(Contact).filter(
        and_(Contact.user_id == user.id, Contact.email.like(f"%{contact_email}%"))).all()
    return contacts


async def get_contacts_by_first_name(contact_first_name: str, user: User, db: Session):
    contacts = db.query(Contact).filter(and_(Contact.user_id == user.id,
                                             Contact.first_name.like(f"%{contact_first_name}%"))).all()
    return contacts


async def get_contacts_by_last_name(contact_last_name: str, user: User, db: Session):
    contacts = db.query(Contact).filter(and_(Contact.user_id == user.id,
                                             Contact.last_name.like(f"%{contact_last_name}%"))).all()
    return contacts


async def get_contacts_with_birthday(days, user: User, db: Session):
    contacts = []
    all_contacts = db.query(Contact).filter(Contact.user_id == user.id).all()
    for contact in all_contacts:
        for i in range(days):
            celebration_day = datetime.now() + timedelta(days=i)
            if contact.birthday.day == celebration_day.day and contact.birthday.month == celebration_day.month:
                contacts.append(contact)
    return contacts


async def create(body: ContactModel, user: User, db: Session):
    contact = Contact(first_name=body.first_name, last_name=body.last_name, phone=body.phone,
                      email=body.email, birthday=body.birthday, description=body.description, user=user)
    db.add(contact)
    db.commit()
    return contact


async def update(contact_id: int, body: ContactModel, user: User, db: Session):
    contact = await get_contact_by_id(contact_id, user, db)
    if contact:
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.phone = body.phone
        contact.email = body.email
        contact.birthday = body.birthday
        contact.description = body.description
        db.commit()
    return contact


async def remove(contact_id: int, user: User, db: Session):
    contact = await get_contact_by_id(contact_id, user, db)
    if contact:
        db.delete(contact)
        db.commit()
    return contact
