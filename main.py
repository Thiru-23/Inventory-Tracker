from fastapi import FastAPI,Depends
from models import Product
from database import session,engine
from fastapi.middleware.cors import CORSMiddleware
import da
from sqlalchemy.orm import Session



app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"])

da.Base.metadata.create_all(bind=engine)


products=[Product(id=1, name="Phone", description="A smartphone", price=699.99, quantity=50),
Product(id=2, name="Laptop", description="A powerful laptop", price=999.99, quantity=30),
Product(id=3, name="Pen", description="A blue ink pen", price=1.99, quantity=100),
Product(id=4, name="Table", description="A wooden table", price=199.99, quantity=20),]



def get_db():
    db=session()
    try:
        yield db
    finally:
        db.close()

def init_db():
    db=session()
    c=db.query(da.Product).count
    if c==0:
     for p in products:
        db.add(da.Product(**p.model_dump()))
     db.commit()

init_db()




@app.get("/")
def greet():
    return "welcome"
@app.get("/products")
def get_all(db:Session=Depends(get_db)):
    dproducts=db.query(da.Product).all()
    
    return dproducts

@app.get("/products/{id}")
def get_byid(id:int,db:Session=Depends(get_db)):
    dd=db.query(da.Product).filter(da.Product.id==id).first()
    if dd:
     return dd
    return " no products"

@app.post("/products")
def add(product: Product, db: Session = Depends(get_db)):
    new_product = da.Product(**product.model_dump())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product
@app.put("/products/{id}")
def update(id:int,product:Product,db: Session = Depends(get_db)):
    dd=db.query(da.Product).filter(da.Product.id==id).first()
    if dd:
        dd.name=product.name
        dd.description=product.description
        dd.price=product.price
        dd.quantity=product.quantity
        db.commit()
        return "product updated"
    else:
     return "no products"

@app.delete("/products/{id}")
def delete(id:int,db: Session = Depends(get_db)):
    db_product=db.query(da.Product).filter(da.Product.id==id).first()
    if db_product:        
        db.delete(db_product)
        db.commit()
        return "Product deleted"
    else:
         return "not found"   