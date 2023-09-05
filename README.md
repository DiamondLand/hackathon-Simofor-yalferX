# Онбординг Telegram Bot Python + PostgreSQL!

---

### 💖 О проекте:

Проект создавался за 1 день в рамках хакатона Code Rocks 2023 и является сырым. Если вам требуется пример интересного бота для проведения онбординг - рекомендую рассмотреть данных проект и в нынешнем readme я расскажу о плюсах и минусах.

---

### 💎 Плюсы:

- Панель администратора с возможностью контролировать прохождения онбординг, а также добавлением анкет для знакомства с коллективом.

- Отдельный файл с некоторыми ответами и кнопками бота для быстрой настройки.
  
- Использование FSM для перемещения по этапам тестирования и временного хранения данных с них.

- Вынос требуемых функций для настройки по отдельным файлам (postgres_db.py, binary.py).

- Не малое количество проверок на допуск ошибок пользователем при заполнении полей тестирования.

  
---

### 💀 Минусы:

- Синхронная база данных при иных асинхронных библиотек, использоуемых в боте.

-  Код написанный на скорую руку.

- Требуется ручная настройка фотографий в бинарном коде базы данных.

- Некоторые ответы бота "вшиты" в код.

- Нельзя выбрать нескольких администраторов в панель. Только 1 ID пользователя (в settings)