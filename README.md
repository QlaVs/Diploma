# Дипломный проект
## "Разработка системы мониторинга браузера для предотвращения фишинговых атак"  
В данной дипломной работе в качестве объекта исследования были выделены действия пользователя внутри сети.

Цель работы – Повышение эффективности применения инструментария для обнаружения фишинга и предупреждения пользователя.

В ходе выполнения ВКР был разработан программный модуль для отслеживания посещенных в браузере страниц для обнаружения потенциальной опасности в виде фишингового содержимого, при этом основной новизной данного ПО является объединение нескольких методов оценки страниц и возможность самообучения программы для улучшения алгоритмов оценки. Основная направленность данного ПО – применение в корпоративных сетях или внутри государственных органов для отслеживания действия сотрудников. С экономической стороны проект выигрывает своей дешевизной, так как большая его часть состоит из открытого ПО и общедоступных данных.

:white_check_mark: Работа защищена на оценку `Отлично` :white_check_mark:<br/>

> Также была отмечена практическая ценность разработанного прототипа

## Параметры для модели дерева решений
Данная модель является главной частью проекта и непосредственно через неё происходит определение потенциальных угроз  
  
MY DATA:

    "phishing_url":
       -1 - no log form / can't grab log form
        0 - probably NOT phishing cite
        1 - probably phishing cite

    "rank":
       -1 - bad domain ran (0-3.66/10)
        0 - good domain rank  (3.67-7.33/10)
        1 - best domain rank (7.34-10/10)

    "sus":
       -1 - not sus at all
        0 - URL doesn't contain 3 parts (must be for exp: "www.cite.com";
                                     sometimes its only can be "cite.com", so this flag is "soft")
             / First part of URL is not "WWW" (that's not happened all the time, but its might be suspicious for sure)
            |        OR
        1 - |  Top-level domain name is not popular (for exp: popular: .com, .net, .ru; sus: .xyz, .xxx, .me)
            |        OR
             \ HTTP is not Secure (not HTTPS in URL)

    "password":
        0 - no pass input / didn't grab pass input
        1 - page contains pass input

    "login":
        0 - no log input / didn't grab log input
        1 - page contains log input

    "iframe":
        0 - no iframe tag on page
        1 - iframe tag on page
> Параметр "rank" взят через сайт https://openpagerank.com
<br/>

[IQS](https://www.ipqualityscore.com/) DATA:

    "iqs_phishing":
        0 - "false"
        1 - "true"

    "iqs_sus":
        0 - "false"
        1 - "true"

    "iqs_risk_score":
       -1 - 0-33
        0 - 34-66
        1 - 66-100


Результат:

        -1 - No warning
         1 - Warning

Пример уведомления (Результат == 1):  
![Рисунок1](https://user-images.githubusercontent.com/49796077/176501596-e16f6663-195d-4bd1-9001-1b8b855610df.png)
