#модуль получения данных
import json
from config import *
from selenium import webdriver
from storage import DB


class FnsScraper:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(15)
        self.file_inp = file_json
        self.db = DB()

    def get_okved(self):
        '''Возвращает список номеров оквэд'''
        with open('input.json') as file_input:
            data = json.load(file_input)
        return data

    def set_selected_okved(self):
        '''Устанавливает новый URL, в зависимости от выбранных оквэд'''
        okvedip = self.get_okved()
        # Переход по новому URL по всем ОКВЭД из кортежа
        self.set_url(f'{self.driver.current_url}&okvedIp={"%2C".join(okvedip)}')

        self.wait_load_page(60)  # ожидание загрузки

        """ лишнее действие, вроде как)
        search = get_button_search(driver)  # Получение кнопки поиска
        search.click()
        """

    def get_button_ip(self):
        '''Возвращает кнопку ИП'''
        return self.driver.find_element(By.XPATH, '//label[contains(text(), "Индивидуальный предприниматель (ИП)")]')

    def get_button_search(self):
        '''Возвращает кнопку поиска'''
        return self.driver.find_element(By.XPATH, '//button[contains(@class, "btn btn-warning")]')

    def set_page_ip(self):
        '''Переход на вкладку ИП и обновление страницы'''
        label_element = self.get_button_ip()  # Получение кнопки ИП

        label_element.click()

        search = self.get_button_search()  # Получение кнопки поиска

        search.click()

    def get_count_activities_ip(self):
        '''Возвращает количество подходящих записей'''
        result_data = self.driver.find_element(By.ID, 'resultip')  # resultip
        count = int(result_data.find_element(By.CLASS_NAME, 'group-counter').text.strip('()'))
        return count

    def set_page_with_all_activities_ip(self):
        '''Переход на не сущесвующую страницу, где выводятся все записи на одной странице'''
        count_ip = self.get_count_activities_ip()
        print(f"Всего записей {count_ip}")  # количество записей нужно для сверки

        size = 10  # переход на не сущесвующую страницу, тогда выводятся все записи на одной странице
        count_page = str(count_ip // size + 2)
        self.set_url(re.sub('page=\d+', f'page={count_page}', self.driver.current_url))

        self.wait_load_page(100)  # ожидание загрузки

    def get_all_activities_ip(self):
        '''Получение всех активностей ИП-шников'''
        result_data = self.driver.find_element(By.ID, 'resultip')
        table_rows = result_data.find_elements(By.CLASS_NAME, 'pb-card')  # все записи ИП по выбранным ОКВЭД

        self.wait_load_page(100)  # ожидание загрузки
        return table_rows

    def set_url(self, path):
        '''Устанавливает новый URL'''
        self.driver.get(path)  # переход на новую страницу

    def get_db(self):
        '''Возвращает экземпляр DB'''
        db = DB()
        return db

    def update_db(self, table_rows):
        '''Заполняет базу новыми данными, если такие уже существуют обновляет'''
        c = 0
        for row in table_rows:
            c += 1
            data = row.text.split('\n')
            self.db.insert(data)
        print(f"Загружено {c}")

    def wait_load_page(self, times):
        '''Ожидание исчезновения загрузки'''
        time.sleep(3)
        WebDriverWait(self.driver, times).until(
            EC.invisibility_of_element_located((By.ID, 'txtBlockUI')))



class CaptchaException(Exception):
    def __init__(self, message=None):
        self.default_message = 'Капча! В другой раз получится'
        super().__init__(self.default_message)
