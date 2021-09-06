from pprint import pprint
# читаем адресную книгу в формате CSV в список contacts_list
import csv
import re


def get_fio(row):
    counter = 0
    fio = ['' for j in range(3)]

    for i in range(0, 3):
        name = re.split(r'\s', row[i])
        if '' not in name:
            for letter in name:
                fio[counter] = letter
                counter += 1
    return fio


def transform_phone_number(ph_numb):
    phone_pattern = re.compile(r'(\+7|[8])[\s(]*(\d{3})[\s)-]*(\d{3})[\s-]*(\d{2})[\s-]*(\d{2})[\s(а-яёА-ЯЁ\.]*(\d*)')

    phone_group = phone_pattern.search(ph_numb)
    if phone_group is not None:
        result_number = f'+7({phone_group.group(2)}){phone_group.group(3)}-{phone_group.group(4)}-{phone_group.group(5)}'
        if phone_group.group(6):
            result_number += f' доб.{phone_group.group(6)}'
        return result_number
    else:
        return ''


def transform_row(contacts_list):
    proc_contacts_list = list()
    proc_contacts_list.append(contacts_list[0])

    for i in range(1, len(contacts_list)):
        cur_row = get_fio(contacts_list[i])

        cur_row.extend(contacts_list[i][3:5])

        cur_row.append(transform_phone_number(contacts_list[i][5]))

        cur_row.append(contacts_list[i][6])
        proc_contacts_list.append(cur_row)
    return proc_contacts_list

def remove_duplicates(contacts_list):
    temp_list = list()
    new_contacts_list = list()

    for i in range(len(contacts_list)):
        flag = False
        for j in range(len(contacts_list)):
            if contacts_list[i][0] == contacts_list[j][0] \
                    and contacts_list[i][1] == contacts_list[j][1] \
                    and contacts_list[i] != contacts_list[j]:
                flag = True
                temp = list()
                for elem in range(len(contacts_list[i])):
                    if contacts_list[i][elem]:
                        temp.append(contacts_list[i][elem])
                    else:
                        temp.append(contacts_list[j][elem])
                new_contacts_list.append(temp)
        if not flag:
            new_contacts_list.append(contacts_list[i])
    result_list = list()

    for i in new_contacts_list:
        if (i[0] + i[1]) not in temp_list:
            result_list.append(i)
            temp_list.append(i[0] + i[1])

    return result_list

if __name__ == '__main__':
    with open("phonebook_raw.csv") as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)


    contacts_list = transform_row(contacts_list)

    contacts_list = remove_duplicates(contacts_list)
    pprint(contacts_list)

    # код для записи файла в формате CSV
    with open("phonebook.csv", "w") as f:
      datawriter = csv.writer(f, delimiter=',')
    #   # Вместо contacts_list подставьте свой список
      datawriter.writerows(contacts_list)
