# Coursera
Скрипт собирает информацию о разных курсах на Курсере (20 случайных из [xml](https://www.coursera.org/sitemap~www~courses.xml) файла) и экспортирует её в excel-файл.

Для работы скрипта нужны библиотеки, которых нет в стандратной поставке python, они перечислены в файле `requirements.txt`. Для установки всех зависимостей введите:
```python
pip3 install -r requirements.txt
``` 

## Запуск
Для получения справки нужно запустить скрипт с флагом `-h` или `--help`
Для запуска вводим:
```python
python3 coursera.py filepath.xlsx
```
