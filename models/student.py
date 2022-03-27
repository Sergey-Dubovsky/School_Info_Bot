from sqlalchemy import Column, String, Integer, Boolean, Numeric
from .database import Base

# таблица зарегистрированных пользователей
# в ней chat_id ползователя telegram соотносится c ФИО ребенка из таблицы балансов
# записи в таблицу добавляются при регистрации в боте (tlg_bot.py)


class Student(Base):
    disabled = Column(
        Boolean, nullable=False, index=True, default=0
    )  # отключение рассылки уведомдений (для отладки)
    admin = Column(
        Boolean, nullable=False, index=True, default=0
    )  # админский аккаунт (может доступна команда /stop )
    rk = Column(
        Boolean, nullable=False, index=True, default=0
    )  # член родительского комитета (может получать список всех должников, команда /dolgi )
    student_fio = Column(String(50), nullable=False, index=True)  # фамилия ребенка
    threshold = Column(
        Integer, nullable=False, default=500
    )  # минимальный баланс ниже которого шлется уведомление
    telegram_id = Column(
        Integer, nullable=False, index=True, unique=True
    )  # chat_id пользователя из телеграмма
    last_balance = Column(
        Numeric(precision=10, scale=2), nullable=False, index=True, default=0
    )  # последний отправленный баланс (чтоб не слать повторное уведомление с таким же балансом)

    def __str__(self):
        return (
            f"{self.__class__.__name__}(id={self.id}, "
            f"student_fio={self.student_fio!r},disabled={self.disabled!r},admin={self.admin!r},rk={self.rk!r},threshold={self.threshold!r},last_balance={self.last_balance!r},telegram_id={self.telegram_id!r}"
        )

    def __repr__(self):
        return str(self)
