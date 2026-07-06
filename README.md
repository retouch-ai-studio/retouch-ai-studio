# ✦ Photo AI Studio

Лендинг студии AI-ретуши, бизнес-портретов, нейро-образов и реставрации фотографий.

## Что входит

- Главная страница `index.html` с калькулятором, портфолио, FAQ и CTA в ВК.
- SEO-страницы под услуги:
  - `/retush-foto-online/`
  - `/biznes-portret-po-foto/`
  - `/restavraciya-staryh-foto/`
  - `/ai-avatar-po-foto/`
  - `/foto-dlya-rezyume/`
- Страница конфиденциальности `privacy.html`.
- Open Graph preview `preview.jpg`.
- `robots.txt` и `sitemap.xml`.
- Изображения вынесены из base64 в `assets/images/`, поэтому HTML стал легче и быстрее.

## Автообновление портфолио из ВК

Робот находится в `.github/workflows/update_site.yml`.

Каждый день по расписанию workflow запускает:

```bash
python scripts_and_raw_data/fetch_all_vk.py
python scripts_and_raw_data/build_site.py
```

`fetch_all_vk.py` берёт свежие записи из ВК через API, скачивает фотографии в `assets/images/` и обновляет `vk_posts_all.json`.

Для полноценной работы нужно добавить в GitHub Secrets один из секретов:

- `VK_SERVICE_TOKEN`, предпочтительно;
- или `VK_TOKEN`.

Если токена нет, робот не ломает сайт: он просто сохраняет текущую базу портфолио и завершает работу успешно.

`build_site.py` не пересоздаёт дизайн сайта целиком. Он только вставляет свежий массив `ALL_POSTS` в `index.html`, поэтому ручные правки дизайна и текстов не перетираются.

## Аналитика

В коде уже подготовлены события:

- `vk_message_click`
- `calculator_click`
- `vk_order_click`
- `copy_order_text`

Чтобы включить Яндекс.Метрику, добавьте стандартный код Метрики и ID счётчика в `window.YANDEX_METRIKA_ID`.

## Контакты

- Группа ВК: https://vk.com/retouch_ai_online
- Сообщения ВК: https://vk.com/im?sel=-239853638
