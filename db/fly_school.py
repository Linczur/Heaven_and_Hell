from faker import Faker

from sqlalchemy import (
    Column, Integer, String,
    DateTime, Numeric, Float, Date, ForeignKey
)
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Employees(Base):
    __tablename__ = "employees"

    employee_id = Column(Integer, autoincrement=True, primary_key=True)
    first_name = Column(String(64), nullable=False)
    last_name = Column(String(64), nullable=False)
    work_start = Column(DateTime, nullable=False)
    PESEL = Column(Integer, nullable=False, unique=True)
    phone = Column(Numeric, nullable=False)
    address = Column(String(64))

    empl_dep = relationship("Departments", back_populates="employee")


class Departments(Base):
    __tablename__ = "departments"

    dep_id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(100), nullable=False)
    budget = Column(Float, nullable=False)
    address = Column(String(100))
    manager = Column(String(32))
    empl_id = Column(Integer, ForeignKey('employees.employee_id'))

    employee = relationship('Employees', back_populates="empl_dep")
    course_dep = relationship("Courses", back_populates='department')


class CourseType(Base):
    __tablename__ = "course_type"

    type_id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String(7))

    course_type = relationship("Courses", back_populates="type")


class Ratings(Base):
    __tablename__ = "ratings"

    rating_id = Column(Integer, autoincrement=True, primary_key=True)
    rating = Column(Integer)
    course_id = Column(Integer, ForeignKey('courses.course_id'))
    student_id = Column(Integer, ForeignKey('students.student_id'))

    rate = relationship('Students', back_populates='student_course_rate')
    course_rating = relationship('Courses', back_populates='rating')


class Students(Base):
    __tablename__ = "students"

    student_id = Column(Integer, autoincrement=True, primary_key=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    PESEL = Column(String(11), nullable=False)
    phone = Column(String(100), nullable=True)
    address = Column(String(64))

    student_course_rate = relationship("Ratings", back_populates='rate')

    @staticmethod
    def create_fake_students():
        fake = Faker('pl_PL')
        return Students(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            PESEL=fake.pesel(),
            phone=fake.phone_number(),
            address=fake.address(),
        )


def create_fake_students(session, count=100):
    students_generated = 0
    while students_generated < count:
        try:
            session.add(Students.create_fake_students())
            session.commit()
        except IntegrityError:
            session.rollback()
            continue
        students_generated += 1


class Courses(Base):
    __tablename__ = "courses"

    course_id = Column(Integer, autoincrement=True, primary_key=True)
    course_name = Column(String(32), nullable=False)
    price = Column(Float, nullable=False)
    ECTS_points = Column(Integer)
    start_date = Column(Date)
    end_date = Column(Date)
    course_type = Column(String(32), nullable=False)
    dep_id = Column(Integer, ForeignKey('departments.dep_id'))
    type_id = Column(Integer, ForeignKey('course_type.type_id'))

    rating = relationship('Ratings', back_populates='course_rating')
    type = relationship('CourseType', back_populates="course_type")
    department = relationship('Departments', back_populates='course_dep')
