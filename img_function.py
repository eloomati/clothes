import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import os
import re



def take_every_other(imgs):
  return imgs[::2]

# Funkcja pobierająca zdjęcia
def get_img(url, path, name_of_folder):
    try:
        response = requests.get(url) # zapytanie do istnienia url
        content = response.content # przygotowanie content dla BytesIO
        img = Image.open(BytesIO(content)) # otwarcie zdjecia
        img_name = url.split('/')[-1].split('.')[0] + '.jpg' # nadanie zdjeciu odpowiedniej nazwy
        os.makedirs(f'{path}/{name_of_folder}', exist_ok=True) # stworzenie folderu do zapisu, jeśli nie istnieje
        img.save(f'{path}/{name_of_folder}/{img_name}') # zapisanie zdjęcia
    except:
        print('Fail') # wyrzucenie błędu, bez przerywania działania programu


# Funkcja konwertująca zdjęcia w formacie PNG na JPG
def convert_png_to_jpg(enter, output):
    image = Image.open(enter) # otwarcie zdjęcia przez program
    image_rgb = image.convert("RGB") # konwercja zdjęcia PNG na JPG
    return image_rgb.save(output, "JPEG") # zwrócenie zdjęcia w formacie JPG


# Funkcja sprawdzajaca czy na koncu url jest cyfra
def check_last_value(link):
    # podzielenie stringa i wybranie ostatniej czesci url
    last_value = link.split('/')[-1]
    # sprawdzenie czy ostatnia wartosc z wyciagnietego stringa to cyfra
    if last_value and last_value[-1].isdigit():
        # konwertowanie ostatniej wartosci na typ liczbpwy
        return int(last_value[-1])
    else:
        return ''


# Class to check if url is correct and don't have basic jpg
class StringChecker:
    def __init__(self):
        self.list_of_regex_to_delete = [] # inicjalizacja pustej listy z regex tych url, ktorych chcemy sie pozbyc z listy
        self.list_of_regex_to_save = [] # inicjalizacja pustej listy z regex tych url, które chcemy sprecyzować,
                                        # żeby wybrać odpowiednią zawartość

    # Funkcja dodająca regex do listy usuwającej
    def add_regex_to_delete(self, regex):
        self.list_of_regex_to_delete.append(re.compile(regex.strip()))

    # Funkcja dodająca regex do listy specjalizującej odpowiednią zawartość linka
    def add_regex_to_save(self, regex):
        self.list_of_regex_to_save.append(re.compile(regex.strip()))

    # Funkcja sprawdzająca treść url i zwracająca wartość True/False w odpowiedniej sytuacji
    def check_string(self, string):
        # petla sprawdzczajaca czy regex z listy jest w url
        if any(re.search(regex, string) for regex in self.list_of_regex_to_delete):
            return False # wartosc False usuwa nam te url które są zgodnę z regex z listy
        # petla sprawdzczajaca czy regex z listy jest w url
        elif any(re.search(regex, string) for regex in self.list_of_regex_to_save):
            return True # wartość True zwraca nam te url, które są zgodnę z regex z listy
        else:
            return True


# Klasa pobierajaca url i dzielaca go na czesci, przy okazji tworzaca kontent dla funkcji URLParser
class PageGetter:

    # wczytanie url
    def __init__(self, url):
        self.url = url

    # funkcja sprawdzajaca ostatnia wartosc url, jesli to int to wstawia counter
    def get_page(self, counter):
        if self.url[-1][-1].isdigit():
            counter = str(counter)
            done_url = re.sub(r'\d+$', counter, self.url)
        else:
            done_url = self.url

        # sprawdzenie istnienia strony oraz zwrocenie contentu dla funkcji URLParser
        try:
            response = requests.get(done_url)
            return response.content
        except:
            print('Web doesnt exist!')


# Klasa która analizuje nam skladnie naszego url
class URLParser:
    def __init__(self, string_checker):
        self.string_checker = string_checker # podlaczenie funkcji do funkcji sprawdzającej poprawność URL

    # Funkcja sprawdzająca składnie URL, która przy odpowiednich parametrach przeszukuje plik zródłowy strony i jeśli
    # jest spełniony odpowiedni warunek to zwraca liste URLi zawierających odniesienie do zdjęć
    def parse_url(self, content, mark, classification, name_of_classification, source):
        try:
            soup = BeautifulSoup(content, 'html.parser')
        except:
            soup = BeautifulSoup(content, 'html.parser', from_encoding='ISO-8859-1')

        pictures = soup.find_all(mark, {classification: name_of_classification})

        try:
            return [img[source] for img in pictures if self.string_checker.check_string(img[source])]
        except:
            imgs = take_every_other(pictures)
            return [img[source] for img in imgs if self.string_checker.check_string(img[source])]


# Klasa odpowiedzialna za obsługę działania pobierania zdjęć
class DataCollector:
    def __init__(self, link, start_page, end_page, mark, classification,
                 name_of_classification, source, path, name_of_folder, url_parser, page_getter):
        self.link = link # adres url
        self.start_page = start_page # cyfra oznaczająca pierwszą stronę z której chcemy pobierać
        self.end_page = end_page # cyfra oznaczająca ostatnią stronę z której chcemy pobierać
        self.mark = mark # znacznik według którego chcemy przeszukiwać div na stronie
        self.classification = classification # znacznik oznaczający klasę w której zapisane są zdjęcia
        self.name_of_classification = name_of_classification # nazwa klasy w której zapisywane są zdjęcia
        self.source = source # nazwa zniacznika, który chcemy wyciągnąć url
        self.path = path # sciezka do miejsca w którym chcemy zapisywać zdjęcia
        self.name_of_folder = name_of_folder # nazwa folderu który chcemy stworzyć do zapisywania zdjęć
        self.url_parser = url_parser # instancja klasy URLParser
        self.page_getter = page_getter # intacja klasy PageGetter

    # funkcja obsługująca bezpośrednie pobieranie
    def get_data(self):
        # petla sprawdzająca wartość counter
        if self.start_page != '':
            start_page = int(self.start_page)
            end_page = int(self.end_page)
            # petla tworząca tworząca ilość linków rownych podanemu zakresowi counter przez uzytkownika
            for counter in range(start_page, end_page + 1):
                content = self.page_getter.get_page(counter) # zapisanie contentu z kazdej stworzonej strony
                # utworzenie listy url zawieracych link do zdjecia
                urls = self.url_parser.parse_url(content, self.mark, self.classification, self.name_of_classification,
                                                 self.source)
                # petla ktora pobiera z kazdego url zdjecie i zapisuje je w odpowiednim folderze
                for i, url in enumerate(urls):
                    get_img(url, self.path, self.name_of_folder) # aktywacja funkcji pobierającej
                    if i % 20 == 0: # petla informująca użytkownika o stanie działania programu
                        print(f'Downloaded {i} for page {counter} from {self.link}')
        else:
            content = self.page_getter.get_page('') # zapisanie content z jednego url
            urls = self.url_parser.parse_url(content, self.mark, self.classification, self.name_of_classification,
                                             self.source) # utworzenie listy url zawierajacych link do zdjec
            # petla ktora pobiera z kazdego url zdjecie i zapisuje je w odpowiednim folderze
            for i, url in enumerate(urls):
                get_img(url, self.path, self.name_of_folder) # zapisanie content z jednego url
                if i % 20 == 0: # petla informujaca uzytkownika o stanie dzialania programu
                    print(f'Downloaded {i} from {self.link}')


# funkcja dzielaca wczytany url na czesci za pomoca separatora / oraz ?
def link_to_part(url, counter):
    url_to_part = re.split(r'[/?]', url) # podzielenie funkcji przez separatory
    i = 0 #inicjalizacja licznika
    done_url = 'https://' # inicjalizacja poczatku url

    # petla sprawdzajaca wartosc ostatniego znaku z url oraz wystapienia symboli 'page' w url
    if url[-1][-1].isdigit() and (re.search(r'\?p', url) or re.search(r'page', url)):
        while i < len(url_to_part) - 1: # petla skladajaca url, bez ostatniej czesci
            done_url += f'{url_to_part[i]}/'
            i += 1
        counter = str(counter)
        done_url += f'?{url_to_part[-1].replace(url_to_part[-1][-1], counter)}' # zamiana ostatniej wartosci na
                                                                                    # wartosc countera
    else:
        while i < len(url_to_part) - 1: # petla skladajaca url, bez ostatniej czesci
            done_url = done_url + f'{url_to_part[i]}/'
            i += 1
        done_url += f'{url_to_part[-1]}' # doklejenie konca url bez znaku /