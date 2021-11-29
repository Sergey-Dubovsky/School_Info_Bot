from sqlalchemy import Column, String, Numeric
from .database import Base

# Описания класса для sql-view, созданного в БД средствами работы с БД (без alembic), для запроса списка должников.
# Используется только для чтения, поэтому нет PK
# При обновлении структуры с помощью alembic этот класс комментируется в __init__.py
# Описание view в файле models\create_debtors.sql


class Debtor(Base):
    student_fio = Column(String(50), nullable=False)  # фамилия ребенка
    balance = Column(Numeric(precision=10, scale=2))  # актуальный баланс счета
    last_balance = Column(
        Numeric(precision=10, scale=2)
    )  # последний отправленный баланс (чтоб не слать повторное уведомление с таким же балансом)
    telegram_id = Column(
        String(10), nullable=False
    )  # chat_id пользователя из телеграмма

    def __str__(self):
        return (
            f"{self.__class__.__name__}(id={self.id}, "
            f"student_fio={self.student_fio!r},balance={self.balance!r},last_balance={self.last_balance!r},telegram_id={self.telegram_id!r})"
        )

    def __repr__(self):
        return str(self)
