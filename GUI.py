from fileinput import filename

import customtkinter
from customtkinter import CTkOptionMenu, filedialog
from scrapinfo import ScrapInfo

def selectfile():
    filename = filedialog.askopenfilename()
    print(filename)




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

    button_to_select = customtkinter.CTkButton(
        master=app,
        text="Wybierz plik w którym umieścić utworzone pliki",
        command=selectfile
    )
    button_to_select.pack(pady=10)

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
        scrape_info = ScrapInfo(more_info, pages, filename)
        print(scrape_info.more_info)
        print(scrape_info.number_of_pages)



        return scrape_info
    else:
        print("błąd działania GUI aplikacji")
        exit()

