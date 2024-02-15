import os
import pandas
from math import ceil

menu: str = """Введите <1> если хотите просмотреть телефонный справочник
Введите <2> если хотите найти запись
Введите <3> если хотите редактировать запись
Введите <4> чтобы добавить новую запись
Для выхода введите <0>"""

def read_tel_dir() -> None:
    """
    Постранично выводит записи из телефонного справочника до тех пор пока пользователь не введет "0" чтобы выйти из функции, на одной странице максимум 5 записей
    """
    os.system('cls||clear')
    df = pandas.read_json('telephone_directory.json', encoding='utf-8')
    page_size = 5
    page_count = ceil(len(df) / page_size)
    while True:
        page_number = abs(int(input(
            f'Введите номер страницы для просмотра, доступно {page_count} страниц(ы) или введите 0 для выхода в главное меню: ')))
        if page_number == 0:
            break
        elif page_number > page_count:
            os.system('cls||clear')
            print("Данной страницы нет в справочнике, пожалуйста выберите допустимую страницу.")
            continue

        start_index = (page_number - 1) * page_size
        if len(df) - start_index < 5:
            os.system('cls||clear')
            page = df.iloc[start_index:]
            print(page)
        else:
            os.system('cls||clear')
            end_index = start_index + page_size
            page = df.iloc[start_index:end_index]
            print(page)
    os.system('cls||clear')
    print(menu)


def search(df: pandas.DataFrame):
    """
    Производит поиск записи спрашивая пользователя по какому параметру он хочет искать запись или дает возможность прекратить поиск если пользователь ввел "0"
    :param df: Двумерная структура данных в виде таблицы записей из справочника
    :return: фильтрованные данные если пользователь ввел парметр и пример строки по которой искать или None если ничего не найдено, так же возвращает "0" если пользователь захотел прекратить поиск
    """
    search_by = input(
        'Выберите параметр по которому хотите найти запись:\n'
        '<1>Фамилия\n'
        '<2>Имя\n'
        '<3>Отчество\n'
        '<4>Название организации\n'
        '<5>Рабочий номер телефона\n'
        '<6>Личный номер телефона или введите <0> для выхода: ')
    os.system('cls||clear')
    columns = {'1': 'last_name', '2': 'first_name', '3': 'middle_name', '4': 'org', '5': 'work_num',
               '6': 'person_num'}
    if search_by == '0':
        return search_by
    elif search_by not in columns.keys() or search_by == '':
        return 'Данного парамтра нет среди предложенных. Пожалуйста выберите параметр из списка.'
    search_term = input('Введите данные для поиска: ')

    filtered_data = df[df[columns[search_by]].str.lower().str.startswith(search_term.lower())]
    return None if filtered_data.empty else filtered_data


def search_record() -> None:
    """
    Производит поиск записи используя метод описанный выше
    """
    os.system('cls||clear')
    df = pandas.read_json('telephone_directory.json', encoding='utf-8')
    while True:
        filtered_data = search(df)
        if filtered_data is None:
            print('Ничего не найдено, попробуйте ввсети другие данные.')
            continue
        elif type(filtered_data) == str and filtered_data == '0':
            break
        print(filtered_data)

    os.system('cls||clear')
    print(menu)


def input_data() -> dict:
    """
    Получает данные для создания новой записи
    :return: возвращает dict с введенными данными от пользователя
    """
    new_record = {}
    while True:
        try:
            new_record['last_name'], new_record['first_name'], new_record['middle_name'] = input('Введите ФИО: ').split(
                " ")
            new_record['org'] = input('Введите название организации: ')
            new_record['work_num'] = input('Введите рабочий номер телефона: ')
            new_record['person_num'] = input('Введите личный номер телефона: ')

            check_data = input(f'Пожалуста проверьте еще раз введенные данные: ' + ' '.join(list(
                new_record.values())) + ', если все так введите <1>, иначе введите <0> для повторного ввода данны: ')
            if check_data == '1':
                return new_record
            elif check_data == '0':
                new_record = {}
                continue
            print("Введенного вами варианта нет в списке, пожалуйста введите данные снова.")


        except ValueError:
            os.system('cls||clear')
            print('Неверно введенный формат ФИО(необходимый формат: Иванов Иван Иванович). Попробуйте снова.')


def add_record() -> None:
    """
    Добавляет новую запись, полученную от метода input_data описанного выше и сохраняет новую запись в файл telephone_directory.json
    """
    os.system('cls||clear')
    new_record = input_data()

    df = pandas.read_json('telephone_directory.json', encoding='utf-8')
    new_df = pandas.DataFrame([new_record])
    df = pandas.concat([df, new_df])
    df.to_json('telephone_directory.json', orient='records', force_ascii=False)

    os.system('cls||clear')
    print('Запись успешно добавлена. Выберите следующее действие.')
    print(menu)


def edit_record() -> None:
    """
    Редактирует запись в файле  telephone_directory.json, давая возможность найти конкретную запись или выбрать запись просмотрев весь файл.
    """
    os.system('cls||clear')
    while True:
        action = input("Введите <1> если хотите найти конкретную запись для редактирования\n"
                       "Bведите <2> если хотите просмотреть весь список записей"
                       "Bведите <0> для выхода: ")

        if action == '0':
            os.system('cls||clear')
            print(menu)
            return

        df = pandas.read_json('telephone_directory.json', encoding='utf-8')

        if action == '1':
            while True:
                os.system('cls||clear')
                filtered_data = search(df)
                if filtered_data is None:
                    print('Ничего не найдено, попробуйте ввсети другие данные.')
                    continue
                elif type(filtered_data) == str and filtered_data == '0':
                    os.system('cls||clear')
                    print(menu)
                    return
                print(filtered_data)

                if len(filtered_data) > 1:
                    index = input(
                        'Пожалуйста введите инекс(первая колонка слева) записи которую хотите редактировать или введите <q> для выхода: ')
                    if index == 'q':
                        os.system('cls||clear')
                        print(menu)
                        return
                    elif int(index) not in set(filtered_data.index):
                        print('Данного индекса нет среди предоставленных вам записей.')
                        continue
                    print('Введите пожалуйста новые данные для этой записи.')
                    new_record = input_data()
                    df.loc[int(index)] = new_record
                    df.to_json('telephone_directory.json', orient='records', force_ascii=False)
                    os.system('cls||clear')
                    print('Запись была успешно редактирована.')
                    print(menu)
                    return

                if input('Нажмите <Enter> если хотите продолжить редактирование или введите <q> для выхода: ') == 'q':
                    os.system('cls||clear')
                    print(menu)
                    return

                print('Введите пожалуйста новые данные для этой записи.')
                new_record = input_data()
                df.loc[int(filtered_data.index[0])] = new_record
                df.to_json('telephone_directory.json', orient='records', force_ascii=False)
                os.system('cls||clear')
                print('Запись была успешно редактирована.')
                print(menu)
                return

        if action == '2':
            print(df)
            index = input(
                'Пожалуйста введите инекс(первая колонка слева) записи которую хотите редактировать или введите <q> для выхода: ')
            if index == 'q':
                os.system('cls||clear')
                print(menu)
                return
            elif int(index) not in set(df.index):
                print('Данного индекса нет среди предоставленных вам записей.')
                continue
            print('Введите пожалуйста новые данные для этой записи.')
            new_record = input_data()
            df.loc[int(index)] = new_record
            df.to_json('telephone_directory.json', orient='records', force_ascii=False)
            os.system('cls||clear')
            print('Запись была успешно редактирована.')
            print(menu)
            return

        os.system('cls||clear')
        print('Введенного вами варианта нет в списке, пожалуйста выберите вариант из списка:')