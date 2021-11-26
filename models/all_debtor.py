from sqlalchemy import (Column,String,Numeric)
from sqlalchemy.sql import text
from sqlalchemy import select
from .database import Base
from .balance import Balance
from .student import Student
from sqlalchemy_utils.view import create_view

# Для новых функций. Игнорировать!!!

class All_debtor(Base):
    __table__ = create_view(
        name='all_debtors',
        selectable=select(
            [
                Balance.id,
                Balance.student_fio,
                Balance.balance,
                Student.telegram_id,
            ],
            from_obj=(
                Balance.__table__
                    .join(Student, Balance.student_fio == Student.student_fio)
            ),
            whereclause=(text('balances.last<>0 and balance.balance<students.treshold'))
        ),
        metadata=Base.metadata
    )
# class Debtor(Base):
#     student_fio = Column(String(50),nullable=False)
#     balance = Column(Numeric(precision=10,scale=2)) 
#     telegram_id = Column(String(10),nullable=False) 

#     def __str__(self):
#         return (
#             f"{self.__class__.__name__}(id={self.id}, "
#             f"student_fio={self.student_fio!r},balance={self.balance!r},telegram_id={self.telegram_id!r})"

#         )

#     def __repr__(self):
#         return str(self)

