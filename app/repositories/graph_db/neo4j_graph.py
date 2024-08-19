from neo4j import GraphDatabase, RoutingControl, Driver
from app.repositories.graph_db.base import BaseFriendRepo


class Neo4jFriendRepo(BaseFriendRepo):
    def __init__(self, uri: str, username: str, password: str, db_name: str) -> None:
        self.uri = uri
        self.username = username
        self.password = password
        self.db_name = db_name

    def get_driver(self) -> Driver:
        return GraphDatabase.driver(self.uri, auth=(self.username, self.password))

    def add_friend(self, driver: Driver, name: str, friend_name: str):
        driver.execute_query(
            "MERGE (a:Person {name: $name}) "
            "MERGE (friend:Person {name: $friend_name}) "
            "MERGE (a)-[:KNOWS]->(friend)",
            name=name,
            friend_name=friend_name,
            database_=self.db_name,
        )

    def print_friends(self, driver: Driver, name: str):
        records, _, _ = driver.execute_query(
            "MATCH (a:Person)-[:KNOWS]->(friend) WHERE a.name = $name "
            "RETURN friend.name ORDER BY friend.name",
            name=name,
            database_=self.db_name,
            routing_=RoutingControl.READ,
        )
        for record in records:
            print(record["friend.name"])
