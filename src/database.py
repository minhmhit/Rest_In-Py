import os
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from model import Base, User, Tenant, Room, Service, Bill, BillService
from sqlalchemy import text


def get_database_url():
    return "mysql+mysqlconnector://root:@localhost/quanlynhatro"

# tạo engine
engine = create_engine(get_database_url(), echo=False)  
#kiểm tra
if not database_exists(engine.url):
    create_database(engine.url)
    print("Đã tạo cơ sở dữ liệu 'quanlynhatro'.")

#tạo session
Session = sessionmaker(bind=engine)

#tạo bảng từ model
def init_db():
    # tạo bảng
    Base.metadata.create_all(engine)
    print("Đã tạo tất cả các bảng trong cơ sở dữ liệu.")

def generate_comprehensive_sql_script():
    os.makedirs('databasesql', exist_ok=True)
    script_path = os.path.join('databasesql', 'qlnt.sql')
    
    inspector = inspect(engine)
    
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write("-- Tạo cơ sở dữ liệu\n")
        f.write("CREATE DATABASE IF NOT EXISTS quanlynhatro;\n")
        f.write("USE quanlynhatro;\n\n")
        
        for table in Base.metadata.sorted_tables:
            f.write(f"-- Bảng {table.name}\n")
            f.write(f"DROP TABLE IF EXISTS {table.name};\n")
            f.write(f"CREATE TABLE {table.name} (\n")
            
            columns = []
            for column in table.columns:
                col_def = f"    {column.name} {column.type}"
                if not column.nullable:
                    col_def += " NOT NULL"
                if column.primary_key:
                    col_def += " PRIMARY KEY"
                if column.unique:
                    col_def += " UNIQUE"
                if column.foreign_keys:
                    fk = list(column.foreign_keys)[0]
                    col_def += f" REFERENCES {fk.target_fullname}"
                columns.append(col_def)
            
            f.write(",\n".join(columns))
            f.write("\n);\n\n")
        
        print(f"Đã sinh file SQL chi tiết: {script_path}")

init_db()
# generate_comprehensive_sql_script()   chạy func này để tạo sql

#xuất data
__all__ = ["Session", "get_database_url", "generate_comprehensive_sql_script", "engine"]


# test kết nối
"""

    if __name__ == "__main__":
        session = Session()
        try:
            session.execute(text('SELECT 1'))
            print("Kết nối cơ sở dữ liệu thành công!")
        except Exception as e:
            print(f"Lỗi kết nối: {e}")
        finally:
            session.close()
        
"""
