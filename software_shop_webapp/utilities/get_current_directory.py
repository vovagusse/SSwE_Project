import os
import sys
import pathlib


def get_current_directory(custom_filepath: str = None):
    """Данная функция возвращает директорию/путь, в 
    котором лежит скрипт .py, который вызывает данную функцию. 
    Эта функция более точно ищет то место, где находится 
    скрипт и не обращает внимания на то, в какой директории 
    находится пользователь в терминале (а именно эта директория 
    берётся за основу как "относительный путь" по 
    умолчанию, что не всегда хорошо).

    :param custom_filepath: путь до файла (если нужно узнать путь до директории конкретного скрипта), по умолчанию - None
    :type custom_filepath: str, optional
    :return: путь до файла, откуда была вызвана данная функция
    :rtype: str
    """
    
    p = os.path.dirname(sys.argv[0])
    if custom_filepath:
        print(f"Path: {custom_filepath}")
        p = str(pathlib.Path(custom_filepath).parent.resolve())
    a = lambda x: x if (x!="" or x) else "<empty>"
    print(f"[p]: {a(p)}")
    plat = sys.platform
    if ("win" in plat):
        p = p[0].upper() + p[1:]
        p = p.replace("/", "\\")
    return p