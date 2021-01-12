#!/usr/bin/python3
# -*- coding:utf-8 -*-

import datetime
from typing import NoReturn

from lxml import etree

import private_config
import sqlite_helper
import zhihu_login


class Content:
    table_name = ''
    create_table_statement = ''

    @classmethod
    def has_table(cls) -> bool:
        result = sqlite_helper.execute('SELECT name FROM sqlite_master WHERE type="table";')
        tables = {line[0] for line in result}
        return cls.table_name in tables

    @classmethod
    def create_table(cls) -> NoReturn:
        sqlite_helper.execute(cls.create_table_statement)

    def __init__(self, url_token: str, object_created: str, title: str, content: str,
                 read_count: int, upvoted_count: int, commented_count: int):
        self.url_token = url_token
        self.object_created = object_created
        self.title = title
        self.content = content
        self.read_count = read_count
        self.upvoted_count = upvoted_count
        self.commented_count = commented_count


class Pin(Content):
    table_name = 'pin'
    create_table_statement = f'''
    CREATE TABLE {table_name} (
        url_token               text,
        object_created          text,
        title                   text,
        content                 text,
        read_count              int,
        upvoted_count           int,
        commented_count         int,
        forwarding_count        int
    );
    '''.strip()

    def __init__(self, url_token: str, object_created: str, title: str, content: str,
                 read_count: int, upvoted_count: int, commented_count: int, forwarding_count: int):
        super().__init__(url_token, object_created, title, content, read_count, upvoted_count, commented_count)
        self.forwarding_count = forwarding_count

    def save(self) -> NoReturn:
        if not self.__class__.has_table():
            self.__class__.create_table()
        result = sqlite_helper.execute(f'SELECT * FROM {self.__class__.table_name} WHERE url_token=?',
                                       (self.url_token, ))
        if not result:
            data = (self.url_token, self.object_created, self.title, self.content,
                    self.read_count, self.upvoted_count, self.commented_count, self.forwarding_count)
            sqlite_helper.execute(f'INSERT INTO {self.__class__.table_name} (url_token, object_created, '
                                  f'title, content, read_count, upvoted_count, commented_count, forwarding_count) '
                                  f'VALUES (?, ?, ?, ?, ?, ?, ?, ?);', data)


class Article(Content):
    table_name = 'article'
    create_table_statement = f'''
        CREATE TABLE {table_name} (
            url_token               text,
            object_created          text,
            title                   text,
            excerpt                 text,
            content                 text,
            read_count              int,
            complete_reading_rate   int,
            upvoted_count           int,
            commented_count         int,
            collected_count         int
        );
        '''.strip()

    def __init__(self, url_token: str, object_created: str, title: str, excerpt: str, content: str,
                 read_count: int, complete_reading_rate: int, upvoted_count: int,
                 commented_count: int, collected_count: int):
        super().__init__(url_token, object_created, title, content, read_count, upvoted_count, commented_count)
        self.excerpt = excerpt
        self.complete_reading_rate = complete_reading_rate
        self.collected_count = collected_count

    def save(self) -> NoReturn:
        if not self.__class__.has_table():
            self.__class__.create_table()
        result = sqlite_helper.execute(f'SELECT * FROM {self.__class__.table_name} WHERE url_token=?',
                                       (self.url_token,))
        if not result:
            data = (self.url_token, self.object_created, self.title, self.excerpt, self.content,
                    self.read_count, self.complete_reading_rate, self.upvoted_count,
                    self.commented_count, self.collected_count)
            sqlite_helper.execute(f'INSERT INTO {self.__class__.table_name} (url_token, object_created, '
                                  f'title, excerpt, content, read_count, complete_reading_rate, upvoted_count, '
                                  f'commented_count, collected_count) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);', data)


def get_pins() -> NoReturn:
    # 获取最近一个月的最近 10 条想法
    account = zhihu_login.ZhihuAccount(private_config.username, private_config.password)
    if account.login():
        begin_date = datetime.date.today() - datetime.timedelta(days=30)
        end_date = datetime.date.today()
        pins = account.session.get(f'https://www.zhihu.com/api/v4/creator/content_statistics/pins?'
                                   f'begin_date={begin_date}&end_date={end_date}').json()['data']
        for pin in pins:
            response = account.session.get(f'https://www.zhihu.com/pin/{pin["url_token"]}')
            html = etree.HTML(response.text)
            content = html.xpath('//*[@id="root"]/div/main/div/div/div[2]/div[1]/span')[0].xpath('string(.)')
            pin['content'] = content
            print(pin)
            p = Pin(**pin)
            p.save()


def get_articles() -> NoReturn:
    # 获取最近一个月的最近 10 篇文章
    account = zhihu_login.ZhihuAccount(private_config.username, private_config.password)
    if account.login():
        begin_date = datetime.date.today() - datetime.timedelta(days=30)
        end_date = datetime.date.today()
        articles = account.session.get(f'https://www.zhihu.com/api/v4/creator/content_statistics/articles?'
                                       f'begin_date={begin_date}&end_date={end_date}').json()['data']
        account.session.headers['Host'] = 'zhuanlan.zhihu.com'
        for article in articles:
            response = account.session.get(f'https://zhuanlan.zhihu.com/p/{article["url_token"]}')
            html = etree.HTML(response.text)
            content = html.xpath('//*[@id="root"]/div/main/div/article/div[1]/div')[0].xpath('string(.)')
            article['content'] = content
            print(article)
            a = Article(**article)
            a.save()


if __name__ == '__main__':
    get_pins()
    get_articles()
