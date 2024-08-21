from typing import Iterable, List, Union

import numpy as np
from openai import Client

from app.llm.base import BaseLLM
from app.llm.prompts import ENTITY_RELATIONSHIPS_GENERATION_PROMPT


class XInferenceLLM(BaseLLM):
    def __init__(self, base_url: str, api_key: str, model: str):

        # to make the client
        self.base_url = base_url
        self.api_key = api_key
        self.model_name = model
        self.client = Client(base_url=self.base_url, api_key=self.api_key)

        # what to extract from the text
        # and what kind of cypher llm generates
        # self.entity_types = entity_types

    def extract_entity_and_relation(self, context: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {
                    "role": "system",
                    "content": ENTITY_RELATIONSHIPS_GENERATION_PROMPT.format(
                        entity_types="ORGANIZATION,PERSON,LOCATION",
                        input_text=context,
                        language="english",
                    ).format(
                        tuple_delimiter="*",
                        record_delimiter="---",
                        completion_delimiter="---",
                    ),
                },
                # {
                #     "role": "user",
                #     "content": context,
                # },
            ],
            temperature=0,
        )

        return response.choices[0].message.content

    def contruct_cypher(self, question: str) -> str:
        # cypher = ""
        # for entity in entities:
        #     cypher += f"CREATE (:{entity['entity_type']} {{name: '{entity['entity_name']}', description: '{entity['entity_description']}'}})\n"
        # for relation in relations:
        #     cypher += f"CREATE ({relation['source_entity']})-[:{relation['relationship_description']}]->({relation['target_entity']})\n"
        # return cypher
        system_message = """
Task: Generate Cypher queries to query a Neo4j graph database based on the provided schema definition.
Instructions:
Use only the provided relationship types and properties.
Do not use any other relationship types or properties that are not provided.
If you cannot generate a Cypher statement based on the provided schema, explain the reason to the user.
Schema:

This is the schema representation of the Neo4j database.
Node types are the following:
Person,Organization,Location
Node properties are the following:
name,description
Relationship properties are the following:
strength,description
Relationship point from source to target nodes
RELATES
Make sure to respect relationship types and directions

Note: Do not include any explanations or apologies in your responses.
        """
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": question},
        ]
        # Used for Cypher healing flows
        # if history:
        #     messages.extend(history)

        completions = self.client.chat.completions.create(
            model=self.model_name, temperature=0, messages=messages
        )
        return completions.choices[0].message.content


if __name__ == "__main__":
    from app.utils.config import env

    x = XInferenceLLM(
        base_url=env.EMBEDDING_ENDPOINT,
        api_key="speak and see it done",
        model=env.LLM_MODEL_UID,
    )

    from app.chunking.simple_chunking import SimpleChunker

    # chunker = SimpleChunker()
    # # input_text = """
    # # The XYZ Company is a leading technology organization that specializes in software development and data analytics. Alice is the CEO of the company and she is responsible for setting the strategic direction and overseeing the overall operations. Bob is the head of the engineering department and he leads a team of talented software engineers who develop innovative solutions for clients. Carol is the chief data scientist and she is in charge of analyzing large datasets to extract valuable insights for the organization. Debby is the project manager and she ensures that projects are delivered on time and within budget. Emily is a senior software engineer who works closely with Bob and the engineering team to implement new features and improve existing software. Francis is the marketing manager and he is responsible for promoting the company's products and services to potential clients. The strong relationship among Alice, Bob, Carol, Debby, Emily, and Francis is crucial for the success of the XYZ Company. They collaborate closely, share information, and support each other to achieve the company's goals and deliver high-quality solutions to clients.
    # # """
    # for chunk in chunker.chunk(text_file_path="crime_and_punishment.txt"):
    #     print(chunk)
    #     print(x.extract_entity_and_relation(context=chunk))
    #     break
    # print(x.contruct_cypher(question="What is relation of Tom and Emily"))
    # MATCH (p1:Person {name: 'Tom'})-[:RELATES]->(p2:Person {name: 'Emily'})
    # RETURN p1, p2, p1.RELATES.p2.strength, p1.RELATES.p2.description

    print(x.contruct_cypher(question="What organizations are related to Tom"))

    # MATCH (p:Person {name: 'Tom'})-[:RELATES]->(o:Organization)
    # RETURN o.name, o.description

    print(x.contruct_cypher(question="Who is Tom"))

    # now bring the cypher to the neo4j and see if it works
