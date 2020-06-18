# step1 - graph based representation of review corpus
#build a word adjacency graph for a comment string

#cypher language query to be used with neo4j 
INSERT_QUERY = '''
    WITH split(tolower({comment}), " ") AS words
    WITH [w in words WHERE NOT w in ["the", "and", "i", "it", "to"]] AS text
    UNWIND range(0, size(text)-2) AS i
    MERGE (W1: word{name: text[i]})
    MERGE (W2: word{name: text[i+1]})
    MERGE (W1)-[r:NEXT]->(W2)
        ON CREATE SET r.count = 1
        ON MATCH SET r.count = r.count+1 '''

#python function to query the best buy API

def load_graph(product_sku):
    for i in range(1,6):
        r = requests.get(REQUEST_URL.format(sku = product_sku, API_KEY = API_KEY, page = str(i)))
        data = r.json()
        for comment in data['reviews']:
            comments = comment["comment"].split(".")
            for sentence in comments:
                sentence = sentence.strip()
                sentence = regex.sub("", sentence)
                graph.cypher.execute(INSERT_QUERY, parameters = {'comment': sentence})

#step2 - find and score candidate summaries
#find highest ranked paths of 2-5 words

SORT_QUERY = '''
    MATCH p = (:Word)-(r: NEXT*1..4)->(:Word) WITH p
    WITH reduce (s=0,x in relationship(p) | s+x.count) AS total,p
    With nodes(p) AS text, 1.0*total/size(nodes(p)) AS weight
    RETURN extract(x in TEXT | x.name) AS phrase, weight ORDER BY weight DESC LIMIT 10'''

