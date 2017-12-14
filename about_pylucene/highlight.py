from lucene import \
            QueryParser, IndexSearcher, IndexReader, StandardAnalyzer, \
        TermPositionVector, SimpleFSDirectory, File, SimpleSpanFragmenter, Highlighter, \
    QueryScorer, StringReader, SimpleHTMLFormatter, \
            VERSION, initVM, Version
import sys

FIELD_CONTENTS = "contents"
FIELD_PATH = "path"
#QUERY_STRING = "lucene and restored"
QUERY_STRING = sys.argv[1]
STORE_DIR = "/home/kanaujia/lucene_index"

if __name__ == '__main__':
    initVM()
    print 'lucene', VERSION

    # Get handle to index directory
    directory = SimpleFSDirectory(File(STORE_DIR))

    # Creates a searcher searching the provided index.
    ireader  = IndexReader.open(directory, True)

    # Implements search over a single IndexReader.
    # Use a single instance and use it across queries
    # to improve performance.
    searcher = IndexSearcher(ireader)

    # Get the analyzer
    analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)

    # Constructs a query parser.
    queryParser = QueryParser(Version.LUCENE_CURRENT, FIELD_CONTENTS, analyzer)

    # Create a query
    query = queryParser.parse(QUERY_STRING)

    topDocs = searcher.search(query, 50)

    # Get top hits
    scoreDocs = topDocs.scoreDocs
    print "%s total matching documents." % len(scoreDocs)

    HighlightFormatter = SimpleHTMLFormatter();
    query_score = QueryScorer (query)

    highlighter = Highlighter(HighlightFormatter, query_score)

    # Set the fragment size. We break text in to fragment of 64 characters
    fragmenter  = SimpleSpanFragmenter(query_score, 64);
    highlighter.setTextFragmenter(fragmenter);

    for scoreDoc in scoreDocs:
        doc = searcher.doc(scoreDoc.doc)
    text = doc.get(FIELD_CONTENTS)
    ts = analyzer.tokenStream(FIELD_CONTENTS, StringReader(text))
        print doc.get(FIELD_PATH)
        print highlighter.getBestFragments(ts, text, 3, "...")
    print ""