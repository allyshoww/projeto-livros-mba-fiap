import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

BASE_URL = "https://books.toscrape.com/"
START_URL = BASE_URL + "catalogue/page-1.html"

def get_soup(url):
    response = requests.get(url)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")

def extract_book_info(book, category):
    # Título do livro
    title = book.find("h3").find("a")["title"]
    # Preço (removendo símbolo £ e caracteres especiais)
    price_text = book.find("p", class_="price_color").text.strip()
    # Remove £, Â e outros caracteres não numéricos, mantendo apenas dígitos e ponto
    import re
    price_clean = re.sub(r'[^0-9.]', '', price_text)
    price = float(price_clean)
    # Rating (classe que indica a nota)
    rating_class = book.find("p", class_="star-rating")["class"]
    rating_words = ["Zero", "One", "Two", "Three", "Four", "Five"]
    rating = next((i for i, word in enumerate(rating_words) if word in rating_class), 0)
    # Disponibilidade
    availability = book.find("p", class_="instock availability").text.strip()
    # URL da imagem - corrigindo caminho relativo
    image_rel_url = book.find("img")["src"].replace("../", "")
    image_url = BASE_URL + image_rel_url
    return {
        "title": title,
        "price": price,
        "rating": rating,
        "availability": availability,
        "category": category,
        "image_url": image_url
    }

def get_categories():
    soup = get_soup(BASE_URL)
    category_links = soup.select("div.side_categories ul li ul li a")
    categories = {}
    for cat in category_links:
        name = cat.text.strip()
        url = BASE_URL + cat["href"]
        categories[name] = url
    return categories

def scrape_category(category_name, category_url):
    books = []
    page_url = category_url
    while True:
        soup = get_soup(page_url)
        book_items = soup.select("article.product_pod")
        for book in book_items:
            info = extract_book_info(book, category_name)
            books.append(info)
        next_button = soup.select_one("li.next > a")
        if next_button:
            next_page = next_button["href"]
            # Construir URL da próxima página
            if "catalogue" in page_url:
                base = page_url.rsplit('/', 1)[0] + '/'
            else:
                base = category_url.rsplit('/', 1)[0] + '/'
            page_url = base + next_page
            time.sleep(1)  # Evita sobrecarga do servidor
        else:
            break
    return books

def scrape_all_categories():
    categories = get_categories()
    all_books = []
    for category_name, category_url in categories.items():
        print(f"Extraindo livros da categoria: {category_name}")
        books = scrape_category(category_name, category_url)
        all_books.extend(books)
    return all_books

if __name__ == "__main__":
    print("Iniciando scraping dos livros...")
    all_books_data = scrape_all_categories()
    df = pd.DataFrame(all_books_data)
    df.to_csv("data/books.csv", index=False, encoding="utf-8")
    print(f"Scraping concluído. {len(df)} livros extraídos e salvos em 'data/books.csv'.")
