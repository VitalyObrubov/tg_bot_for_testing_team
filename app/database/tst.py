import gspread  # импортируем библиотеку

gs = gspread.service_account(filename='gsheetscred.json')  # подключаем файл с ключами и пр.
sh = gs.open_by_key('1vybR8raLw_oXvfMb8o8c5cYbPQrmmVQ9QjhaNUJcALQ')  # подключаем таблицу по ID
worksheet = sh.sheet1  # получаем первый лист

# res = worksheet.get_all_records()  # считываем все записи (массив: ключ-значение)
# res = worksheet.get_all_values()  # считываем все значения
# res = worksheet.row_values(1)  # получаем первую строчку таблицы
# res = worksheet.col_values(1)  # получаем первую колонку таблицы
# res = worksheet.get('A2')  # получаем заданную ячейку
# res = worksheet.get('A2:C2')  # получаем заданный диапазон
# print(res)  # выводим в консоль

# newRec = ["Антонов", "Самолет", 2500]
# worksheet.insert_row(newRec, 2)  # добавляем новые данные в строку 2

formula = worksheet.acell('A2', value_render_option='FORMULA').value

worksheet.append_row(["Онищенко", '=HYPERLINK("seyepapeseny@gmail.com";"email")', 220, "+5343466636"],value_input_option = "USER_ENTERED")  # добавить новую строку с данными
#worksheet.update_cell(6, 3, '=HYPERLINK("seyepapeseny@gmail.com";"email")')  # обновить ячейку
#worksheet.delete_rows(3)  # удалить строку номер 3
#worksheet.update_acell('A14','=HYPERLINK("seyepapeseny@gmail.com";"email")')
