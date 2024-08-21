# lightweight-graphrag
my hobby is to reinvent the wheel


### ideas from

* from document to graph: https://neo4j.com/developer-blog/global-graphrag-neo4j-langchain/ 
* from query to cypher: https://neo4j.com/developer-blog/generating-cypher-queries-with-chatgpt-4-on-any-graph-schema/
* but i am not going to use langchain
* and local llm model is used


### ideas here

* data processing
    * chunk the text
    * each chunk
        * the llm is prompt to return node/relation in a format that can be easily parsed into cypher.
        * create an embedding and save to vector db

* answer question
    * given the question
        * creates embedding and search from vector db
        * let llm forms the cypher to search from the graph, get result from graph, let llm summerize
        * from both above results, let llm answer the question


### Material: Crime and Punishment
curl https://www.gutenberg.org/cache/epub/2554/pg2554.txt > crime_and_punishment.txt

### data model

according to neo4j's documentation:
```
Before creating a property graph database, it is important to develop an appropriate data model. This will provide structure to the data, and allow users of the graph to efficiently retrieve the information they are looking for.
```

however such data model will have to change based on the business use. The person label for linkedin will be different compared to the person label for literature.

### pipeline

* chunk
* from chunk get entities and relation
* for entity and relation
    * create id
    * this id is used for postgres, to store the descriptions
* embeding the chunks for rag (raw_text_colletion)

* cronjobs:
    * postgres
    * node resolution

### answer question

* who are the main characters:
    * forms the cypher of getting 10 most connected PERSON nodes
    * use the cypher to 


* who is closely related to xxx


* what is xxxxx

* who does xxx love?
    * forms the cypher of most connected nodes
    * list out the persons and the relation ids
    * from relation ids, get the context from postgres
    * the rag




