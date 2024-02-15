from utils import read_tel_dir, search_record, edit_record, add_record, menu


actions = {'1': read_tel_dir, '2': search_record, '3': edit_record, '4': add_record}

print(menu)
while True:
    try:
        action = input('Выберите действие: ')
        if action == '0':
            break
        actions[action]()

    except KeyError:
        print('Такого варинта нет среди предложенных. Пожалуйста выберите действие из списка.')