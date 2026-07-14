from models import User, Admin, Wallet, Task
from sqlalchemy.orm import Session
from sqlalchemy import text, select
from datetime import date
#from util import hash_password, verify_password

#import bcrypt

'''
# ----------------------
# Admin
# ----------------------
class AdminRepository():
    def __init__(self, session:Session):
        self.session=session
'''
# ----------------------
# Task
# ----------------------
class TaskRepository():
    def __init__(self, session:Session):
        self.session=session

    def find_all_tasks(self)-> list[Task]:
        return self.session.query(Task).all()

    def find_open_tasks(self)-> list[Task]:
        return self.session.query(Task).filter(Task.status == "OPEN").all()

    def find_one_tasks(self, shop_date:date) -> list[Task]:
        #statement = select(Task).where(Task.shop_date == shop_date)
        #result = self.session.execute(statement)
        #return list(result.scalars().all())
        query = (
            self.session.query(Task)
            .filter(Task.shop_date == shop_date)
            #.filter(Task.status == "OPEN")
        )
        return query.all()

    def create_task(self, task:Task) -> Task:
        existing = self.session.query(Task).filter(Task.monat==task.monat, Task.jahr==task.jahr).first()
        if existing:
            raise ValueError("Task existiert bereits!")
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task

# ----------------------
# User
# ----------------------
class UserRepository():
    def __init__(self, session:Session):
        self.session = session

    def find_all_users(self)-> list[User]:
        return self.session.query(User).all()


    def create(self, user:User) -> User:
        existing = self.session.query(User).filter(User.buchnummer == user.buchnummer).first()
        if existing:
            raise ValueError("User existiert bereits!")
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user
# ----------------------
'''
    def find_user_by_id(self, id:int)-> User | None:
        return self.session.get(User, id)
    
    def delete_user(self, user_id:int)-> User | None:
        user = self.session.get(User, user_id)
        if user is None:
            return None
        self.session.delete(user)
        self.session.commit()
        return user

    def find_user_by_credentials(self, username:str, password:str)->User | None:
        #hashed = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())
        stored_user = self.session.query(User).filter(User.username == username).first()
        if not stored_user:
            return None
        return  stored_user if verify_password(password, stored_user.password) else None


# ----------------------
# Wallet
# ----------------------
class WalletRepository():
    def __init__(self, session:Session):
        self.session=session

    # def save(self, todo:Todo) -> Todo:
    #     self.session.add(todo)
    #     self.session.commit()
    #     self.session.refresh(todo) 
    #     return todo

    def update_wallet_state(self, todo_id:int, new_state:str)->Todo | None:
        allowed = {"OPEN","IN_PROGRESS","DONE"}
        if new_state not in allowed:
            raise ValueError(f"Invalid State, allowed: {allowed}")
        todo = self.session.get(Todo,todo_id)
        if not todo:
            return None
        todo.state = new_state
        self.session.commit()
        self.session.refresh(todo)
        return todo

    def find_wallet_by_task(self,user_id:int,task:str)->list[Todo]:
        return (self.session.query(Todo).filter(Todo.user_id==user_id,Todo.task.ilike(f"%{task}%")).all())

#----------------------
# todo

    def new_wallet_by_user(self, user_id: int, todo: Todo) -> Todo:
        user = self.session.get(User, user_id)
        user.todos.append(todo)
        self.session.commit()
        self.session.refresh(todo)
        return todo

    def find_wallet_by_user(self,user_id:int)->list[Todo]:
        return self.session.query(Todo).filter(Todo.user_id==user_id).all()

   # def find_open_todos_by_user(self,user_id:int)->list[Todo]:
   #     return (self.session.query(Todo).filter(Todo.user_id == user_id, Todo.state == "OPEN").all())
    
    def find_open_wallet_by_user(self, user_id: int) -> list[Todo]:
        query = (
            self.session.query(Todo)
            .filter(Todo.user_id == user_id)
            .filter(Todo.state == "OPEN")
        )
        return query.all()
#---------------------

    def delete_wallet(self, todo_id:int)-> Todo | None:
        """ """
        todo = self.session.get(Todo,todo_id)
        if todo is  None:
            return None
        self.session.delete(todo)
        self.session.commit()
        return todo

    def delete_all_done_wallet(self,user_id:int)->int:
        wallet = (
            self.session.query(wall)
            .filter(
                Wallet.user_id == user_id,
                Wallet.state == "DONE"
            )
            .all()
        )
        count = len(wallet)
        for wall in wallet:
            self.session.delete(wall)
        self.session.commit()
        return  count
'''
