= README =

Эта папка содержит документацию проекта Leams в формате MediaWiki.

== Структура файлов ==

* '''Index.wiki''' — Главная страница проекта (английская версия index.md)
* '''Main_Page.wiki''' — Главная страница документации (русская версия)
* '''Installation.wiki''' — Руководство по установке и настройке
* '''Architecture.wiki''' — Архитектура проекта
* '''API_Overview.wiki''' — Документация по API
* '''Streaming_Setup.wiki''' — Настройка стриминга
* '''FAQ.wiki''' — Часто задаваемые вопросы
* '''Contributing.wiki''' — Руководство для контрибьюторов

== Как использовать ==

=== Важно! ===

⚠️ '''НЕ копируйте содержимое файлов напрямую из исходных .md файлов!''' 

Файлы .wiki уже конвертированы в правильный формат MediaWiki. Исходные Markdown файлы содержат HTML теги и специфичный для MkDocs синтаксис, который не будет корректно работать в MediaWiki.

=== Создание страниц в MediaWiki ===

==== Метод 1: Через веб-интерфейс ====

# Зайдите на ваш MediaWiki сайт
# Создайте новую страницу с правильным названием (например, "Installation")
# Откройте соответствующий .wiki файл из этой папки
# Скопируйте '''весь текст из .wiki файла'''
# Вставьте в редактор MediaWiki
# Сохраните страницу

==== Метод 2: Special:Import ====

# Зайдите в Special:Import на вашем MediaWiki сайте
# Загрузите .wiki файлы
# Или используйте API для автоматического импорта

=== Использование скрипта импорта ===

<syntaxhighlight lang="bash">
#!/bin/bash
# import_to_mediawiki.sh

WIKI_URL="https://your-wiki.com/api.php"
BOT_USERNAME="YourBot"
BOT_PASSWORD="YourPassword"

# Функция для импорта страницы
import_page() {
    local file=$1
    local title=$2
    local content=$(cat "$file")
    
    # Получение токена
    token=$(curl -s "${WIKI_URL}?action=query&meta=tokens&type=csrf&format=json" \
        -b cookies.txt \
        | jq -r '.query.tokens.csrftoken')
    
    # Создание/обновление страницы
    curl -s "${WIKI_URL}" \
        -b cookies.txt \
        -d "action=edit" \
        -d "title=${title}" \
        -d "text=${content}" \
        -d "token=${token}" \
        -d "format=json"
}

# Авторизация
curl -s "${WIKI_URL}" \
    -c cookies.txt \
    -d "action=login" \
    -d "lgname=${BOT_USERNAME}" \
    -d "lgpassword=${BOT_PASSWORD}" \
    -d "format=json"

# Импорт всех страниц
import_page "Main_Page.wiki" "Main Page"
import_page "Installation.wiki" "Installation"
import_page "Architecture.wiki" "Architecture"
import_page "API_Overview.wiki" "API Overview"
import_page "Streaming_Setup.wiki" "Streaming Setup"
import_page "FAQ.wiki" "FAQ"
import_page "Contributing.wiki" "Contributing"

echo "Import completed!"
</syntaxhighlight>

== Конвертация из Markdown ==

Основные изменения при конвертации из Markdown в MediaWiki:

{| class="wikitable"
! Markdown !! MediaWiki
|-
| <code># Heading</code> || <code>= Heading =</code>
|-
| <code>## Heading 2</code> || <code>== Heading 2 ==</code>
|-
| <code>**bold**</code> || <code>'''bold'''</code>
|-
| <code>*italic*</code> || <code>''italic''</code>
|-
| <code>[text](url)</code> || <code>[url text]</code>
|-
| <code>`code`</code> || <code>&lt;code&gt;code&lt;/code&gt;</code>
|-
| <code>```lang</code> || <code>&lt;syntaxhighlight lang="lang"&gt;</code>
|-
| <code>- item</code> || <code>* item</code>
|-
| <code>1. item</code> || <code># item</code>
|-
| <code>---</code> || <code>----</code>
|}

== Дополнительные шаблоны ==

⚠️ '''Важно:''' В файлах используются символы вместо MediaWiki шаблонов для обеспечения совместимости:

* ✓ — используется вместо <code><nowiki>{{Yes}}</nowiki></code>
* ✗ — используется вместо <code><nowiki>{{No}}</nowiki></code>
* ⚠️ — используется вместо <code><nowiki>{{Warning}}</nowiki></code>

Если в вашей MediaWiki установлены соответствующие шаблоны, вы можете заменить символы на шаблоны.

== Категории ==

Все страницы помечены категориями для удобной навигации:

* <nowiki>[[Category:Documentation]]</nowiki>
* <nowiki>[[Category:Installation]]</nowiki>
* <nowiki>[[Category:Architecture]]</nowiki>
* <nowiki>[[Category:API]]</nowiki>
* <nowiki>[[Category:Streaming]]</nowiki>
* <nowiki>[[Category:FAQ]]</nowiki>
* <nowiki>[[Category:Contributing]]</nowiki>

== Обновление документации ==

При обновлении Markdown документации не забудьте также обновить соответствующие .wiki файлы в этой папке.

Можно использовать автоматический конвертер (например, pandoc):

<syntaxhighlight lang="bash">
# Конвертация Markdown в MediaWiki
pandoc -f markdown -t mediawiki input.md -o output.wiki
</syntaxhighlight>

Однако после автоматической конвертации потребуется ручная доработка для:
* Исправления внутренних ссылок
* Добавления категорий
* Использования MediaWiki-специфичных шаблонов
* Форматирования таблиц

== Полезные ссылки ==

* [https://www.mediawiki.org/wiki/Help:Formatting MediaWiki Formatting Help]
* [https://www.mediawiki.org/wiki/Manual:Contents MediaWiki Manual]
* [https://www.mediawiki.org/wiki/API:Main_page MediaWiki API]

== Контакты ==

При вопросах о документации:
* GitHub Issues: https://github.com/azlamire/Leams/issues
* Discord: https://discord.gg/leams
* Email: docs@leams.com
