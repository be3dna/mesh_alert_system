Метод	Endpoint	            Назначение
POST	/api/auth/register	    Регистрация
POST	/api/auth/login	        Авторизация
POST	/api/auth/logout	    Завершение сессии
POST	/api/auth/refresh	    Обновление токена
POST	/api/auth/restore	    Запрос восстановления доступа
POST	/api/auth/reset-password	Установка нового пароля
GET	    /api/users/me	        Информация о текущем пользователе
PATCH   /api/users/me/password  Обновление пароля через ЛК
PATCH   /api/users/me           Обновление информации о профиле
GET	    /api/users/me/settings	Получение настроек пользователя
PATCH	/api/users/me/settings	Изменение настроек пользователя
GET     /api/users              Получение списка пользователей
GET     /api/users/{id}         Получение профиля пользователя
GET	    /api/alerts	            Список оповещений
POST	/api/alerts	            Создание оповещения
GET	    /api/alerts/{id}	    Получение оповещения
PATCH	/api/alerts/{id}	    Редактирование
DELETE	/api/alerts/{id}	    Удаление (если допустимо)
POST	/api/alerts/{id}/cancel	Отмена оповещения
GET	    /api/alerts/{id}/history	История изменений
GET     /api/alerts/{id}/delivery   Статус доставки оповещения
GET     /api/alerts/{id}/recipients Получатели оповещения
GET     /api/alerts/{id}/statistics Статистика доставки и получения
GET	    /api/alerts/suggested	Предложенные оповещения
POST	/api/alerts/suggested	Предложение оповещения
POST	/api/alerts/suggested/{id}/approve	Подтверждение
POST	/api/alerts/suggested/{id}/reject	Отклонение
GET     /api/areas              Список территорий
POST    /api/areas              Создание территории
GET     /api/areas/{id}         Данные о территории
PATCH   /api/areas/{id}         Обновление данных о территории
GET     /api/areas/{id}/alerts  Оповещения в пределах территории
GET	    /api/nodes	            Список узлов
POST	/api/nodes	            Регистрация узла
GET	    /api/nodes/{id}	        Информация об узле
PATCH	/api/nodes/{id}	        Изменение информации
DELETE	/api/nodes/{id}	        Удаление узла
GET	    /api/nodes/{id}/status	Текущее состояние
GET	    /api/nodes/{id}/metrics	Метрики узла
GET	    /api/nodes/{id}/neighbors	Соседние узлы
PATCH	/api/nodes/{id}/settings	Конфигурация узла
POST    /api/nodes/{id}/heartbeat   Передача информации о состоянии узла
POST    /api/nodes/{id}/telemetry   Передача телеметрии
GET     /api/nodes/{id}/commands    Получение доступных комманд
POST    /api/nodes/{id}/commands    отправка команды
GET	    /api/nodes/{id}/log    Получение логов узла
GET	    /api/nodes/{id}/sound-commands	Доступные команды конкретного узла
GET	    /api/admin/logs	        Системный журнал
GET	    /api/admin/dashboard	Статистика
GET	    /api/admin/services	    Список сервисов
PATCH	/api/admin/services/{id}	Управление сервисом
GET	    /api/admin/sync	        Состояние синхронизации
POST    /api/admin/users        Создание пользователя админом
DELETE  /api/admin/users/{id}   Удаление пользователя
PATCH   /api/admin/users/{id}   Изменение личной информации пользователя
PATCH   /api/admin/users/{id}/status    Обновление статуса пользователя(блокировка/разблокировка)
GET     /api/admin/users/{id}/history   Получение истории изменения пользователя
GET     /api/admin/users/{id}/log   Получение лога действий пользователя   
PATCH   /api/admin/users/{id}/role  Изменение роли пользователя
GET	    /api/admin/settings	    Получение системных настроек
PATCH	/api/admin/settings	    Изменение системных настроек
GET	    /api/sound-commands	    Список звуковых команд
GET	    /api/sound-commands/{id}	Информация о команде