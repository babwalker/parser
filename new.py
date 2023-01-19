import requests
from bs4 import BeautifulSoup
import os
import csv

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
}

products_link = []
products_text = []

def find_products(headers):
    count = 0

    url = "https://www.skylabmodule.com/"

    req = requests.get(url, headers=headers)
    src = req.text

    soup = BeautifulSoup(src, "lxml")

    all_products = soup.find_all("li", class_="menu-item menu-item-type-taxonomy menu-item-object-product_cat")

    for product in all_products:
        products_text.append(product.text)

    for product in all_products:
        product = product.find("a").get("href")
        product = product + "page/"
        products_link.append(product)
        count += 1
        if count > 4:
            break

    count = 0

    for product in products_link:
        os.mkdir(f"D://all/{products_text[count]}")
        count_link = 1
        while True:
            url = f"{product}{count_link}/"
            req = requests.get(url, headers=headers)
            src = req.text

            soup = BeautifulSoup(src, "lxml")
            if soup.find("div", class_="product_list_btm"):
                count_link += 1
                all_cards = soup.find_all("div", class_="col-xl-3")
                for card in all_cards:
                    card = card.find("a").get("href")
                    url = card
                    req = requests.get(url, headers=headers)
                    src = req.text

                    soup = BeautifulSoup(src, "lxml")
                    print(url)
                    if soup.find("h4", class_="products-details-introduce-title") != None:
                        title = soup.find("h4", class_="products-details-introduce-title").text
                    else:
                        title = soup.find("h1", class_="products-details-introduce-subtitle").text
                    subtitle = soup.find("h1", class_="products-details-introduce-subtitle").text
                    if soup.find("div", class_="products-details-introduce-desc").find("p"):
                        description = soup.find("div", class_="products-details-introduce-desc").find("p").text
                    else:
                        description = "Description none"

                    characteristic = soup.find("div", class_="table-wrap").text

                    with open(f"D://all/{products_text[count]}/{title}.csv", "w", encoding="utf=8", newline="") as file:
                        writer = csv.writer(file, delimiter=",")
                        writer.writerow(("subtitle", "description, characteristic"))
                        writer.writerow((subtitle, description, characteristic))
            else:
                print(f"{products_text[count]} сделана")
                count += 1
                break
        

def main():
    find_products(headers=headers)

if __name__ == "__main__":
    main()

