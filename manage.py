#-*- coding:utf-8 -*-

"""
启动脚本：
    manage.py

数据库迁移：
    python manage.py db init
    python manage.py db migrate -m "information about this migrate"
    python manage.py db upgrade

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


# sys.setdefaultencoding('utf-8')


app=create_app("default")
manager=Manager(app)
migrate=Migrate(app,db)

def make_shell_context():
    """自动加载环境"""
    return dict(app=app,db=db,MovieInfo=MovieInfo)
manager.add_command("shell",Shell(make_context=make_shell_context))
manager.add_command("db",MigrateCommand)

@manager.command
def crawl():
    '''数据收集器'''
    pass

#～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～
@manager.command
def indexer():
    '''索引器'''
    lucene.initVM()
    indexDir = SimpleFSDirectory(File("index/"))
    writerConfig = IndexWriterConfig(Version.LUCENE_4_10_1, StandardAnalyzer())
    writer = IndexWriter(indexDir, writerConfig)
    movies = MovieInfo.query.limit(100).all()
    print("Index starting...")
    for n, l in enumerate(movies):
        doc = Document()
        doc.add(Field("name", l.name, Field.Store.YES, Field.Index.ANALYZED))
        doc.add(Field("shortcut", l.shortcut, Field.Store.YES, Field.Index.ANALYZED))
        # doc.add(Field('url'),l.url,Field.Store.YES,Field.Index.ANALYZED)
        writer.addDocument(doc)
        print("Item {} indexed...".format(n+1))
    print("Index finished...")
    print("Closing index of %d docs..." % writer.numDocs())
    writer.close()
#～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～

#～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～
@manager.command
def retriever(keyword):
    '''查询器'''
    result=[]
    lucene.initVM()
    analyzer = StandardAnalyzer(Version.LUCENE_4_10_1)
    reader = IndexReader.open(SimpleFSDirectory(File("index/")))
    searcher = IndexSearcher(reader)

    query = QueryParser(Version.LUCENE_4_10_1, "shortcut", analyzer).parse(keyword)
    MAX = 5
    hits = searcher.search(query, MAX)

    print("Found %d document(s) that matched query '%s':" % (hits.totalHits, query))
    for hit in hits.scoreDocs:
        print(hit.score, hit.doc, hit.toString())
        doc = searcher.doc(hit.doc)
        result.append(doc.get("shortcut"))
    reader.close()
    return result

#～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～

if __name__ == '__main__':
    manager.run()