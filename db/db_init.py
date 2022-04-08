from db.fly_school import (
    Base,
    create_fake_students,
)
from db.session import Session

if __name__ == "__main__":
    session = Session()
    Base.metadata.create_all(session.get_bind())
    create_fake_students(session)
