import datetime
from with_session import with_session
from models.debtor import Debtor
from models.student import Student
from notifiers.core import get_notifier
from config import TELEGRAM_TOKEN

# Модуль рассылки уведомлений в случае если баланс меньше заданного предела
# Запускается по cron

@with_session
def get_debtors(session): # запрос списка учеников, которым нужно отправить уведомления
    return session.query(Debtor).all()

@with_session
def save_last_balance(session,id,new_balance): # сохранение значения отправленного баланса для исключения повторной отправки одинакового баланса
    session.query(Student).filter_by(telegram_id = id).update({"last_balance": new_balance}, synchronize_session="fetch")
    session.commit()

def message_text(student,summ): # формирование строки уведомления
    return f"Баланс {student}: {summ}"

def main():
    
    debtors_list=get_debtors()
    if debtors_list:
        telegram=get_notifier('telegram')
        for row in debtors_list:
            if datetime.datetime.today().isoweekday() == 6 or abs(row.last_balance-row.balance)>200:
                # по субботам отправляем в любом случае, в остальные дни только если баланс менялся больше чем на 200 после последней отправки
                response=telegram.notify(token=TELEGRAM_TOKEN, chat_id=row.telegram_id, message=message_text(row.student_fio,row.balance))    
                print(f"{message_text(row.student_fio,row.balance)}: {response}")
                if response.status == 'Success':
                    save_last_balance(row.telegram_id,row.balance)
                

if __name__== '__main__':
    main()


