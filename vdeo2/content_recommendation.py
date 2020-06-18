# Content-based filtering of content recommendation

#building the article graph - articles users have shared, extract keywords, insert in the graph, scrape additional articles

INSERT_ARTICLE_QUERY = '''
    MERGE (u: URL{url: {url}})
    SET u.title = {title}
    FOREACH (keyword in {keywords} | MERGE (k: keyword{text:keyword} CREATE UNIQUE (k)<-[:IS_ABOUT] - (u)))
    FOREACH (img in {images} | MERGE (i: image{url:img} <-[:WITH_IMAGE] - (u))
    FOREACH (vid in {videos} | MERGE (v: videos{url:vid} <-[:WITH_VIDEO] - (u))
    FOREACH (author in {authors} | MERGE (a: authors{name:author} <-[:AUTHORED_BY] - (u)) '''

INSERT_LIKED_QUERY = '''
    MERGE (u: User {name: {username}})
    MERGE (u : URL {url: {url}})
    CREATE UNIQUE (u)-[:LINKED] -> (a) '''

#output query
# this shows the graph of the liked articles by the users and each liked articles keywords as next level nodes
LIKED_QUERY = '''
    MATCH (:User) - [:LIKED]->(article: URL)-[:IS_ABOUT]->(k:keyword)
    WHERE u.name = "suchana"
    RETURN u,article, k LIMIT 10 '''

# for content recommendation first step is to see what keywords the user is mostly interested in

SORT_KEYWORDS = '''
    MATCH(u:User)-[:LIKED]-(article:URL)-[:IS_ABOUT]->(k:keyword)
    WHERE u.name = "suchana"
    RETURN k.text as keyword, count(k) AS num ORDER BY num DESC LIMIT 25 '''

#the last line counts the number of times each keyword appears on the articles that I liked

# next is find other articles that have the same set of keywords

RECOMMEND_ARTICLES = '''
    MATCH( u : User)-[:LIKED]->(article: URL)-[:IS_ABOUT]->(k:keyword)
    WHERE u.name = "suchana"
    MATCH (k) <- [:IS_aBOUT]-(rec:URL) WHERE NOT (u)-[:LIKED] -> (rec)
    WITH rec, collect (DISTINCT k text) AS keywords
    RETURN rec.title, size(keywords) AS weight, keywords ORDER BY weight DESC LIMIT 10 '''

# this count the number of times the article has overlapping keywords that I'm interested in. And I am taking the 
# size of those overlapping keywords as the weight and we're going to return 10 recommendations ordered by the weight in desc order

# Hence we are able to prioritize article links I'm interested in.
