# COMICS POSTER

Скрипт по загрузке случайного комикса с сайта [XKCD](https://xkcd.com/) и его постингу в [VK](https://vk.com/).

## Предустановка
1. Установите необходимые библиотеки:

Для этого используйте команду:
```shell
pip install -r requirements.txt
```
2. Настройте `.env` - файл:

Внутри этого файла должны быть переменные с вашими секретным данными от VK API:
```
VK_ACCESS_TOKEN=<YOUR-VK-ACCESS-TOKEN>
GROUP_ID=<YOUR-GROUP-ID>
```

Полезные ссылки:
1. Для получения [Access Token VK](https://vk.com/dev/implicit_flow_user)
2. Для получения [VK GROUP ID](https://regvk.com/id/)

## Начало работы
После того, как вы настроили переменные окружения запустите скрипт следующей командой:
```shell
python3 main.py
```
Если в консоле не появилось ошибок - значит пост с комментарием уже в вашем паблике в ВК, скорее его посмотрите и поставьте лайк!

## Создано при помощи
* [Devman](https://dvmn.org/) - Обучающая платформа
* [VK API](https://vk.com/) - Социальная сеть
* [XKCD](https://xkcd.com/) - Сайт с комиксами

## Автор
[Alexander Zharyuk](https://github.com/AlexanderZharyuk/)

