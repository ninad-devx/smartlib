from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.shelf import Shelf
from app.models.book import Book
from sqlalchemy import or_

from app.schemas.book import(ShelfCreate,Bookcreate)

router=APIRouter()

@router.post("/shelves")
def create_shelf(payload:ShelfCreate,db:Session=Depends(get_db)):
    shelf=Shelf(
        shelf_code=payload.shelf_code,
        floor=payload.floor
    )
    db.add(shelf)
    db.commit()

    return {
        "success":True,
        "message":"shelf created"
    }


@router.get("/shelves")
def get_shelves(db:Session=Depends(get_db)):
    shelves=db.query(Shelf).all()
    return shelves


@router.post("/books")
def created_book(payload:Bookcreate,db:Session=Depends(get_db)):

    print(payload)

    book=Book(
        isbn=payload.isbn,
        title=payload.title,
        author=payload.author,
        publisher=payload.publisher,
        category=payload.category,
        shelf_id=payload.shelf_id,
        quantity=payload.quantity,
        available_quantity=payload.quantity
    )

    db.add(book)
    db.commit()
    return {
        "succes":True,
        "message":"book added"
    }

@router.get("/books")
def get_books(db:Session=Depends(get_db)):
    books=db.query(Book).all()
    return books


@router.get("/books/search")
def search_books(
    q: str,
    db: Session = Depends(get_db)
):

    books = (
        db.query(
            Book,
            Shelf
        )
        .join(
            Shelf,
            Book.shelf_id == Shelf.id
        )
        .filter(
            Book.title.ilike(f"%{q}%")
        )
        .all()
    )

    result = []

    for book, shelf in books:

        result.append({

            "id": book.id,

            "title": book.title,

            "author": book.author,

            "available_quantity":
                book.available_quantity,

            "shelf_code":
                shelf.shelf_code

        })

    return result
    
    
