# -*- coding : utf-8 -*-
import sys
from app import create_app,db
from flask_script import Manager,Shell
from app.models import Movies
from flask_migrate import Migrate,MigrateCommand

"""
下面是pylucene需要使用的java包，考虑大家的机子上没有相应的环境，运行程序会报错所以大家
在pull下来之后请先将波浪线之间的代码注释掉，在push之前解注释即可
"""
#～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～
# import lucene
# from java.io import File
# from org.apache.lucene.analysis.standard import StandardAnalyzer
# from org.apache.lucene.document import Document, Field
# from org.apache.lucene.index import IndexWriter, IndexWriterConfig
# from org.apache.lucene.store import SimpleFSDirectory
# from org.apache.lucene.util import Version
#～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～

app=create_app("default")
manager=Manager(app)
migrate=Migrate(app,db)

def make_shell_context():
    """自动加载环境"""
    return dict(app=app,db=db,Movies=Movies)
manager.add_command("shell",Shell(make_context=make_shell_context))
manager.add_command("db",MigrateCommand)

@manager.command
def crawl():
    '''数据收集器'''
    pass

#～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～
# @manager.command
# def indexer():
#     '''索引器'''
#     lucene.initVM()
#     indexDir = SimpleFSDirectory(File("index/"))
#     writerConfig = IndexWriterConfig(Version.LUCENE_4_10_1, StandardAnalyzer())
#     writer = IndexWriter(indexDir, writerConfig)
#
#     print("%d docs in index" % writer.numDocs())
#     print("Reading lines from sys.stdin...")
#     for n, l in enumerate(sys.stdin):
#         doc = Document()
#         doc.add(Field("text", l, Field.Store.YES, Field.Index.ANALYZED))
#         writer.addDocument(doc)
#     print("Indexed %d lines from stdin (%d docs in index)" % (n, writer.numDocs()))
#     print("Closing index of %d docs..." % writer.numDocs())
#     writer.close()
#～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～

#～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～
# @manager.command
# def retriever(keywords):
#     '''查询器'''
#     lucene.initVM()
#     analyzer = StandardAnalyzer(Version.LUCENE_4_10_1)
#     reader = IndexReader.open(SimpleFSDirectory(File("index/")))
#     searcher = IndexSearcher(reader)
#
#     query = QueryParser(Version.LUCENE_4_10_1, "text", analyzer).parse("我爱你")
#     MAX = 1000
#     hits = searcher.search(query, MAX)
#
#     print("Found %d document(s) that matched query '%s':" % (hits.totalHits, query))
#     for hit in hits.scoreDocs:
#         print(hit.score, hit.doc, hit.toString())
#         doc = searcher.doc(hit.doc)
#         print(doc.get("text").encode("utf-8"))
#～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～

if __name__ == '__main__':
    manager.run()