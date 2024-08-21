from neo4j import Driver, GraphDatabase, RoutingControl, Record

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

    def add_entity(self, driver: Driver, entity_type: str, name: str, description_id: str):
        driver.execute_query(
            f"MERGE (a:{entity_type} {{name: $name, description: $description}})",
            name=name,
            description=description_id,
            database_=self.db_name,
        )

    def add_relation(self, driver: Driver, entity_type_from: str, entity_type_to: str, name_from: str, name_to: str, description_id: str, strength: int):
        driver.execute_query(
            f"MATCH (a:{entity_type_from} {{name: $name_from}}) "
            f"MATCH (b:{entity_type_to} {{name: $name_to}}) "
            f"MERGE (a)-[:RELATES {{description: $description, strength:$strength}}]->(b)",
            name_from=name_from,
            name_to=name_to,
            description=description_id,
            strength=strength,
            database_=self.db_name
        )
    
    def get_entity(self, driver: Driver, entity_type: str, name: str):
        records: list[Record]
        records, _, _ = driver.execute_query(
            f"MATCH (a:{entity_type} {{name: $name}}) "
            f"RETURN a.description",
            name=name,
            database_=self.db_name,
            routing_=RoutingControl.READ,
        )
        return records

    def query_relation_description(self, driver: Driver, entity_type_from: str, entity_type_to: str, name_from: str, name_to: str):

        # type notation.. to make nothing white
        records: list[Record]
        records, _, _ = driver.execute_query(
            f"MATCH (a:{entity_type_from} {{name: $name_from}})-[r:RELATES]->(b:{entity_type_to} {{name: $name_to}}) "
            f"RETURN r.description, r.strength",
            name_from=name_from,
            name_to=name_to,
            database_=self.db_name,
            routing_=RoutingControl.READ,
        )
        print([r.items() for r in records])
        return records
    
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

    
    # def properties_query(self, driver: Driver):

    #     node_properties_query = """
    #     CALL apoc.meta.data()
    #     YIELD label, other, elementType, type, property
    #     WHERE NOT type = "RELATIONSHIP" AND elementType = "node"
    #     WITH label AS nodeLabels, collect(property) AS properties
    #     RETURN {labels: nodeLabels, properties: properties} AS output

    #     """

    #     rel_properties_query = """
    #     CALL apoc.meta.data()
    #     YIELD label, other, elementType, type, property
    #     WHERE NOT type = "RELATIONSHIP" AND elementType = "relationship"
    #     WITH label AS nodeLabels, collect(property) AS properties
    #     RETURN {type: nodeLabels, properties: properties} AS output
    #     """

    #     rel_query = """
    #     CALL apoc.meta.data()
    #     YIELD label, other, elementType, type, property
    #     WHERE type = "RELATIONSHIP" AND elementType = "node"
    #     RETURN {source: label, relationship: property, target: other} AS output
    #     """
    #     records, _, _ = driver.execute_query(
    #         node_properties_query,
    #         database_=self.db_name,
    #         routing_=RoutingControl.READ,
    #     )
    #     print(records)

    # def add_procedure(self, driver: Driver, name: str, procedure: str):
    #     driver.execute_query(
    #         f"CALL dbms.procedures.register('{name}', '{procedure}')",
    #         database_=self.db_name,
    #     )


if __name__ == "__main__":
    repo = Neo4jFriendRepo(
        uri="neo4j://neo4j:7687",
        username="neo4j",
        password="very-cool-password",
        db_name="neo4j",
    )
    with repo.get_driver() as driver:
        # repo.add_entity(driver, "Person", "Tom1", "uuid1")
        # repo.add_entity(driver, "Person", "Emily1", "uuid2")
        # repo.add_relation(driver, "Person", "Person", "Tom1", "Emily1", "uuid4", 10)
        # print(repo.query_relation_description(driver, "Person", "Person", "Tom1", "Emily1"))
        repo.properties_query(driver)
