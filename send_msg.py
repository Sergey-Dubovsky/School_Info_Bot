import datetime
from with_session import with_session
from models.student import Student
from notifiers.core import get_notifier
from config import TELEGRAM_TOKEN

# Модуль ручной рассылки информационных сообщений подписчкам


@with_session
def get_admins(session):  # запрос списка учеников, которым нужно отправить уведомления
    return session.query(Student).filter_by(admin=1).all()


@with_session
def get_rk(session):  # запрос списка учеников, которым нужно отправить уведомления
    return session.query(Student).filter_by(admin=0, rk=1).all()


@with_session
def get_users(session):  # запрос списка учеников, которым нужно отправить уведомления
    return session.query(Student).filter_by(admin=0, rk=0).all()


@with_session
def get_all(session):  # запрос списка учеников, которым нужно отправить уведомления
    return session.query(Student).all()


def main():

    telegram = get_notifier("telegram")

    # list = get_admins()
    # list = get_all()
    list=get_rk()

#     message_str = """
# В бот добавлена команда "/hist" - история изменений за 14 дней, с ее помощью можно понять причину изменения баланса, не залезая в общую таблицу.\n
# Также напоминаю, что текущий баланс можно быстро узнать с помощью команды "/balance"\n
# Все команды можно найти и вызвать из меню бота (кнопка рядом со строкой ввода сообщения).
# или кликнув по команде прямо в переписке, например в этом сообщении. 
#     """

    message_str = """
Для членов РК в бот добавлена команда "/dolgi" - список всех должников с указанием размера долга. 
    """

    for row in list:
        response = telegram.notify(
            token=TELEGRAM_TOKEN,
            chat_id=row.telegram_id,
            message=message_str,
        )
        print(f"{row.student_fio}: {response}")


if __name__ == "__main__":
    main()
