from sqlalchemy.orm import Session
from app.models.store import Store
from app.schemas.store import StoreCreate, StoreUpdate


class StoreService:
    @staticmethod
    def create_store(db: Session, store_data: StoreCreate) -> Store:
        store = Store(**store_data.dict())
        db.add(store)
        db.commit()
        db.refresh(store)
        return store

    @staticmethod
    def get_store(db: Session, store_id: int) -> Store:
        return db.query(Store).filter(Store.id == store_id).first()

    @staticmethod
    def list_stores(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Store).filter(Store.is_active == True).offset(skip).limit(limit).all()

    @staticmethod
    def update_store(db: Session, store_id: int, store_data: StoreUpdate) -> Store:
        store = db.query(Store).filter(Store.id == store_id).first()
        if not store:
            return None
        
        update_data = store_data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(store, key, value)
        
        db.commit()
        db.refresh(store)
        return store

