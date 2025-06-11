from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin




if __name__ == '__main__':
    #link podstawowy
    base_url = "https://www.otomoto.pl/osobowe?search%5Border%5D=relevance_web"
    #print("search how many pages?: ")
    #number_of_pages= int(input())

    number_of_pages = 1

    offer_links = []
    offer_models = []
    offer_years = []
    offer_brands = []
    offer_mileages = []
    offer_prices = []



    for page_number in range(0, number_of_pages):  #for do przechodzenia między wyznaczonymi stronami OLX
        if(page_number > 0):
            url = f"{base_url}&page={page_number}"  # do bazowego linku do strony dodajemy ?page={numer strony} co pozwala przechodzic miedzy stronami
        elif(page_number == 0):
            url = base_url

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        }

        url = "https://www.otomoto.pl/osobowe"
        response = requests.get(url, headers=headers)
        doc = BeautifulSoup(response.text, 'html.parser')

        #lista wszystkich znalezionych linków na stronie - zawiera niepoprawne linki i przekierowania
        link_tag = doc.find_all("a", href=True)
        all_links = [tag.get("href") for tag in link_tag if tag.get("href")]

        #szukamy tylko linków prowadzących na stronę otomoto - do tego co drugi, do każdej jednej oferty są przypisane dwa takie same linki
        base_url = "https://www.otomoto.pl"

        #offer_links_with_duplicates - oferty już po przefiltrowaniu ale z duplikatami
        offer_links_with_duplicates = [
            urljoin(base_url, link) for link in all_links if "/osobowe/oferta/" in link
        ]

        seen_links = set()
        for n in range(len(offer_links_with_duplicates)):
            if offer_links_with_duplicates[n] not in seen_links:
                offer_links.append(offer_links_with_duplicates[n])
                seen_links.add(offer_links_with_duplicates[n])


        price_tags = doc.find_all("h3", class_="efzkujb1 ooa-1d59yzt")
        offer_prices = [tag.get_text(strip=True) for tag in price_tags]

        # Extract mileage
        mileage_tags = doc.find_all("dd", attrs={"data-parameter": "mileage"})
        offer_mileages = [tag.get_text(strip=True) for tag in mileage_tags]

        # Extract production year
        year_tags = doc.find_all("dd", attrs={"data-parameter": "year"})
        offer_years = [tag.get_text(strip=True) for tag in year_tags]

        fuel_tags = doc.find_all("dd", attrs={"data-parameter": "fuel_type"})
        fuel_types = [tag.get_text(strip=True) for tag in fuel_tags]

        gearbox_tags = doc.find_all("dd", attrs={"data-parameter": "gearbox"})
        gearbox_types = [tag.get_text(strip=True) for tag in gearbox_tags]



        #wyświetlam wszystkie znalezione oferty
        print(f"----- Offers from page {page_number+1} -----")
        for n in range(len(offer_prices)):
            print(f"Oferta nr.{n+1}")
            print(f"link: {offer_links[n]}")
            print(f"cena: {offer_prices[n]}")
            print(f"przebieg: {offer_mileages[n]}")
            print(f"rok produkcji: {offer_years[n]}")
            print(f"S{fuel_types[n]}")
            print(f"skrzynia biegów: {gearbox_types[n]}")
