from app.utils.config import env
from app.services.service import FriendService
from app.repositories.graph_db.neo4j_graph import Neo4jFriendRepo


def main():
    s = FriendService(
        friend_repo=Neo4jFriendRepo(
            uri=env.NEO4J_URI,
            username=env.NEO4J_USERNAME,
            password=env.NEO4J_PASSWORD,
            db_name=env.NEO4J_DB,
        )
    )
    s.something_needs_add_friend()
    s.something_needs_print_friends()


# make sure you are using the driver with with
if __name__ == "__main__":
    main()
