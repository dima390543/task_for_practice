from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import sqlite3
import os

file_db = 'list_ip.sqlite3'
if os.path.exists(file_db):
    os.remove(file_db)

#виды деятельностей ИП.
t = (
    ("03", "08.92.2", "11.01", "31.01"), # >31000 записей
    ("08", "09"), # >3500 записей
    ("05.10.11", "14.20.2", "20.59.1"), # >120 записей
    ("03.2", ), # 7123 записей
    ("03", )# 15000 записей
)
i = 1 # выбор входных данных

current_okvedip = t[i] #кортеж номеров ОКВЭД


driver = webdriver.Chrome() #установлен на рабочий стол и прописан путь до него в path
driver.implicitly_wait(15) #неявное ожидание

driver.get('https://pb.nalog.ru/')


#Поиск кнопки Индивидуальный предприниматель (ИП)
label_element = driver.find_element(By.XPATH, '//label[contains(text(), "Индивидуальный предприниматель (ИП)")]')

#нажатие
label_element.click()


"""Можно было путем интерактивного меню найти кнопку - Вид деятеальности, 
потом найти поле поиска, вбить в поиск ОКВЭД send_keys(okved), 
send_keys(Keys.ENTER) можно выбрать конкретный ОКВЭД
Практически все записи так можно выбрать, но не все. Он не отображает
некоторые.
"""



search = driver.find_element(By.XPATH, '//button[contains(@class, "btn btn-warning")]')#кнопка поиска
search.click()#нажать на эту кнопку нужно для того, чтобы изменился URL




# Переход по новому URL по всем ОКВЭД из кортежа
driver.get(f'{driver.current_url}&okvedIp={"%2C".join(current_okvedip)}')


time.sleep(3)
WebDriverWait(driver, 60).until(EC.invisibility_of_element_located((By.ID, 'txtBlockUI')))#явное ожидание загрузки



search = driver.find_element(By.XPATH, '//button[contains(@class, "btn btn-warning")]')#кнопка поиска
search.click()#нажать на эту кнопку нужно для того, чтобы изменился URL






result_data = driver.find_element(By.ID, 'resultip') #resultip
count = int(result_data.find_element(By.CLASS_NAME, 'group-counter').text.strip('()'))
print(f"Всего записей {count}")#количество записей нужно для сверки





size = 10# переход на не сущесвующую страницу, тогда выводятся все записи на одной странице
count_page = str(count // size + 2)
driver.get(re.sub('page=\d+', f'page={count_page}', driver.current_url))



time.sleep(3)
WebDriverWait(driver, 100).until(EC.invisibility_of_element_located((By.ID, 'txtBlockUI')))#явное ожидание загрузки



table_rows = result_data.find_elements(By.CLASS_NAME, 'pb-card')# все записи ИП по выбранным ОКВЭД


#контекстный менеджер
with sqlite3.connect(file_db) as conn:
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS InformationIp (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT,
        status TEXT,
        edo_status TEXT,
        inn TEXT,
        ogrnip TEXT,
        ogrnip_date TEXT,
        code_okvd TEXT,
        activity TEXT
    )
    ''')

    c = 0
    for row in table_rows:
        c += 1
        data = row.text.split('\n')
        if len(data) == 11:
            cursor.execute('''
           INSERT INTO InformationIp (full_name, status, edo_status, inn, ogrnip, ogrnip_date, code_okvd, activity)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)
           ''', (data[0], data[1], data[2], data[4], data[6], data[8], data[9], data[10]))
        elif len(data) < 11:
            cursor.execute('''
            INSERT INTO InformationIp (full_name, edo_status, inn, ogrnip, ogrnip_date, code_okvd, activity)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (data[0], data[1], data[3], data[5], data[7], data[8], data[9]))
        else:
            print(data)

    print(f"Загружено {c}")
    conn.commit()

driver.quit()
