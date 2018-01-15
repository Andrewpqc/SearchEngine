#-*- coding:utf-8 -*-

"""
数据库迁移：
    python manage.py db init
    python manage.py db migrate -m "key information"
    python manage.py db upgrade

建立索引：
    python manage.py indexer

启动程序：
    python manage.py runserver

"""

import sys
from app import create_app,db
from flask_script import Manager,Shell
from app.models import MovieInfo
from flask_migrate import Migrate,MigrateCommand

"""
下面是pylucene需要使用的java包，考虑大家的机子上没有相应的环境，运行程序会报错所以大家
在pull下来之后请先将波浪线之间的代码注释掉，在push之前解注释即可
"""
#～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～
import lucene
from java.io import File
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field
from org.apache.lucene.index import IndexWriter, IndexWriterConfig, IndexReader
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.util import Version
#～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～




app=create_app("default")
manager=Manager(app)
migrate=Migrate(app,db)

def make_shell_context():
    """自动加载环境"""
    return dict(app=app,db=db,MovieInfo=MovieInfo)
manager.add_command("shell",Shell(make_context=make_shell_context))
manager.add_command("db",MigrateCommand)


'''
flag : 标志变量，实现单例模式,防止多次启动初始化JVM，实现单例模式
'''
flag = True


@manager.command
def crawl():
    '''
    数据收集器,这里数据以前已经爬取，直接使用原来的数据
    '''
    pass

#～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～

'''
       Field.Store.YES:存储字段值（未分词前的字段值）
       Field.Store.NO:不存储,存储与索引没有关系
       Field.Store.COMPRESS:压缩存储,用于长文本或二进制，但性能受损

       Field.Index.ANALYZED:分词建索引
       Field.Index.ANALYZED_NO_NORMS:分词建索引，但是Field的值不像通常那样被保存，而是只取一个byte，这样节约存储空间
       Field.Index.NOT_ANALYZED:不分词且索引
       Field.Index.NOT_ANALYZED_NO_NORMS:不分词建索引，Field的值去一个byte保存
'''
@manager.command
def indexer():
    '''索引器'''
    lucene.initVM()
    indexDir = SimpleFSDirectory(File("index/"))
    writerConfig = IndexWriterConfig(Version.LUCENE_CURRENT, StandardAnalyzer())
    writer = IndexWriter(indexDir, writerConfig)
    movies = MovieInfo.query.limit(10000).all()
    print("Index starting...")
    for n, l in enumerate(movies):
        doc = Document()
        doc.add(Field("name", l.name, Field.Store.YES, Field.Index.ANALYZED))
        doc.add(Field("shortcut", l.shortcut, Field.Store.YES, Field.Index.ANALYZED))
        doc.add(Field('url',l.url,Field.Store.YES,Field.Index.ANALYZED))
        writer.addDocument(doc)
        print("Item {} indexed...".format(n+1))
    print("Index finished...")
    print("Closing index of %d docs..." % writer.numDocs())
    writer.close()

@manager.command
def shourcut_retriever(keyword):
    '''查询器：在简介中查询'''
    global flag
    if flag:
        lucene.initVM()
    flag=False
    analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)
    reader = IndexReader.open(SimpleFSDirectory(File("index/")))
    searcher = IndexSearcher(reader)

    query = QueryParser(Version.LUCENE_4_10_1, "shortcut", analyzer).parse(keyword)
    MAX = 20
    hits = searcher.search(query, MAX)

    print("Found %d document(s) that matched query '%s':" % (hits.totalHits, query))
    results = []
    for hit in hits.scoreDocs:
        print(hit.score, hit.doc, hit.toString())
        doc = searcher.doc(hit.doc)
        result=[doc.get('shortcut'),doc.get('url'),doc.get('name')]
        print(doc.get('url'))
        results.append(result)
    return results
#～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～

if __name__ == '__main__':
    manager.run()