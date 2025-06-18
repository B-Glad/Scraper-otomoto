from pydoc import describe
from time import sleep
import customtkinter
from customtkinter import CTkOptionMenu, filedialog, CTkProgressBar
from scrapinfo import ScrapInfo
import os

def create_app() -> ScrapInfo | None:
    def button_clicked():
        nonlocal clicked
        clicked = True
        print("button clicked")
        app.quit()


    def increase(value):
        slider_label.configure(text=int(value))

    def choose_folder():
        nonlocal save_path
        selected = filedialog.askdirectory(title="Wybierz folder zapisu wykresów")
        if selected:
            save_path = selected
            folder_label.configure(text=f"📁 {selected}")
        else:
            save_path = None
            folder_label.configure(text="❌ Nie wybrano folderu")

    customtkinter.set_appearance_mode("System")
    customtkinter.set_default_color_theme("blue")

    app = customtkinter.CTk()
    app.geometry("750x500")
    app.title("Scraper Otomoto")

    clicked = False
    save_path = None

    text = customtkinter.CTkLabel(app, text="Czy wyświetlić dodatkowe informacje?:")
    text.pack(pady=10)

    optionmenu = CTkOptionMenu(master=app, values=["Tak", "Nie"])
    optionmenu.set("Tak")
    optionmenu.pack(pady=10)

    slider = customtkinter.CTkSlider(master=app, from_=1, to=30, command=increase)
    slider.pack(pady=10)

    slider_label = customtkinter.CTkLabel(master=app, text="15", font=("Helvetica", 12))
    slider_label.pack(pady=10)

    # Przycisk wyboru folderu
    folder_button = customtkinter.CTkButton(app, text="Wybierz folder zapisu(wymagane)", command=choose_folder)
    folder_button.pack(pady=10)

    folder_label = customtkinter.CTkLabel(app, text="Nie wybrano folderu")
    folder_label.pack(pady=5)

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
        scrape_info = ScrapInfo(more_info, pages, save_path)
        print(scrape_info.more_info)
        print(scrape_info.number_of_pages)
        scrape_info.save_path = save_path  # dodajemy atrybut ścieżki zapisu
        app.destroy()
        return scrape_info
    else:
        print("błąd działania GUI aplikacji")
        exit()


def closing_app(excel_filse_name):
    def exit_all():
        quit()
    customtkinter.set_appearance_mode("System")
    customtkinter.set_default_color_theme("blue")

    app = customtkinter.CTk()
    app.geometry("800x200")
    app.title("Scraper Otomoto")

    text = customtkinter.CTkLabel(app, text=f"Zakonczono działanie aplikacji. \n We wskazanym folderze utworzono nowy plik excel: {excel_filse_name}")
    text.pack(pady=10)

    button = customtkinter.CTkButton(
        master=app,
        text="wyjdź",
        fg_color="purple",
        command=exit_all
    )
    button.pack(pady=10)

    app.mainloop()