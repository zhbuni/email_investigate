import openpyxl
from pathlib import Path
from pprint import pprint


def get_parsed_table():
    dict_of_themes = {}
    list_of_themes = []
    xlsx_file = Path('mail.xlsx')
    wb_obj = openpyxl.load_workbook(xlsx_file)

    sheet = wb_obj.active
    sheet_ranges = wb_obj['Лист1']['B:G']
    episode_number = 1
    for i in range(len(sheet_ranges[0])):
        dct = {}
        episode = sheet_ranges[0][i].value
        if str(episode).split()[0].strip().lower() == 'эпизод':
            episode_number = int(episode.split()[1])

        theme = sheet_ranges[1][i].value
        keyword = sheet_ranges[2][i].value
        if keyword and isinstance(keyword, str) and keyword[0] == '=':
            keyword = wb_obj['Лист1'][str(keyword[1:])].value
        tip_1 = sheet_ranges[3][i].value
        tip_2 = sheet_ranges[4][i].value
        tip_3 = sheet_ranges[5][i].value
        if all((theme, keyword)):
            dct['episode_number'] = str(episode_number).strip()
            dct['theme'] = str(theme).strip()
            dct['episode'] = str(episode).strip()
            dct['keyword'] = str(keyword).strip()
            dct['tip_1'] = str(tip_1).strip()
            dct['tip_2'] = str(tip_2).strip()
            dct['tip_3'] = str(tip_3).strip()
            list_of_themes.append(dct)
            # dict_of_themes[episode] = {}
            # dict_of_themes[episode]['theme'] = theme
            # dict_of_themes[episode]['keyword'] = keyword
            # dict_of_themes[episode]['tip_1'] = tip_1
            # dict_of_themes[episode]['tip_2'] = tip_2
            # dict_of_themes[episode]['tip_3'] = tip_3
            # print(theme, keyword, answer_1, answer_2, answer_3, sep='\t')
    return list_of_themes