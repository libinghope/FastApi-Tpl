import sys
import os

# Add the project root to the python path
sys.path.append(os.getcwd())

from app.models.item import Item
from app.models.sys.user import SysUser
from sqlalchemy.inspection import inspect

def verify_model():
    print("Verifying Item model...")
    mapper = inspect(Item)
    columns = [c.key for c in mapper.columns]
    
    expected_fields = [
        'id', 'title', 'description', 
        'create_time', 'update_time', 'delete_time', 
        'create_by', 'update_by', 'delete_by', 'remark'
    ]
    
    missing_fields = [field for field in expected_fields if field not in columns]
    
    if missing_fields:
        print(f"FAILED: Missing fields in Item model: {missing_fields}")
    else:
        print("SUCCESS: Item model has all expected fields.")
        print(f"Columns found: {columns}")
        
    print("\nVerifying SysUser model...")
    mapper_user = inspect(SysUser)
    columns_user = [c.key for c in mapper_user.columns]
    
    expected_fields_user = [
        'id', 'username', 'dept_id',
        'create_time', 'update_time', 'delete_time', 
        'create_by', 'update_by', 'delete_by', 'remark'
    ]
    
    missing_fields_user = [field for field in expected_fields_user if field not in columns_user]
    
    if missing_fields_user:
        print(f"FAILED: Missing fields in SysUser model: {missing_fields_user}")
        sys.exit(1)
    else:
        print("SUCCESS: SysUser model has all expected fields.")
        print(f"Columns found: {columns_user}")

if __name__ == "__main__":
    verify_model()
