from app.models.base import Base
from sqlalchemy.orm import DeclarativeBase
import sys

def verify_sqlalchemy_base():
    print("Verifying SQLAlchemy Base class...")
    
    if issubclass(Base, DeclarativeBase):
        print("✅ SUCCESS: Base class inherits from sqlalchemy.orm.DeclarativeBase")
        print("This confirms the modern SQLAlchemy 2.0 pattern is in use.")
        sys.exit(0)
    else:
        print("❌ FAILURE: Base class does NOT inherit from DeclarativeBase")
        print(f"Base MRO: {Base.mro()}")
        sys.exit(1)

if __name__ == "__main__":
    verify_sqlalchemy_base()
