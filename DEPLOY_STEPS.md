# Пошаговая публикация и настройка Photo AI

## Шаг 1. Загрузить обновлённые файлы в GitHub

Если работаете локально:

```bash
git add -A
git commit -m "Обновление сайта Photo AI: SEO, портфолио, робот ВК"
git push
```

После push GitHub Pages опубликует новую версию сайта.

## Шаг 2. Проверить GitHub Pages

Откройте:

```text
https://retouch-ai-studio.github.io/retouch-ai-studio/
```

Проверьте:

- первый экран;
- калькулятор;
- портфолио;
- кнопку ВК;
- страницы услуг;
- `privacy.html`;
- `sitemap.xml`;
- `robots.txt`.

## Шаг 3. Добавить секрет VK_SERVICE_TOKEN

В GitHub:

```text
Repository → Settings → Secrets and variables → Actions → New repository secret
```

Название секрета:

```text
VK_SERVICE_TOKEN
```

Значение: ваш VK service token.

Важно: не публикуйте токен в README, HTML или открытом коде.

## Шаг 4. Запустить робота вручную

В GitHub:

```text
Actions → Автоматическое обновление сайта из ВКонтакте → Run workflow
```

После выполнения проверьте коммит от `VK-AutoBot`.

## Шаг 5. Подключить Яндекс.Метрику

В `index.html` найдите строку:

```js
window.YANDEX_METRIKA_ID = null;
```

Замените `null` на ID счётчика, например:

```js
window.YANDEX_METRIKA_ID = 12345678;
```

Подготовленные цели:

- `vk_message_click`
- `calculator_click`
- `vk_order_click`
- `copy_order_text`

## Шаг 6. Добавить цели в Яндекс.Метрике

В интерфейсе Метрики создайте JavaScript-события с такими же именами:

```text
vk_message_click
calculator_click
vk_order_click
copy_order_text
```

## Шаг 7. Проверить индексацию

В Яндекс.Вебмастере добавьте сайт и отправьте:

```text
https://retouch-ai-studio.github.io/retouch-ai-studio/sitemap.xml
```

