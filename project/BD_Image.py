import os
import sqlite3
import hashlib
import sys
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED
from tqdm import tqdm
import shutil
import pandas as pd
import numpy as np
import argparse
from termcolor import colored


DELETE = colored('DELETE', "red")
CHANGE = colored('CHANGE', "yellow")
NEW = colored('NEW', "green")

import re


def get_list_path_files(folder_path: str) -> list[str]:
    """Получить список файлов"""
    list_path_files = []
    for root, dirs, files in os.walk(folder_path):
        for name in files:
            list_path_files.append(os.path.join(root, name)[len(folder_path) + 1:])
    return list_path_files


def get_hash_file(path_file: str) -> str:
    """Получить хэш файла"""
    return hashlib.md5(open(path_file, 'rb').read()).hexdigest()


def get_info_files(folder_path, list_path_files):
    """Получить информацию о файлах"""

    def get_info_file(path_file):
        return (path_file, get_hash_file(os.path.join(folder_path, path_file)), "PENDING")

    with ThreadPoolExecutor(max_workers=16) as executor:
        results = list(tqdm(executor.map(get_info_file, list_path_files, timeout=60)))
    return results


def add_db(name_table: str, conn, info: tuple) -> None:
    # добавление инфы по файлу в бд
    sql = f''' INSERT INTO  "{name_table}" (name_file, hex_value,file_tag)
                                      VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, info)
    conn.commit()


def copy_files(original_folder_path: str, clone_folder_path: str, table_name: str, conn) -> None:
    """Скопировать файлы из одной директории в другую"""
    cur = conn.cursor()
    cur.execute(f"""SELECT name_file FROM '{table_name}' WHERE file_tag = 'PENDING'""")
    list_name = [name[0] for name in cur.fetchall()]

    def copy_file(path_file: str):
        list_path_file = path_file.split("\\")  # разделить путь на папки

        if len(list_path_file) > 1:
            path_save = clone_folder_path
            for dir in list_path_file[:-1]:
                path_save = os.path.join(path_save, dir)
                if not os.path.exists(path_save): os.makedirs(path_save)

        # копирование файла
        try:
            shutil.copy(os.path.join(original_folder_path, path_file), os.path.join(clone_folder_path, path_file))
        except:
            print('Невозможно скопировать файл ' + path_file)

    with ThreadPoolExecutor(max_workers=1) as executor:
        executor.map(copy_file, list_name, timeout=100)

    print("Копирование файлов завершено!")
    print("Обновление информации в БД...")
    cur.execute(f"""UPDATE '{table_name}' SET file_tag = 'ADD' WHERE file_tag = 'PENDING'""")
    conn.commit()

def delete_file(path_file: str, clone_folder_path: str):
    list_path_file = path_file.split("\\")[::-1]  # разделить путь на папки
    path_file_folder = os.path.join(clone_folder_path, path_file)
    # удалить файл
    os.remove(path_file_folder)
    for i in list_path_file:
        path_file_folder = path_file_folder.replace(i, "")
        try:
            os.rmdir(path_file_folder)
        except:
            pass

def delete_files(clone_folder_path: str, table_name: str, conn) -> None:
    """Удалить файлы из синхронизированной папки"""
    cur = conn.cursor()
    cur.execute(f"""SELECT name_file FROM '{table_name}' WHERE file_tag = '{DELETE}'""")
    list_name = [name[0] for name in cur.fetchall()]

    def delete_file(path_file: str):
        list_path_file = path_file.split("\\")[::-1]  # разделить путь на папки
        path_file_folder = os.path.join(clone_folder_path, path_file)
        # удалить файл
        os.remove(path_file_folder)
        for i in list_path_file:
            path_file_folder = path_file_folder.replace(i, "")
            try:
                os.rmdir(path_file_folder)
            except:
                pass


    with ThreadPoolExecutor(max_workers=16) as executor:
        executor.map(delete_file, list_name, timeout=100)

    print("Удаление файлов завершено!")
    print("Обновление информации в БД..")
    cur.execute(f"""DELETE  from '{table_name}' WHERE file_tag = '{DELETE}'""")
    conn.commit()


def update_files(original_folder_path: str, clone_folder_path: str, table_name: str, conn) -> None:
    """Скопировать файлы из одной директории в другую"""
    cur = conn.cursor()
    cur.execute(f"""SELECT name_file FROM '{table_name}' WHERE file_tag = '{CHANGE}'""")
    list_name = [name[0] for name in cur.fetchall()]

    def copy_file(path_file: str):
        list_path_file = path_file.split("\\")  # разделить путь на папки
        os.remove(os.path.join(clone_folder_path, path_file))  # удаление старого файла

        if len(list_path_file) > 1:
            path_save = clone_folder_path
            for dir in list_path_file[:-1]:
                path_save = os.path.join(path_save, dir)
                if not os.path.exists(path_save): os.makedirs(path_save)

        # копирование файла
        try:
            shutil.copy(os.path.join(original_folder_path, path_file), os.path.join(clone_folder_path, path_file))
        except:
            print('Невозможно скопировать файл ' + path_file)

    with ThreadPoolExecutor(max_workers=16) as executor:
        executor.map(copy_file, list_name, timeout=100)

    print("Обновление файлов завершено!")
    print("Обновление информации в БД...")
    cur.execute(f"""UPDATE '{table_name}' SET file_tag = 'ADD' WHERE file_tag = '{CHANGE}'""")
    conn.commit()


def change_files(original_folder_path: str, clone_folder_path: str, table_name: str, conn):
    """Проверка изменения файлов"""
    new_list_file = get_list_path_files(original_folder_path)  # Получить файлы из директории
    list_info_new_files = get_info_files(original_folder_path, new_list_file)  # информация о новых файлах
    print("Проверка изменений...")

    sql_query = pd.read_sql_query(f'''
                                   SELECT
                                   *
                                   FROM '{table_name}'
                                   ''', conn)

    df = pd.DataFrame(sql_query, columns=['name_file', 'hex_value', 'file_tag'])

    def check_file(file_info):
        # обновление информации
        name_file, hex_file = file_info[:2]
        # проверка файла в таблице
        if (df['name_file'].eq(f'{name_file}')).any():
            # если файл в таблице, то проверяем hex
            if not (hex_file == df.loc[(df['name_file'] == name_file)]['hex_value'].to_list()[0]):
                df.loc[(df.name_file == name_file), ('file_tag')] = CHANGE
                df.loc[(df.name_file == name_file), ('hex_value')] = hex_file
            else:
                df.loc[(df.name_file == name_file), ('file_tag')] = 'NOT CHANGE'
        else:
            # Если файла нет, добавляем его
            file_info_new = [file_info[0],
                             file_info[1],
                             NEW]
            df.loc[len(df.index)] = file_info_new

    with ThreadPoolExecutor(max_workers=16) as executor:
        executor.map(check_file, list_info_new_files, timeout=60)
    df.loc[(df.file_tag == "ADD"), ('file_tag')] = DELETE
    df_update = df.loc[(df['file_tag'] != 'NOT CHANGE')][['name_file', 'file_tag']]

    # df_update = colored(df_update, 'red')
    print('Обновленные файлы: ', '\n')
    if len(df_update) > 0:
        print(df_update.to_string(header=False),'\n')
        # вернуть значение
        df.loc[(df.file_tag == "NOT CHANGE"), ('file_tag')] = 'ADD'
        df.loc[(df.file_tag == NEW), ('file_tag')] = 'PENDING'
        if input(f"Синхронизировать {original_folder_path} c {clone_folder_path} ? [y/n] ").lower() == "y":
            print("Обновление информации в БД..")
            print(df)
            df.to_sql(name=table_name, con=conn, if_exists='replace')
            print("Начало синхронизации...")
            # Добавить новые файлы
            copy_files(original_folder_path, clone_folder_path, table_name, conn)
            # Удалить файлы
            delete_files(clone_folder_path, table_name, conn)
            # Обновление файлов
            update_files(original_folder_path, clone_folder_path, table_name, conn)
        else:
            print("Отказ синхронизации, BYE!")
    else:
        print("Нет новых изменений ")



def create_connect_table_db(original_folder_path: str, clone_folder_path: str) -> None:
    name_table = original_folder_path + " - " + clone_folder_path
    try:
        # создание бд
        conn = sqlite3.connect('files.db', check_same_thread=False)
        # создание курсора
        cur = conn.cursor()
        print("Подключен к БД...")
        # создание таблицы
        # создать или подключится к таблице
        cur.execute(f"""CREATE TABLE IF NOT EXISTS "{name_table}" (
                                            id integer PRIMARY KEY,
                                            name_file text,
                                            hex_value text,
                                            file_tag text 
                                    );""")
        # проверка синхронизации папок
        print("Проверка на синхронизацию папок...")
        #     если таблица пустая -> синхронизации не было
        cur.execute(f"""SELECT * from "{name_table}" """)
        records = cur.fetchall()
        if len(records) == 0:
            print("Папки не синхронизированы")

            if input(f"Синхронизировать {original_folder_path} c {clone_folder_path} ? [y/n] ").lower() == "y":
                if os.listdir(clone_folder_path+'\\') != 0:
                    if input(f"Директория {clone_folder_path} - не пустая, очистить ее? [y/n] ").lower() == "y":
                        list_files_for_delete = get_list_path_files(clone_folder_path)
                        for file_for_delete in list_files_for_delete:
                            delete_file(os.path.join(clone_folder_path, file_for_delete),clone_folder_path)
                    else:
                        pass
                print("Начало синхронизации...")
                list_path_files = get_list_path_files(original_folder_path)
                print(f"Найдено файлов:", len(list_path_files))

                df = pd.DataFrame({'name_file': list_path_files})
                print(df.to_string(header=False))

                print("Обновление информации в БД...")
                # получение info
                results = get_info_files(original_folder_path, list_path_files)
                # Добавление в бд
                for result in results:
                    add_db(name_table, conn, result)
                print("Копирование файлов...")
                copy_files(original_folder_path, clone_folder_path, name_table, conn)
                print(f"Директория: {original_folder_path} синхронизирована с директорией: {clone_folder_path}")
            else:
                print("Отказ синхронизации, BYE!")

        else:
            print("Папки синхронизированы")
            if input(f"Проверить обновление директории: {original_folder_path} ? [y/n] ").lower() == "y":
                change_files(original_folder_path, clone_folder_path, name_table, conn)
            else:
                print("Отказ синхронизации, BYE!")

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        cur.close()
        if conn:
            conn.close()
            print("Соединение с SQLite закрыто")


# parser = argparse.ArgumentParser(description='Prepare data for preprocessing')
# parser.add_argument('--originalFolder', type=str)
# parser.add_argument('--cloneFolder', type=str)
# # parser.add_argument('--maxThreads', type=int, default=4)
# # parser.add_argument('--filter', type=str, default=None)
# args = parser.parse_args()
#
# originalFolder = args.originalFolder
# cloneFolder = args.cloneFolder

original_folder_path = "C:\\Users\\gongn\\Documents\\Магистратура"
clone_folder_path = "D:\\temp\\Test"

create_connect_table_db(original_folder_path, clone_folder_path)
