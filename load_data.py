from with_session import with_session
from exclude import excl_list
from gsheetsdb import connect
from models.balance import Balance
from config import GDOCS_URL

# Модуль загрузки данных из Google Docs запускается по cron, либо по команде запроса баланса в боте
# Новые данные по балансу ученика загружаются в базу данных, только если баланс изменился.

# Загрузка из GoogleDocs
def get_table():
    conn = connect()
    return conn.execute(
        f"""
        SELECT 
            "ФИО ученика"  as student_fio, 
            "ОСТАТОК" as balance,
            "ОБЕДЫ Светлана" as meal,
            "Экскурсии Светлана" as excursion,
            "Расход"-"ОБЕДЫ Светлана"-"Экскурсии Светлана" as other
        FROM
            "{GDOCS_URL}"
    """,
        headers=4,
    )


@with_session
def save(session, data):

    for row in data:
        if (
            row.student_fio and row.student_fio not in excl_list
        ):  # Проверка не входит ли ученик в список бывших учеников

            last_rec = (
                session.query(Balance)
                .filter_by(student_fio=row.student_fio, last=True)
                .one_or_none()
            )

            # запрос последнего загруженного баланса
            if last_rec:
                last_balance = last_rec.balance
                last_meal = last_rec.meal
                last_excursion = last_rec.excursion
                last_other = last_rec.other
            else:
                last_balance = 0
                last_meal = 0
                last_excursion = 0
                last_other = 0

            if float(last_balance) != round(
                row.balance, 2
            ):  # проверка изменился ли баланс
                session.query(Balance).filter_by(
                    student_fio=row.student_fio, last=True
                ).update(
                    {"last": False}, synchronize_session="fetch"
                )  # сброс призанка посленего баланса
                session.add(  # добавление записи с новым балансом
                    Balance(
                        student_fio=row.student_fio,
                        last=True,
                        balance=round(row.balance, 2),
                        balance_delta=(round(row.balance, 2) - float(last_balance)),
                        meal=round(row.meal, 2),
                        meal_delta=(round(row.meal, 2) - float(last_meal)),
                        excursion=round(row.excursion, 2),
                        excursion_delta=(
                            round(row.excursion, 2) - float(last_excursion)
                        ),
                        other=round(row.other, 2),
                        other_delta=(round(row.other, 2) - float(last_other)),
                    )
                )
                print(
                    f"{row.student_fio} Баланс: {round(row.balance,2)} ({round(round(row.balance,2)-float(last_balance),2)})"
                )

    session.commit()


def load():
    save(get_table())


def main():
    load()


if __name__ == "__main__":
    main()
