from models.mixins import TimestampMixin
from sqlalchemy import (Column,String,Numeric,Boolean)
from .database import Base

class Balance(Base,TimestampMixin):
    student_fio = Column(String(50),nullable=False, index=True)                         # фамилия ребенка
    last = Column(Boolean,nullable=False,index=True)                                    # призак последнего (актуального баланса)
    balance = Column(Numeric(precision=10,scale=2),nullable=False, index=True)          # значение баланса
    balance_delta = Column(Numeric(precision=10,scale=2),nullable=False)                # изменение баланса относительно предыдущей загрузки (delta)
    meal = Column(Numeric(precision=10,scale=2),nullable=False,default=0)               # затраты на обеды
    meal_delta = Column(Numeric(precision=10,scale=2),nullable=False,default=0)         # затраты на обеды (изменение (delta))
    excursion = Column(Numeric(precision=10,scale=2),nullable=False,default=0)          # затраты на экскурсии
    excursion_delta = Column(Numeric(precision=10,scale=2),nullable=False,default=0)    # затраты на экскурсии (изменение (delta))
    other = Column(Numeric(precision=10,scale=2),nullable=False,default=0)              # затраты прочие           
    other_delta = Column(Numeric(precision=10,scale=2),nullable=False,default=0)        # затраты прочие (изменение (delta))           
    
    def __str__(self):
        return (
            f"{self.__class__.__name__}(id={self.id}, "
            f"last={self.last!r},"
            f"student_fio={self.student_fio!r},balance={self.balance!r},balance_delta={self.balance_delta!r},"
            f"meal={self.meal!r},meal_delta={self.meal_delta!r},"
            f"excursion={self.excursion!r},excursion_delta={self.excursion_delta!r},"
            f"other={self.other!r},other_delta={self.other_delta!r},"
            f"loaded_at={self.loaded_at})"
        )

    def __repr__(self):
        return str(self)

