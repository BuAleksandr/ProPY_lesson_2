from pprint import pprint
import csv
import re

if __name__ == '__main__':
    with open("phonebook_raw.csv", "r", encoding="utf-8") as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)

    contacts_list2 = []
    for contacts in contacts_list:
        contacts[:3] = [' '.join(contacts[:3])]
        contacts[0] = contacts[0].split(' ')
        del contacts[0][3:]
        contacts = contacts[0] + contacts[1:]
        contacts_list2.append(contacts)
    contacts_list = contacts_list2


    def number(pattern, subst, list):
        x = 0
        for i in list:
            y = 0
            for n in i:
                list[x][y] = re.sub(pattern, subst, n)
                y = y + 1
            x = x + 1


    number(r"(\+7|8)\s*?\(?(\d{3})\)?\-?\s?(\d{3})\-?(\d{2})\-?(\d{2})", r"+7(\2)\3-\4-\5", contacts_list)
    number(r"\(?доб.\s+(\d+)\)?", r"доб.\1", contacts_list)

    contact_document = []
    contacts_dict = {}
    new_contacts_list = []
    new_contacts_list = [contacts_list[0]]

    for i in contacts_list[0]:
        contacts_dict[i] = ''
    del contacts_list[0]

    contacts_dict_new = {}

    for contact in contacts_list:
        x = 0
        for name in contacts_dict:
            contacts_dict_new[name] = contact[x]
            x = x + 1
        contact_document.append(contacts_dict_new)
        contacts_dict_new = {}
    # print(contact_document)

    sorted_data = sorted(contact_document, key=lambda i: (i['firstname'], i['lastname']))


    def merge_dict(dict_1, dict_2):
        for k, v in dict_2.items():
            if dict_1.get(k):
                if dict_1[k] == v:
                    dict_1[k] = dict_1[k]
                elif dict_1[k] == '':
                    dict_1[k] = [v]
                elif v == '':
                    dict_1[k] = dict_1[k]
            else:
                dict_1[k] = v
        return dict_1


    new_contacts_dict = {}
    x = 0
    result = []
    for i in sorted_data:
        for res in new_contacts_dict.values():
            result.extend(res)
        if i['lastname'] and i['firstname'] not in result:
            new_contacts_dict[x] = [i['lastname'], i['firstname']]
            x = x + 1
            new_contacts_list.append(list(i.values()))
        else:
            for k, v in new_contacts_dict.items():
                if v == [i['lastname'], i['firstname']]:
                    examination = k
            merge = merge_dict(sorted_data[examination], i)
            new_contacts_list.append(list(merge.values()))
            fail = examination + 1
            del new_contacts_list[fail]
            new_contacts_dict[x] = [i['lastname'], i['firstname']]
            x = x + 1
    # pprint(new_contacts_list)

    with open("phonebook.csv", "w") as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(new_contacts_list)


