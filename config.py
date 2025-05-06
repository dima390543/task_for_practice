# Модуль конфигурации
#никакой логики

# Selemiun
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Стандартные библиотеки
import sqlite3
import time
import re
import os

# Начальная страница
path_page_scraper = 'https://pb.nalog.ru/'

# Наименование базы
db_file = 'test_ip.sqlite3'
db_name_table = 'InformationIp'

# Наименование файла чтения
file_json = 'input.json'


