from models import Base, engine
import sys

def init_db():
    Base.metadata.create_all(engine)
    print("Database initialized.")

if __name__ == '__main__':
    if 'init_db' in sys.argv:
        init_db()
