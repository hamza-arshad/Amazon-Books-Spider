# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sqlite3

class BooksPipeline(object):

    def __init__(self):
        self.create_connection()
        self.create_database()

    def create_connection(self):
        self.conn = sqlite3.connect('books.db')
        self.curr = self.conn.cursor()

    def create_database(self):
        self.curr.execute("""drop table if exists books;""")
        self.curr.execute("""create table books(
                            title text,
                            author text,
                            image text,
                            price text
                            )""")

    def process_item(self, item, spider):
        print("Pipeline: " + item['title'])

        self.store_item(item)

        return item

    def store_item(self, item):
        self.curr.execute("""insert into books
                            values (?, ?, ?, ?)""", (
            item['title'],
            item['author'],
            item['image'],
            item['price']
        ))
        self.conn.commit()
