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

global finished_scraping
def create_progressbar(size):

    customtkinter.set_appearance_mode("System")
    customtkinter.set_default_color_theme("blue")


    progress_app = customtkinter.CTk()
    progress_app.geometry("750x500")
    progress_app.title("Scraper Otomoto")

    global progressbar, progress_label
    progressbar = customtkinter.CTkProgressBar(master = progress_app, determinate_speed = 50/size)
    progressbar.pack(pady=10)
    progressbar.set(0)


    progress_label = customtkinter.CTkLabel(master = progress_app, text = "0%")
    progress_label.pack(pady=10)

    progress_app.mainloop()


def increase_progressbar():
    finished_scraping = False
    last_progress = progressbar.get()
    progressbar.step()
    progress_label.configure(text=(round(progressbar.get(), 2)*100, "%"))
    if(progressbar.get()==1 or last_progress > progressbar.get()):
        progress_label.configure(text="Zakończono")
        sleep(2)
        exit()


