import requests
from bs4 import BeautifulSoup


class ForumParser:
    HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "ru-RU,ru;q=0.9,en;q=0.8",
    }

    def __init__(self, session=None):
        self.session = session or requests.Session()
        self.session.headers.update(self.HEADERS)

    # ---------- 1. скачать HTML ----------
    def fetch(self, url: str) -> str:
        response = self.session.get(url, timeout=10)
        response.raise_for_status()
        return response.text

    # ---------- 2. распарсить HTML ----------
    def parse_html(self, html: str):
        """Разбирает готовый HTML — удобно для тестов."""
        soup = BeautifulSoup(html, "lxml")
        results = []

        # Ищем контейнеры сообщений по распространённым селекторам.
        # Под вашу конкретную страницу селекторы можно уточнить.
        posts = soup.select(
            ".post, .message, .comment, article.message, div[data-post-id]"
        )
        if not posts:
            return results

        for post in posts:
            # ID сообщения: data-post-id, id="post-123", href="#post-123"
            post_id = (
                post.get("data-post-id")
                or (post.get("id", "").replace("post-", "") or None)
            )
            if not post_id:
                link = post.select_one("a[href*='#post-']")
                if link:
                    post_id = link["href"].split("#post-")[-1]
            if not post_id:
                continue

            # Логин автора
            author_tag = post.select_one(
                ".author, .username, .nickname, a[rel='author'], [data-author]"
            )
            if author_tag is None:
                continue
            username = author_tag.get("data-author") or author_tag.get_text(strip=True)

            # Тело сообщения (с сохранением HTML внутри)
            body_tag = post.select_one(".message-body, .post-content, .body, .text")
            if body_tag is None:
                continue
            message = body_tag.decode_contents()  # HTML внутри как строка

            results.append(
                {
                    "id": int(post_id),
                    "name": username,
                    "message": message,
                }
            )
        return results

    # ---------- 3. скачать + распарсить ----------
    def parse_page(self, url: str):
        return self.parse_html(self.fetch(url))

    # ---------- 4. сохранить в БД ----------
    def save_to_db(self, parsed_data, repository) -> int:
        saved = 0
        for item in parsed_data:
            try:
                if repository.add(item["id"], item["name"], item["message"]):
                    saved += 1
            except ValueError:
                # уже есть такой ID — пропускаем (или можно обновлять)
                continue
        return saved