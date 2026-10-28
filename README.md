# CRM-система на Django

Веб-приложение для автоматизации учёта услуг, рекламных кампаний, потенциальных клиентов (лидов), контрактов и активных
клиентов, а также подсчёта статистики эффективности рекламы.

## Возможности

- Авторизация пользователей
- CRUD услуг (`Product`)
- CRUD рекламных кампаний (`Advertisement`)
- CRUD потенциальных клиентов (`Lead`)
- Воронка лидов: новый, связались, переговоры, успешно, отказ
- CRUD контрактов (`Contract`)
- CRUD активных клиентов (`Customer`)
- Перевод лида в активного клиента
- Статистика по рекламным кампаниям:
    - количество привлечённых лидов
    - количество перешедших в активных клиентов
    - конверсия лидов в активных клиентов
    - выручка по контрактам
    - ROAS — отношение выручки к расходам на рекламу

## Роли и права

| Роль          | Права                                                                            |
|---------------|----------------------------------------------------------------------------------|
| Администратор | Админка Django, создание/просмотр/редактирование пользователей, назначение ролей |
| Оператор      | CRUD `Lead`                                                                      |
| Маркетолог    | CRUD `Product`, CRUD `Advertisement`                                             |
| Менеджер      | CRUD `Contract`, CRUD `Customer`, просмотр `Lead`                                |
| Все роли      | Просмотр статистики                                                              |

Права выдаются через группы Django (`Group`). Прямые `user_permissions` пользователям не назначаются. Кнопки действий в интерфейсе отображаются только при наличии соответствующего разрешения.

## Воронка лидов

Оператор фиксирует статус работы с лидом. В активного клиента можно перевести
только лида со статусом «Успешно». Один лид может стать активным клиентом только
один раз: это обеспечивается связью `OneToOne` и фильтрацией доступных лидов в
форме создания клиента.

## Стек

- Python 3.14
- Django 6.1.2
- PostgreSQL
- Pylint 3.0.2
- Bootstrap 5, Font Awesome (в шаблонах)

## Установка и запуск

### 1. Клонирование репозитория

```bash
git clone https://github.com/leniksergey/crm.git
cd crm
```

### 2. Виртуальное окружение

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Переменные окружения

Скопируйте `.env.example` в `.env` и заполните параметры PostgreSQL:

```env
SECRET_KEY=ваш_секретный_ключ
DEBUG=True
DB_NAME=crm_db
DB_USER=crm_user
DB_PASSWORD=crm_password
DB_HOST=localhost
DB_PORT=5432
```

### 4. База данных

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py setup_roles          # создаёт группы-роли и права
python manage.py create_test_users    # создаёт тестовых пользователей
python manage.py create_test_data     # создаёт тестовые данные
python manage.py createsuperuser      # суперпользователь для админки
```

### 5. Запуск сервера

```bash
python manage.py runserver
```

Приложение доступно по адресу: `http://127.0.0.1:8000/`

## Тестовые пользователи

| Username | Пароль      | Группа     |
|----------|-------------|------------|
| operator | password123 | Оператор   |
| marketer | password123 | Маркетолог |
| manager  | password123 | Менеджер   |

## Управленческие команды

```bash
python manage.py setup_roles        # Создать группы-роли и выдать права
python manage.py create_test_users  # Создать тестовых пользователей
python manage.py create_test_data   # Создать тестовые данные
python manage.py createsuperuser    # Создать суперпользователя
```

## Pylint

```bash
pylint --rcfile .pylintrc products ads leads contracts customers users config
```

Цель — оценка максимально близкая к 10/10.

## Тесты

```bash
python manage.py test
```

Тесты проверяют матрицу доступа ролей, воронку лидов, доступность лидов для перевода в клиента и расчёт показателей рекламных кампаний.

## Структура проекта

```
crm/
├── config/           # настройки проекта (settings.py, urls.py)
├── ads/              # Advertisement + статистика
├── contracts/        # Contract
├── customers/        # Customer
├── leads/            # Lead
├── products/         # Product
├── users/            # кастомная логика ролей, миксины, команды
├── templates/        # шаблоны (Bootstrap 5)
├── static/           # статические файлы
├── media/            # загруженные файлы (договоры)
├── manage.py
├── requirements.txt
├── .pylintrc
├── .env.example
└── README.md
```

## Маршруты

| URL                      | Назначение               |
|--------------------------|--------------------------|
| `/`                      | Главная                  |
| `/accounts/login/`       | Вход                     |
| `/accounts/logout`       | Выход                    |
| `/products/`             | Список услуг             |
| `/products/<id>/`        | Детальная услуга         |
| `/products/new/`         | Создание услуги          |
| `/products/<id>/edit/`   | Редактирование услуги    |
| `/products/<id>/delete/` | Удаление услуги          |
| `/ads/`                  | Список кампаний          |
| `/ads/statistic/`        | Статистика кампаний      |
| `/leads/`                | Список лидов             |
| `/leads/new/`            | Создание лида            |
| `/leads/<id>/delete/`    | Удаление лида            |
| `/contracts/`            | Список контрактов        |
| `/customers/`            | Список активных клиентов |
| `/admin/`                | Админка Django           |

## Лицензия

MIT
