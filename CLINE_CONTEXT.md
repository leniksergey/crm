# CLINE_CONTEXT.md — CRM-система на Django

## 0. Назначение файла

Этот файл — единый контекст для Cline. Он описывает бизнес-задачу,
техническое задание, текущее состояние проекта, структуру, модели,
роли, маршруты, шаблоны, настройки Pylint и соглашения. Cline должен
использовать его как источник истины при генерации кода.

---

## 1. Бизнес-задача (кратко)

Разработать CRM-систему (веб-приложение) для автоматизации:
- учёта услуг;
- запуска/завершения рекламных кампаний;
- учёта потенциальных клиентов (лидов), пришедших с кампаний;
- перевода лидов в активных клиентов при заключении контракта;
- подсчёта статистики успешности рекламных кампаний.

Роли: администратор, оператор, маркетолог, менеджер.

---

## 2. Техническое задание (полное)

### 2.1. Основные функции
- авторизация пользователя;
- CRUD услуг (`products`);
- CRUD рекламных кампаний (`ads`);
- CRUD потенциальных клиентов (`leads`);
- CRUD контрактов (`contracts`);
- CRUD активных клиентов (`customers`);
- перевод лида в активного клиента;
- статистика по рекламным кампаниям:
  - сколько привлечено лидов;
  - сколько перешло в активных;
  - соотношение дохода от контрактов и расходов на рекламу.

### 2.2. Страницы (для каждого объекта)
- Список: уникальный идентификатор (например, название) — ссылка на детальную;
  рядом кнопка «Удалить»; на странице — общая кнопка «Создать».
- Детальная: неизменяемая форма + кнопки «Редактировать» и «Удалить».
- Редактирование: предзаполненная форма.
- Создание: пустая форма.

Особенности:
- `leads`: рядом с каждой записью — ссылка «Перевести в активного»,
  ведущая на создание `customer` с предзаполненным `lead`.
- `customers`: при создании поле `lead` предзаполнено, остальные пустые.

### 2.3. Роли и права
| Роль | Права |
|------|-------|
| Администратор | админка Django: создание/просмотр/редактирование пользователей, назначение ролей |
| Оператор | CRUD `Lead` |
| Маркетолог | CRUD `Product`, CRUD `Advertisement` |
| Менеджер | CRUD `Contract`, CRUD `Customer`, просмотр `Lead` |
| Все роли | просмотр статистики |

### 2.4. Поля моделей
- **Услуга:** название, описание, стоимость.
- **Рекламная кампания:** название, рекламируемая услуга (FK), канал продвижения, бюджет.
- **Потенциальный клиент:** Ф. И. О., телефон, email, рекламная кампания (FK).
- **Контракт:** название, услуга (FK), файл документа, дата заключения, период действия, сумма.
- **Активный клиент:** потенциальный клиент (OneToOne/FK), контракт (FK).
  Создаётся только из списка лидов.

### 2.5. Зависимости объектов
Услуга ← Рекламная кампания ← Потенциальный клиент
↑
Контракт ← Активный клиент ─────────┘

text

### 2.6. Требования к коду
- Пользователи и роли — только через стандартную админку Django.
- Остальной функционал — вне админки.
- СУБД — PostgreSQL.
- Подключён Pylint 3.0.2 с `.pylintrc` по инструкции.
- (Опционально) аннотации типов + mypy.
- (Опционально) unit-тесты на pytest + pytest-django.

---

## 3. Стек и окружение

- Python 3.14
- Django (версия из `requirements.txt`)
- PostgreSQL
- Pylint 3.0.2
- Bootstrap 5, Font Awesome (в шаблонах)
- Опционально: mypy, pytest, pytest-django

Корень проекта: `~/PycharmProjects/crm`
Виртуальное окружение: `.venv`

---

## 4. Структура проекта
crm/
├── crm/ # settings.py, urls.py, wsgi.py, asgi.py
├── ads/ # Advertisement + статистика
├── contracts/ # Contract
├── customers/ # Customer
├── leads/ # Lead
├── products/ # Product
├── users/ # кастомная логика ролей (если есть)
├── registration/ # авторизация
├── templates/
│ ├── _base.html # базовый шаблон (sidebar, меню по ролям)
│ ├── ads/
│ ├── contracts/
│ ├── customers/
│ ├── leads/
│ ├── products/
│ ├── registration/
│ └── users/
├── static/
│ └── style.css
├── manage.py
├── requirements.txt
├── .pylintrc
└── CLINE_CONTEXT.md # этот файл

text

Шаблоны взяты из папки `templates_only` и разложены по приложениям.

---

## 5. Модели (ориентир; сверять с фактическим `models.py`)

### products.Product
- `name` — CharField
- `description` — TextField
- `price` — DecimalField

### ads.Advertisement
- `name` — CharField
- `product` — FK → `products.Product`
- `channel` — CharField
- `budget` — DecimalField

### leads.Lead
- `full_name` — CharField
- `phone` — CharField
- `email` — EmailField
- `campaign` — FK → `ads.Advertisement`

### contracts.Contract
- `name` — CharField
- `product` — FK → `products.Product`
- `document` — FileField
- `signed_date` — DateField
- `valid_until` — DateField (или период)
- `amount` — DecimalField

### customers.Customer
- `lead` — OneToOne/FK → `leads.Lead`
- `contract` — FK → `contracts.Contract`

> Имена моделей и полей — уточнять по `models.py` каждого приложения.

---

## 6. Роли и права (группы Django)

| Группа | Права |
|--------|-------|
| Администратор | `is_superuser=True` (админка) |
| Оператор | `leads`: add/change/delete/view `Lead` |
| Маркетолог | `products`: CRUD `Product`; `ads`: CRUD `Advertisement` |
| Менеджер | `contracts`: CRUD `Contract`; `customers`: CRUD `Customer`; `leads`: view `Lead` |

Правила:
- **User permissions у пользователей оставлять пустыми** — доступ только через группу.
- Группы создаются командой `python manage.py setup_roles` (если есть) или вручную
  в админке / через shell.
- Все роли видят «Статистику» (пункт меню без проверки `perms`).

### Проверки в `templates/_base.html`
```django
{% if perms.products.view_product %} ... {% endif %}
{% if perms.ads.view_advertisement %} ... {% endif %}
{% if perms.leads.view_lead %} ... {% endif %}
{% if perms.contracts.view_contract %} ... {% endif %}
{% if perms.customers.view_customer %} ... {% endif %}
Ожидаемое меню:

Оператор: «Лиды», «Статистика», «Выход».

Маркетолог: «Услуги», «Рекламные компании», «Статистика», «Выход».

Менеджер: «Лиды», «Контракты», «Активные клиенты», «Статистика», «Выход».

Если пункт не появляется — проверить наличие view_<model> у группы и
совпадение app_label/model с perms в шаблоне.

7. URL-маршруты (ориентир)
URL	Назначение
/	главная
/accounts/login/	вход
/accounts/logout	выход
/products/	список услуг
/products/<id>/	детальная услуги
/products/create/	создание
/products/<id>/edit/	редактирование
/products/<id>/delete/	удаление
/ads/	список кампаний
/ads/statistic	статистика
/leads/	список лидов
/leads/<id>/to-customer/	перевод лида в активного
/contracts/	список контрактов
/customers/	список активных клиентов
/admin/	админка
Точные пути — по urls.py приложений и проекта.

8. Представления (CBV)
Для каждого объекта:

ListView — список (ссылки на детали, кнопка «Создать», кнопки «Удалить»);

DetailView — неизменяемая форма + «Редактировать»/«Удалить»;

CreateView — пустая форма;

UpdateView — предзаполненная форма;

DeleteView — подтверждение удаления.

Особенности:

Lead → ссылка «Перевести в активного» ведёт на создание Customer
с предзаполненным lead.

Customer при создании: поле lead предзаполнено, остальные пустые.

Доступ по ролям — LoginRequiredMixin + PermissionRequiredMixin.

9. Статистика (/ads/statistic)
Считается по каждой рекламной кампании:

Число привлечённых лидов: Lead.objects.filter(campaign=...).count().

Число перешедших в активных: Customer.objects.filter(lead__campaign=...).count().

Соотношение дохода и расходов: sum(Contract.amount) / Advertisement.budget.

Доступ — всем авторизованным ролям.

10. Pylint — настройка и запуск
Установка:

bash
pip install pylint==3.0.2
Генерация шаблона:

bash
pylint --generate-rcfile > .pylintrc
В .pylintrc внести:

ignore-paths:

text
ignore-paths=.*/migrations/*,.*/settings.py,.*/manage.py,.*/apps.py
disable:

text
disable=raw-checker-failed,
        bad-inline-option,
        locally-disabled,
        file-ignored,
        suppressed-message,
        useless-suppression,
        deprecated-pragma,
        use-implicit-booleaness-not-comparison-to-string,
        use-implicit-booleaness-not-comparison-to-zero,
        use-symbolic-message-instead,
        missing-module-docstring,
        too-many-ancestors
Запуск:

bash
pylint --rcfile .pylintrc crm/*
Категории:

C — конвенции оформления;

W — предупреждения;

E — ошибки.
Оценка от −10 до 10; цель — максимально близко к 10.

11. Полезные команды
bash
source .venv/bin/activate
python manage.py runserver
python manage.py makemigrations
python manage.py migrate
python manage.py shell
python manage.py createsuperuser
pylint --rcfile .pylintrc crm/*
12. Текущий статус
☑ Проект создан, приложения разложены.
☑ Шаблоны из templates_only подключены.
☑ _base.html с меню по ролям.
☑ Группа «Оператор» создана, меню проверено
(видны «Лиды», «Статистика», «Выход»).
☑ Группа «Маркетолог» создана; view_product и view_advertisement добавлены
(проверить итоговое число прав: должно быть 8).
□ Группа «Менеджер» — создать и назначить права
(contracts: CRUD, customers: CRUD, leads: view).
□ Тестовые пользователи operator, marketer, manager.
□ Проверка меню под маркетологом и менеджером в приватном окне.
□ Кнопки «Удалить» во всех списках.
□ Настройка .pylintrc и прогон Pylint.
□ (Опционально) mypy, pytest.
□ Git: коммит и пуш на GitHub (публичный репозиторий).
13. Соглашения для Cline
Не переименовывать приложения (products, ads, leads, contracts,
customers, users, registration) — на них завязаны perms в шаблоне.

Не добавлять пользователям User permissions — только группы.

Добавление прав через shell:

python
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

group = Group.objects.get(name='...')
ct = ContentType.objects.get(model='...')
group.permissions.add(*Permission.objects.filter(content_type=ct))
Если пункт меню не отображается — сначала проверить view_<model> у группы,
затем совпадение app_label/model с perms в шаблоне.

Статистика доступна всем авторизованным; при необходимости ограничить —
LoginRequiredMixin.

При генерации CRUD придерживаться CBV и шаблонов из templates/.

Соблюдать PEP 8 и настройки .pylintrc.

Для файловых полей (Contract.document) настроить MEDIA_ROOT/MEDIA_URL.

Для PostgreSQL — параметры подключения в settings.py (не коммитить секреты).

14. Git и GitHub (по инструкции)
git init (если ещё нет), .gitignore (.venv/, __pycache__/, *.pyc,
media/, .env).

Создать публичный репозиторий на GitHub (кнопка New → Public →
Create repository).

Связать локальный и удалённый репозитории, сделать первый коммит и push.

Не коммитить секреты и media/.

15. Чек-лист перед сдачей
□ Все CRUD-страницы работают для всех объектов.
□ Перевод лида в активного работает, lead предзаполнен.
□ Статистика считается по трём критериям.
□ Роли и права соответствуют ТЗ; меню корректно для каждой роли.
□ PostgreSQL подключён.
□ Pylint запускается без ошибок уровня E; оценка высокая.
□ (Опционально) mypy и pytest проходят.
□ Код в публичном репозитории GitHub.