import os
from dotenv import load_dotenv
from neo4j_graphrag.embeddings.openai import OpenAIEmbeddings
from neo4j_graphrag.retrievers import VectorRetriever
load_dotenv()

from neo4j import GraphDatabase

# Connect to Neo4j database
driver = GraphDatabase.driver(
    os.getenv("NEO4J_URI"), 
    auth=(
        os.getenv("NEO4J_USERNAME"), 
        os.getenv("NEO4J_PASSWORD")
    )
)

# Create embedder
# Need to use the same embedding model so vectors are compatible
embedder = OpenAIEmbeddings(model="text-embedding-ada-002")

# Create retriever
# The retriever allows specific properties to be returned from the nodes that match the query
# Uses the embedder to convert the query into a vector to use in the search
retriever = VectorRetriever(
    driver,
    neo4j_database=os.getenv("NEO4J_DATABASE"),
    index_name="moviePlots",
    embedder=embedder,
    return_properties=["title", "plot"],
)

# Search for similar items
result = retriever.search(query_text="Toys coming alive", top_k=5)

# Parse results
for item in result.items:
    print(item.content, item.metadata["score"])

# CLose the database connection
driver.close()
