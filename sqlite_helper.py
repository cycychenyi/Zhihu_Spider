#!/usr/bin/python3
# -*- coding:utf-8 -*-

import sqlite3
from typing import Tuple

import private_config


def execute(statement: str, data: Tuple = ()):
    connection = sqlite3.connect(private_config.sqlite_file)
    cursor = connection.cursor()
    cursor.execute(statement, data)
    result = cursor.fetchall()
    cursor.close()
    connection.commit()
    connection.close()
    return result

