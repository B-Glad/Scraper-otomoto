from pydoc import describe
from time import sleep

import customtkinter
from customtkinter import CTkOptionMenu, filedialog
from scrapinfo import ScrapInfo
import threading
from threading import Event, Thread


def create_app() -> ScrapInfo | None:
    def button_clicked():
        nonlocal clicked
        clicked = True
        print("button clicked")
        app.quit()


    def increase(value):
        slider_label.configure(text=int(value))



    customtkinter.set_appearance_mode("System")
    customtkinter.set_default_color_theme("blue")

    app = customtkinter.CTk()
    app.geometry("750x500")
    app.title("Scraper Otomoto")

    clicked = False

    text = customtkinter.CTkLabel(app, text="Czy wyświetlić dodatkowe informacje?:")
    text.pack(pady=10)

    optionmenu = CTkOptionMenu(master=app, values=["Tak", "Nie"])
    optionmenu.set("Tak")
    optionmenu.pack(pady=10)

    slider = customtkinter.CTkSlider(master=app, from_=1, to=30, command=increase)
    slider.pack(pady=10)

    slider_label = customtkinter.CTkLabel(master=app, text="15", font=("Helvetica", 12))
    slider_label.pack(pady=10)

    button = customtkinter.CTkButton(
        master=app,
        text="Zatwierdź",
        fg_color="purple",
        command=button_clicked
    )
    button.pack(pady=10)

    app.mainloop()

    more_info = True if optionmenu.get() == "Tak" else False
    pages = int(slider.get())

    if clicked:
        print("creating an object")
        scrape_info = ScrapInfo(more_info, pages)
        print(scrape_info.more_info)
        print(scrape_info.number_of_pages)
        app.quit()
        app.destroy()
        return scrape_info
    else:
        print("błąd działania GUI aplikacji")
        exit()

def closing_app():
    customtkinter.set_appearance_mode("System")
    customtkinter.set_default_color_theme("blue")

    app = customtkinter.CTk()
    app.geometry("400x50")
    app.title("Scraper Otomoto")

    text = customtkinter.CTkLabel(app, text="zakonczono działanie aplikacji")
    text.pack(pady=10)
    app.mainloop()



