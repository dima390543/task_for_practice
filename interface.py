# Интерфейс приложения

from fns_scraper import *



scraper = FnsScraper()#создание скрапера, инициализация драйвера, базы данных

scraper.set_url(path_page_scraper)# переход на начальную страницу

scraper.set_page_ip()# Переход на вкладку ИП

scraper.set_selected_okved()# Устанавливает новый URL, в зависимости от выбранных оквэд

scraper.set_page_with_all_activities_ip()#все записи на одной странице

scraper.table_rows = scraper.get_all_activities_ip()#Получение всех записей

scraper.update_db(scraper.table_rows) # запись, обновление записей

scraper.driver.quit()




