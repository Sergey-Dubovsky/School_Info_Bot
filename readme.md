## Назначение
Проект был сделан для автоматизации уведомлений о необходимости пополнения баланса в школьном родительском комитете на экскурсии, обеды и другие общие расходы.

## Исходные данные.
Родительский комитет ведет в GoogleDocs таблицу, где есть колонки ФИО ученика (Фамилия Имя), ОСТАТОК, ОБЕДЫ, ЭКСКУРСИИ и т.д. 
Родительский комитет вносит в таблицу траты, которые приводят к изменению графы ОСТАТОК, а родители должны периодически проверять таблицу и вносить деньги 
по мере расходования, чтоб ыне уходить в минус. Хотелось упростить жизнь родителям и родительскому комитету.

Проект состоит из трех модулей, работающих с общей базой данных через SQLAlchemy. Все модули запускаются на домашнем NAS Synology (на Linux), используется MariaDB. 

## База данных 
Состоит из двух таблиц: balances и students.

Таблица **balances** содержит периодически загружаемые из GoogleDocs данные по остатку и статьям расходов, а также ФИО ученика (по которому делается отбор). 
В итоге в этой таблице формируется история изменения балансов с датой загрузки. Последний баланс помечается в поле last=1 для каждого ученика.

Таблица **students** содержит telegram_id привязанный к ФИО ученика, а также настройки уведомлений. Для одного ученика может быть несколько записей, на случай если несколько родственников захочет мониторить баланс. Настройки в этом случае могут различаться для каждого родственника.

## Модули
Модуль **load_data.py** запускается по cron и несколько раз в сутки загружает данные из GoogleDocs в базу данных. Данные грузятся только если есть изменения

Модуль **send_warn.py** запускается раз в сутки по cron и отправляет уведомления в Telegram тем родителям, у которых баланс ниже заданного значения. При этом если баланс не меняется, то повторное уведомление на следующий день не отправляется. По субботам уведомление с балансом отправляется в любом случае, если баланс ниже заданного.

Модуль **tlg_bot.py** - модуль Telegram-бота, работающий в polling режиме. 
Используется для:
- регистрации (привязки chat_id (поле telegram_id) пользователя к имени ученика в таблице students),
- изменения граничного значения (threshold) для отправки уведомлений (/limit)
- отмены регистрации (/del)
- для запросов актуального баланса (/balance),
- для запросов истории изменений баланса (/hist),

В файле config.py, который не включен в репозиторий, находятся три переменные, содержащие URL таблицы в GoogleDocs, строку подключения к БД 
и токен Telegtram-бота (GDOCS_URL, CONN_STR, TELEGRAM_TOKEN)

