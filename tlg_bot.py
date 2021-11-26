from send_warn import message_text, save_last_balance
import telebot
from with_session import with_session
from models.student import Student
from models.balance import Balance
from config import TELEGRAM_TOKEN
from loguru import logger
from load_data import load

bot = telebot.TeleBot(TELEGRAM_TOKEN, parse_mode='HTML')

# Модуль телеграм-бота
# Используется для:
# - регистрации (привязки chat_id (поле telegram_id) пользователя к имени ученика в таблице students),
# - изменения граничного значения (threshold) для отправки уведомлений (/limit)
# - отмены регистрации (/del)
# а также для запросов:
# - актуального баланса (/balance),
# - динамики изменения баланса с указанием изменившихся статей расхода (обеды, экскурсии, прочее) (не сделано) (/hist)
# - списка должников членами родительского комитета (не сделано) (/dolgi)

# для упрощения регистрации решено был не использовать команту а проверять любой отправленный текст на совпадение с фамилией ребенка в списке загруженных балансов
# если была отправлена фамилия и имя, то происходит регистрация, если нет, то выдается подсказка по работе с ботом

@bot.message_handler(commands=['start', 'help'])  # приветствие, отправка текущих настроек и списка текущих команд
def send_welcome(message):
    send_current_config(message)    

@bot.message_handler(commands=['limit'])  # изменение threshold в файле students
@with_session
def change_limit(session,message):
    current=get_current_data(message.from_user.id)  #загрузка настроек из students

    if current:
        try:
            new_limit=int(message.text.replace('/limit',''))
        except ValueError:
            new_limit=0

        if new_limit!=0: # изменение threshold
            session.query(Student).filter_by(telegram_id = message.from_user.id).update({"threshold": int(message.text.replace('/limit',''))}, synchronize_session="fetch")
            session.commit()
            bot.reply_to(message, 'Минимальный баланс изменен')
        else:
            bot.reply_to(message, 'Не верно указана величина минимального баланса')   

    send_current_config(message)

@bot.message_handler(commands=['del'])  # Отмена регистрации (удаление записи в students)
@with_session
def del_reg(session,message):
    current=get_current_data(message.from_user.id)
    if current:
        session.query(Student).filter_by(telegram_id = message.from_user.id).delete(synchronize_session="fetch")
        session.commit()
        bot.reply_to(message, 'Регистрация успешно отменена!')

    send_current_config(message)

@bot.message_handler(commands=['balance']) # запрос актуального баланса
@with_session
def get_balance(session,message):
    current=get_current_data(message.from_user.id) # загрузка данных регистрации]
    logger.info(f'/balance {message.from_user.id} {message.from_user.first_name} {message.from_user.last_name} {message.from_user.username}') # телеметрия в журнал
    if current:
        load() # обновление балансов из Google Docs
        balance=session.query(Balance).filter_by(student_fio = current.student_fio, last=True).one_or_none()  # запрос последнего загруженного баланса
        if balance:
            bot.reply_to(message, message_text(balance.student_fio,balance.balance))
            save_last_balance(message.from_user.id,balance.balance)  # сохранение последнего отправленного баланса
    else:        
        send_current_config(message) # если пользователь не зарегистрирован, отправка подсказки

@bot.message_handler(commands=['stop'])  # Служебная команда для остановки бота (используется в процессе отладки)
@with_session
def stop_bot(session,message):
    current=get_current_data(message.from_user.id)
    if current: 
        if current.admin: # проверка, является ли запросивший остановку бота админом.
            bot.reply_to(message, 'Работа бота прервана!')
            bot.stop_polling()
        else:    
            bot.reply_to(message, 'Вы не можете выполнить эту команду!')
    else:    
        bot.reply_to(message, 'Вы не зарегистрированы!')


@bot.message_handler(func=lambda message: True)
@with_session
def echo_all(session,message): #регистрация 
    current=get_current_data(message.from_user.id)
    if not current:
        if message.text.replace(' ','').isalpha(): #проверка, состоит ли отправленный текст из букв
            fio=session.query(Balance).filter_by(student_fio = message.text.title()).first()   # проверка есть ли запрошенное ФИО в таблице с загруженными балансами
            if fio: # сохранения данных в таблицу students
                session.add(Student(student_fio=message.text.title(),telegram_id=message.from_user.id,threshold=500))
                session.commit()
                bot.reply_to(message, 'Регистрация успешно завершена!')   
                get_balance(message) # отправка текущего баланса
            else:
                bot.reply_to(message, 'Ученик не найден. Проверьте правильность написания фамилии и имени.')   
        else:
            bot.reply_to(message, 'Ученик не найден. Проверьте правильность написания фамилии и имени.')   
    send_current_config(message) # отправка текущих настроек и подсказки по командам]

@with_session
def get_current_data(session,tlg_id):  #Поиск chat_id в таблице students и загрузка данных
    return session.query(Student).filter_by(telegram_id = tlg_id).one_or_none()

def current_config_str(fio,threshold): # формирование строки с текущими настройками
    return f'Ваши текущие настройки:\nФамилия и имя ребенка:  <i><b>{fio}</b></i>\nМинимальный баланс: <i><b>{threshold}</b></i>'

def send_current_config(message):  # отправка текущих настроек и списка доступных команд]
    current=get_current_data(message.from_user.id)
    if current:
	    reply_text = current_config_str(current.student_fio,current.threshold)
    else:
        reply_text = 'Вы не зарегистрированы. Необходимо отправить боту фамилию и имя ребенка.'

    reply_text += '\n\nДоступные команды:\n  /limit - изменить минимальный баланс (например /limit 500)\n  /balance - показать текущий баланс\n\n  /del - отменить регистрацию'
    bot.reply_to(message, reply_text)


def main():
    # logger.add("/volume1/Git/sib_prod/file_{time}.log")
    logger.add("file_{time}.log")
    bot.infinity_polling()

if __name__== '__main__':
    main()
