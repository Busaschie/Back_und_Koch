from pydantic import BaseModel, Field
#from sqlalchemy import Date, Text
from enum import Enum
from datetime import date

'''
#-----------------------------------------------
# Wallet
#-----------------------------------------------
class WalletBase(BaseModel):
    date:date
    grund:str | None = None
    old_amount:str
    new_amount:str
    betrag:str
    user_id:UserRead.id
    task_id:TaskRead.id

class WalletRead(WalletBase):
    id:int

class WalletCreate(WalletBase):
    pass
'''
#-----------------------------------------------
# Task
#-----------------------------------------------
class TaskStatus(str,Enum):
    OPEN = "OPEN"
    DONE = "DONE"

class TaskBase(BaseModel):
    date:date
    monat:str | None = None
    jahr:int | None = None
    shop_date:date
    abgabe_date:date
    geld_date:date
    user_id: int | None = None
    #TaskStatus = TaskStatus.OPEN

class TaskRead(TaskBase):
    id:int

class TaskCreate(TaskBase):
    pass

#-----------------------------------------------
# User
#-----------------------------------------------
class UserBase(BaseModel):
    vorname:str
    nachname:str
    zimmer_nr:int | None = None
    buchnummer:str | None = None

class UserRead(UserBase):
    id:int
    #WalletBase:list[WalletRead]

class UserCreate(UserBase):
    pass



