from neo4j import GraphDatabase

URI = "bolt://localhost:7687"
AUTH = ("neo4j", "12345678")

drive = None
with GraphDatabase.driver(URI, auth=AUTH) as driver:
    driver.verify_connectivity()
    drive = driver