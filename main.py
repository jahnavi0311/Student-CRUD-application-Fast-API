from fastapi import FastAPI, status, HTTPException
from database import Base, engine
from sqlalchemy.orm import Session
import models
import schemas

# Create the database
Base.metadata.create_all(engine)

# Initialize app
app = FastAPI()

@app.get("/")
def root():
    return "Student Database Application"

@app.post("/", status_code=status.HTTP_201_CREATED)
def new_student(student: schemas.StuDent ):

    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)

    # create an instance of the StuDent database model
    studentdb = models.StuDent(sname = student.sname, section = student.section, grp = student.grp)

    # add it to the session and commit it
    session.add(studentdb)
    session.commit()

    # grab the id given to the object from the database
    id = studentdb.id

    # close the session
    session.close()

    # return the id
    return f"created student details with id {id}"

@app.get("/student/{id}")
def read_student(id: int):

    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)

    # get the student details with the given id
    student = session.query(models.StuDent).get(id)

    # close the session
    session.close()

    # check if student with given id exists. If not, raise exception and return 404 not found response
    if not student:
        raise HTTPException(status_code=404, detail=f"student details with id {id} not found")

    return student

@app.put("/student/{id}")
def update_student(id: int, sname: str, section: str, grp: str):

    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)

    # get the student details with the given id
    student = session.query(models.StuDent).get(id)

    # update student with the given name (if an item with the given id was found)
    if student:
        student.sname = sname
        student.section = section
        student.grp = grp
        session.commit()

    # close the session
    session.close()

    # check if student with given id exists. If not, raise exception and return 404 not found response
    if not student:
        raise HTTPException(status_code=404, detail=f"student details with id {id} not found")

    return student

@app.delete("/student/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(id: int):

    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)

    # get the student details with the given id
    student = session.query(models.StuDent).get(id)

    # if student with given id exists, delete it from the database. Otherwise raise 404 error
    if student:
        session.delete(student)
        session.commit()
        session.close()
    else:
        raise HTTPException(status_code=404, detail=f"student item with id {id} not found")

    return None

@app.get("/student")
def read_student_list():
    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)

    # get all students details
    student_list = session.query(models.StuDent).all()

    # close the session
    session.close()

    return student_list
