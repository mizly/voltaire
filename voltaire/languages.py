from glob import glob
import locale,json
app_language = 'en_CA'
locale.setlocale(locale.LC_ALL, app_language)
languages = {}
language_list = glob("lang/*.json")
for lang in language_list:
    filename = lang.split('\\')
    lang_code = filename[1].split('.')[0]

    with open(lang, 'r', encoding='utf8') as file:
      languages[lang_code] = json.loads(file.read())