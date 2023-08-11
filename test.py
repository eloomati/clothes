from tkinter import *
from tkinter import ttk

# funkcja do wykonania w programie
def calculate(*args):
    try:
        value = float(feet.get())
        meters.set(int(0.3048 * value * 10000.0 + 0.5)/10000.0)
    except ValueError:
        pass

# inicjalizacja i nadanie tytulu aplikacji
root = Tk()
root.title("Feet to Meters")

# widzet ramki, zawiera zawartosc naszego interfejsu
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1) # mowi nam o tym, że ramka sie powinna rozszerzyc jak powiekszy sie okno
root.rowconfigure(0, weight=1)
# tworzenie okno do wproawdzania wartosci
feet = StringVar()
feet_entry = ttk.Entry(mainframe, width=7, textvariable=feet) # mainframe to rodzic do ktorego ma nalezec okno wpisu, width oznacza jak szeroki ma byc, a textvariable to podlaczenie naszego guzika do funkcji i umozliwienie jej aktywacji
feet_entry.grid(column=2, row=1, sticky=(W, E)) # okresla gdzie chcemy umiescic widzet wzgledem innych, sticky oznacza jak wyrownac w komurce siatki przy uzyciu kierunkow z kompasu (we oznacza zachod wschod czyli wyrownanie do lewej i prawej

# tworzenie kolejnego widzetu
meters = StringVar() # odpowiedzialny za metry
ttk.Label(mainframe, textvariable=meters).grid(column=2, row=2, sticky=(W, E))

# odpowiedzialny za przycisk i katywacje funkcji
ttk.Button(mainframe, text="Calculate", command=calculate).grid(column=3, row=3, sticky=W)
# etykiety ktore stersuja uzytkownika wyjasniajac co jak dziala w oknie
ttk.Label(mainframe, text="feet").grid(column=3, row=1, sticky=W)
ttk.Label(mainframe, text="is equivalent to").grid(column=1, row=2, sticky=E)
ttk.Label(mainframe, text="meters").grid(column=3, row=2, sticky=W)

button = ttk.Button(root, text="Hello", command="buttonpressed")
button.grid()
button.configure()
# ulatwienie ktore pozwala nam dodac ramki do wszytskich widzetow, zamiast dopiosywac do kazdej pojedynczo
for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)
# po wlaczeniu programu ten widzet sprawiwa, ze uzytkownik nie musi klikac w okno zeby moc zaczac pisac
feet_entry.focus()
root.bind("<Return>", calculate) # mowi ze jesli wcisniemy enter to zadziala to tak samo jak guzik 'Oblicz'
# odpala petle zdarzen ktora jest potrzebna do interakcji z uzytkownikime i otwarciem okna
root.mainloop()



url = 'https://secondmax.pl/83-koszulki?page=2'
page = PageGetter(url)
content = page.get_page(2)
soup = BeautifulSoup(content, 'html.parser')
imgs = soup.find_all('img', {'loading': 'lazy'})
print(imgs)

url = 'https://secondmax.pl/83-koszulki?page=2'
page = PageGetter(url)
content = page.get_page(2)
soup = BeautifulSoup(content, 'html.parser')
pictures = soup.find_all('img', {'loading': 'lazzy'})
print(pictures)