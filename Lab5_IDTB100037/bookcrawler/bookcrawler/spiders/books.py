import hashlib, re, scrapy

RATINGS = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}


class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    def __init__(self, max_pages=2, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_pages = max(1, int(max_pages))
        self.pages_seen = 0

    def parse(self, response):
        self.pages_seen += 1

        # TODO: for each card, yield response.follow(href, callback=self.parse_book)
        cards = response.css("article.product_pod h3 a::attr(href)").getall()
        for href in cards:
            yield response.follow(href, callback=self.parse_book)

        # TODO: if pages_seen < max_pages, follow li.next a
        if self.pages_seen < self.max_pages:
            next_page = response.css("li.next a::attr(href)").get()
            if next_page:
                yield response.follow(next_page, callback=self.parse)

    def parse_book(self, response):
        # TODO: extract full detail fields, clean missing values
        title = response.css("div.product_main h1::text").get()
        description = response.css("#product_description + p::text").get() or ""
        category = response.css("ul.breadcrumb li:nth-child(3) a::text").get() or ""

        price = response.css("p.price_color::text").get() or ""
        price_gbp = float(re.sub(r"[^\d.]", "", price)) if price else None

        rating_class = response.css("p.star-rating::attr(class)").get() or ""
        rating = next(
            (value for key, value in RATINGS.items() if key in rating_class.split()),
            None,
        )

        availability = response.css("p.instock.availability::text").getall()
        availability = " ".join(text.strip() for text in availability).strip()

        # TODO: yield an IR-ready dict (see field list above)
        yield {
            "doc_id": response.url.rstrip("/").split("/")[-2],
            "title": title,
            "text": f"{title or ''} {category} {description}".strip(),
            "description": description,
            "url": response.url,
            "category": category,
            "source": "books.toscrape.com",
            "price_gbp": price_gbp,
            "rating": rating,
            "availability": availability,
        }
