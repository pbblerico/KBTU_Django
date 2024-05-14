from database import get_db
from auth import schemas
from auth import models
from typing import Annotated
from fastapi import Depends
from auth.exceptions import user_already_exists_exception
from auth.utils import get_password_hash
from instructor.crud import create_instructor
from student.crud import create_student

def check_user_existense(email: str, session: Annotated[str, Depends(get_db)]):
   return session.query(models.User).filter(models.User.email==email).first()


def create_user(user: schemas.UserCreate, session: Annotated[str, Depends(get_db)]): 
   if not check_user_existense(user.email, session):
      raise user_already_exists_exception
   
   encrypted_password = get_password_hash(user.password)

   new_user = models.User(username=user.username, email=user.email, password=encrypted_password, role=user.role.value)

   session.add(new_user)
   session.flush()
   
   if(new_user.role == models.RoleEnum.INSTRUCTOR.value):  
      create_instructor(new_user.id, session)
        
   elif(new_user.role == models.RoleEnum.STUDENT.value):
      create_student(new_user.id, session)

   session.commit()

   return new_user


# def get_assignment_by_id(assignment_id: int, session: Annotated[str, Depends(get_db)]):
#     return session.query(models.Assignment).filter(models.Assignment.id==assignment_id).first()


