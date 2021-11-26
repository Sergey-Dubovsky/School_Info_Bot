CREATE OR REPLACE
ALGORITHM = UNDEFINED VIEW `school_balance`.`debtors` AS
select
    `b`.`id` AS `id`,
    `b`.`student_fio` AS `student_fio`,
    `b`.`balance` AS `balance`,
    `s`.`last_balance` AS `last_balance`,
    `s`.`telegram_id` AS `telegram_id`
from
    (`school_balance`.`balances` `b`
join `school_balance`.`students` `s` on
    (`b`.`student_fio` = `s`.`student_fio`))
where
    `b`.`last` <> 0
    and `b`.`balance` < `s`.`threshold`
    and `s`.`disabled` = 0