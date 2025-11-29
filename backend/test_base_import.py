"""Test that Base class works with the new DeclarativeBase."""
import sys
sys.path.insert(0, '.')

try:
    from app.models.base import Base
    print("✅ Step 1: Base imported successfully")
    print(f"   Base class type: {type(Base)}")
    print(f"   Base.__name__: {Base.__name__}")
    
    from app.models.player import Player
    from app.models.team import Team
    print("✅ Step 2: Models imported successfully")
    print(f"   Player.__tablename__: {Player.__tablename__}")
    print(f"   Team.__tablename__: {Team.__tablename__}")
    
    print(f"\n✅ Step 3: Base.metadata check")
    print(f"   Tables in metadata: {list(Base.metadata.tables.keys())[:5]}...")
    
    print("\n" + "="*60)
    print("✅ SUCCESS: All models work with DeclarativeBase!")
    print("="*60)
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
