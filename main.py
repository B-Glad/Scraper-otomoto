from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
import time
import pandas as pd
from charts import create_statistics_charts
from datetime import datetime
from GUI import create_app, closing_app
from scrapinfo import ScrapInfo
import os


def get_html(url):
    # Otomoto blokuje nasz request jeżeli zrobimy go bez headera
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"}
    response = requests.get(url, headers=header)
    return BeautifulSoup(response.text, 'html.parser')


def show_offers(offer_links, offer_years, offer_brands, offer_mileages, offer_prices, offer_colors, offer_seats,
                fuel_types, gearbox_types, more_informations):
    for n in range(len(offer_links)):
        print(f"Oferta nr.{n + 1}")
        print(f"Link do oferty: {offer_links[n]}")
        print(f"Cena: {offer_prices[n]}")
        print(f"Przebieg: {offer_mileages[n]}")
        print(f"Rok produkcji: {offer_years[n]}")
        print(f"{fuel_types[n]}")
        print(f"skrzynia biegów: {gearbox_types[n]}")
        if more_informations:
            print(f"Marka: {offer_brands[n]}")
            print(f"Ilość siedzeń w samochodzie: {offer_seats[n]}")
            print(f"Kolor: {offer_colors[n]}")
        print("\n")
    print("\n \n")


if __name__ == '__main__':

    scraper_info = create_app()
    print("proccesing")

    print("still processing")

    # link podstawowy
    otomoto_url = "https://www.otomoto.pl/osobowe?search%5Border%5D=relevance_web"
    more_informations = scraper_info.more_info
    number_of_pages = scraper_info.number_of_pages

    all_offers = []  # List to accumulate all offers as dicts

    for page_number in range(0, number_of_pages):
        offer_links = []
        offer_years = []
        offer_brands = []
        offer_mileages = []
        offer_prices = []
        offer_colors = []
        offer_seats = []
        fuel_types = []
        gearbox_types = []

        url = ""
        if (page_number > 0):
            url = f"{otomoto_url}&page={page_number}"
        elif (page_number == 0):
            url = otomoto_url

        doc = get_html(url)

        link_tag = doc.find_all("a", href=True)
        all_links = [tag.get("href") for tag in link_tag if tag.get("href")]

        offer_links_with_duplicates = [
            urljoin(otomoto_url, link) for link in all_links if "/osobowe/oferta/" in link
        ]

        seen_links = set()
        for n in range(len(offer_links_with_duplicates)):
            if offer_links_with_duplicates[n] not in seen_links:
                offer_links.append(offer_links_with_duplicates[n])
                seen_links.add(offer_links_with_duplicates[n])

        price_tags = doc.find_all("h3", class_="efzkujb1 ooa-1d59yzt")
        offer_prices = [tag.get_text(strip=True) for tag in price_tags]

        mileage_tags = doc.find_all("dd", attrs={"data-parameter": "mileage"})
        offer_mileages = [tag.get_text(strip=True) for tag in mileage_tags]

        year_tags = doc.find_all("dd", attrs={"data-parameter": "year"})
        offer_years = [tag.get_text(strip=True) for tag in year_tags]

        fuel_tags = doc.find_all("dd", attrs={"data-parameter": "fuel_type"})
        fuel_types = [tag.get_text(strip=True) for tag in fuel_tags]

        gearbox_tags = doc.find_all("dd", attrs={"data-parameter": "gearbox"})
        gearbox_types = [tag.get_text(strip=True) for tag in gearbox_tags]

        if more_informations:
            for n in range(len(offer_links)):
                offer_doc = get_html(offer_links[n])

                brand_tag = offer_doc.find("p", class_="eur4qwl9 ooa-10u0vtk")
                if brand_tag:
                    offer_brands.append(brand_tag.get_text(strip=True))
                else:
                    offer_brands.append("NA")

                color_container = offer_doc.find("div", {"data-testid": "color"})
                if color_container:
                    color_tag = color_container.find("p", class_="eur4qwl9 ooa-10u0vtk")
                    if color_tag:
                        offer_colors.append(color_tag.get_text(strip=True))
                    else:
                        offer_colors.append("NA")
                else:
                    offer_colors.append("NA")

                seats_container = offer_doc.find("div", {"data-testid": "nr_seats"})
                if seats_container:
                    seats_tag = seats_container.find("p", class_="eur4qwl9 ooa-10u0vtk")
                    if seats_tag:
                        offer_seats.append(seats_tag.get_text(strip=True))
                    else:
                        offer_seats.append("NA")
                else:
                    offer_seats.append("NA")
        else:
            offer_brands = ["NA"] * len(offer_links)
            offer_colors = ["NA"] * len(offer_links)
            offer_seats = ["NA"] * len(offer_links)

        # Ensure all lists are the same length
        min_len = min(len(offer_links), len(offer_years), len(offer_brands), len(offer_mileages), len(offer_prices),
                      len(offer_colors), len(offer_seats), len(fuel_types), len(gearbox_types))
        offer_links = offer_links[:min_len]
        offer_years = offer_years[:min_len]
        offer_brands = offer_brands[:min_len]
        offer_mileages = offer_mileages[:min_len]
        offer_prices = offer_prices[:min_len]
        offer_colors = offer_colors[:min_len]
        offer_seats = offer_seats[:min_len]
        fuel_types = fuel_types[:min_len]
        gearbox_types = gearbox_types[:min_len]

        print(f"----- Oferty ze strony {page_number + 1} -----")
        show_offers(offer_links, offer_years, offer_brands, offer_mileages, offer_prices, offer_colors, offer_seats,
                    fuel_types, gearbox_types, more_informations)

        for i in range(min_len):
            all_offers.append({
                'link': offer_links[i],
                'Rok produkcji': offer_years[i],
                'Marka': offer_brands[i],
                'Przebieg': offer_mileages[i],
                'Cena': offer_prices[i],
                'Kolor': offer_colors[i],
                'Liczba siedzeń': offer_seats[i],
                'Rodzaj paliwa': fuel_types[i],
                'Skrzynia biegów': gearbox_types[i],
            })

    if all_offers:
        data_frame = pd.DataFrame(all_offers)

        # Generate timestamp for unique filenames
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        excel_filename = os.path.join(scraper_info.save_path, f'otomoto_offers_{timestamp}.xlsx')

        try:
            data_frame.to_excel(excel_filename, index=False)
            print(f"Dane zapisane do pliku {excel_filename}")

            # Create and save statistics charts
            try:
                closing_app(excel_filename)
                stats_file, fuel_file = create_statistics_charts(data_frame, scraper_info.save_path)
                print(f"Wykresy statystyczne zostały zapisane jako interaktywne pliki HTML:")
                print(f"- {stats_file}")
                print(f"- {fuel_file}")
                print("Otwórz te pliki w przeglądarce internetowej, aby zobaczyć interaktywne wykresy.")
            except Exception as e:
                print(f"Błąd podczas generowania wykresów: {str(e)}")

        except PermissionError:
            print("Błąd: Nie można zapisać pliku Excel. Upewnij się, że plik nie jest otwarty w innym programie.")
        except Exception as e:
            print(f"Wystąpił nieoczekiwany błąd podczas zapisywania danych: {str(e)}")
    else:
        print("Brak ofert do zapisania.")

