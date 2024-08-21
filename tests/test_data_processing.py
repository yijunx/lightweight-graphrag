from app.chunking.simple_chunking import SimpleChunker
from app.llm.x_llm import XInferenceLLM
from app.repositories.graph_db.neo4j_graph import Neo4jGraphRepo
from app.services.data_processing import DataProcessor
from app.utils.config import env


def test_data_processing():

    p = DataProcessor(
        chunker=SimpleChunker(),
        graph_repo=Neo4jGraphRepo(
            uri=env.NEO4J_URI,
            username=env.NEO4J_USERNAME,
            password=env.NEO4J_PASSWORD,
            db_name=env.NEO4J_DB,
        ),
        llm=XInferenceLLM(
            base_url=env.EMBEDDING_ENDPOINT, api_key="bro", model=env.LLM_MODEL_UID
        ),
    )

    p.process("crime_and_punishment.txt")
