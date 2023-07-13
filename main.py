import functions
import img_function as i

path = r'D:\vision'
url = 'https://remixshop.com/pl/womens-clothes/t-shirts?page=9' # podajemy link z https://
start_page = '1'
end_page = '95'
mark = 'img'
classfication = 'class'
name_of_classification = 'img-fluid'
source = 'src'
name_of_folder = 'koszulki'


if __name__ == '__main__':
   # Tworzenie obiektu StringChecker
    string_checker = i.StringChecker()

   # Dodawanie wyrażeń regularnych do usunięcia
    string_checker.add_regex_to_delete('field_manufacture\.jpg')
    string_checker.add_regex_to_delete('\_menu\_')
    string_checker.add_regex_to_delete('/cookies.svg')
    string_checker.add_regex_to_delete('/banners/')
    string_checker.add_regex_to_delete('/themes/SECONDMAX_PL/assets/img/noimg.png')

   # Dodawanie wyrażeń regularnych do zachowania
    string_checker.add_regex_to_save('environment')
    string_checker.add_regex_to_save('media\.remix')


   # Tworzenie obiektu PageGetter
    page_getter = i.PageGetter(url)

   # Tworzenie obiektu URLParser z wykorzystaniem StringChecker
    url_parser = i.URLParser(string_checker)

    # Tworzenie obiektu DataCollector i wywołanie get_data()
    data_collector = i.DataCollector(link=url, start_page=start_page, end_page=end_page, mark=mark,
                                  classification=classfication, name_of_classification=name_of_classification,
                                  source=source, path=path, name_of_folder=name_of_folder,
                                  url_parser=url_parser, page_getter=page_getter)

    data_collector.get_data()

