from typing import Iterable, List, Union

import numpy as np
from openai import Client


ENTITY_RELATIONSHIPS_GENERATION_PROMPT = """
-Goal-
Given a text document that is potentially relevant to this activity and a list of entity types, identify all entities of those types from the text and all relationships among the identified entities.

-Steps-
1. Identify all entities. For each identified entity, extract the following information:
- entity_name: Name of the entity, capitalized
- entity_type: One of the following types: [{entity_types}]
- entity_description: Comprehensive description of the entity's attributes and activities
Format each entity as ("entity", <entity_name>, <entity_type>, <entity_description>)

2. From the entities identified in step 1, identify all pairs of (source_entity, target_entity) that are *clearly related* to each other.
For each pair of related entities, extract the following information:
- source_entity: name of the source entity, as identified in step 1
- target_entity: name of the target entity, as identified in step 1
- relationship_description: explanation as to why you think the source entity and the target entity are related to each other
- relationship_strength: an integer score between 1 to 10, indicating strength of the relationship between the source entity and target entity
Format each relationship as ("relationship", <source_entity>, <target_entity>, <relationship_description>, <relationship_strength>)

3. Return output in english as a single list of all the entities and relationships identified in steps 1 and 2. Use **---** as the list delimiter.

4. If you have to translate into english, just translate the descriptions, nothing else!

5. When finished, output ---

######################
-Examples-
######################
Example 1:
Entity_types: ORGANIZATION,PERSON
Text:
The Verdantis's Central Institution is scheduled to meet on Monday and Thursday, with the institution planning to release its latest policy decision on Thursday at 1:30 p.m. PDT, followed by a press conference where Central Institution Chair Martin Smith will take questions. Investors expect the Market Strategy Committee to hold its benchmark interest rate steady in a range of 3.5%-3.75%.
######################
Output:
("entity", CENTRAL INSTITUTION, ORGANIZATION, The Central Institution is the Federal Reserve of Verdantis, which is setting interest rates on Monday and Thursday)
---
("entity", MARTIN SMITH, PERSON, Martin Smith is the chair of the Central Institution)
---
("entity", MARKET STRATEGY COMMITTEE, ORGANIZATION, The Central Institution committee makes key decisions about interest rates and the growth of Verdantis's money supply)
---
("relationship", MARTIN SMITH, CENTRAL INSTITUTION, Martin Smith is the Chair of the Central Institution and will answer questions at a press conference, 9)
.

######################
Example 2:
Entity_types: ORGANIZATION
Text:
TechGlobal's (TG) stock skyrocketed in its opening day on the Global Exchange Thursday. But IPO experts warn that the semiconductor corporation's debut on the public markets isn't indicative of how other newly listed companies may perform.

TechGlobal, a formerly public company, was taken private by Vision Holdings in 2014. The well-established chip designer says it powers 85% of premium smartphones.
######################
Output:
("entity", TECHGLOBAL, ORGANIZATION, TechGlobal is a stock now listed on the Global Exchange which powers 85% of premium smartphones)
---
("entity", VISION HOLDINGS, ORGANIZATION, Vision Holdings is a firm that previously owned TechGlobal)
---
("relationship", TECHGLOBAL, VISION HOLDINGS, Vision Holdings formerly owned TechGlobal from 2014 until present, 5)
.

######################
Example 3:
Entity_types: ORGANIZATION,GEO,PERSON
Text:
Five Aurelians jailed for 8 years in Firuzabad and widely regarded as hostages are on their way home to Aurelia.

The swap orchestrated by Quintara was finalized when $8bn of Firuzi funds were transferred to financial institutions in Krohaara, the capital of Quintara.

The exchange initiated in Firuzabad's capital, Tiruzia, led to the four men and one woman, who are also Firuzi nationals, boarding a chartered flight to Krohaara.

They were welcomed by senior Aurelian officials and are now on their way to Aurelia's capital, Cashion.

The Aurelians include 39-year-old businessman Samuel Namara, who has been held in Tiruzia's Alhamia Prison, as well as journalist Durke Bataglani, 59, and environmentalist Meggie Tazbah, 53, who also holds Bratinas nationality.
######################
Output:
("entity", FIRUZABAD, GEO, Firuzabad held Aurelians as hostages)
---
("entity", AURELIA, GEO, Country seeking to release hostages)
---
("entity", QUINTARA, GEO, Country that negotiated a swap of money in exchange for hostages)
---
---
("entity", TIRUZIA, GEO, Capital of Firuzabad where the Aurelians were being held)
---
("entity", KROHAARA, GEO, Capital city in Quintara)
---
("entity", CASHION, GEO, Capital city in Aurelia)
---
("entity", SAMUEL NAMARA, PERSON, Aurelian who spent time in Tiruzia's Alhamia Prison)
---
("entity", ALHAMIA PRISON, GEO, Prison in Tiruzia)
---
("entity", DURKE BATAGLANI, PERSON, Aurelian journalist who was held hostage)
---
("entity", MEGGIE TAZBAH, PERSON, Bratinas national and environmentalist who was held hostage)
---
("relationship", FIRUZABAD, AURELIA, Firuzabad negotiated a hostage exchange with Aurelia, 2)
---
("relationship", QUINTARA, AURELIA, Quintara brokered the hostage exchange between Firuzabad and Aurelia, 2)
---
("relationship", QUINTARA, FIRUZABAD, Quintara brokered the hostage exchange between Firuzabad and Aurelia, 2)
---
("relationship", SAMUEL NAMARA, ALHAMIA PRISON, Samuel Namara was a prisoner at Alhamia prison, 8)
---
("relationship", SAMUEL NAMARA, MEGGIE TAZBAH, Samuel Namara and Meggie Tazbah were exchanged in the same hostage release, 2)
---
("relationship", SAMUEL NAMARA, DURKE BATAGLANI, Samuel Namara and Durke Bataglani were exchanged in the same hostage release, 2)
---
("relationship", MEGGIE TAZBAH, DURKE BATAGLANI, Meggie Tazbah and Durke Bataglani were exchanged in the same hostage release, 2)
---
("relationship", SAMUEL NAMARA, FIRUZABAD, Samuel Namara was a hostage in Firuzabad, 2)
---
("relationship", MEGGIE TAZBAH, FIRUZABAD, Meggie Tazbah was a hostage in Firuzabad, 2)
---
("relationship", DURKE BATAGLANI, FIRUZABAD, Durke Bataglani was a hostage in Firuzabad, 2)


-Real Data-
######################
entity_types: {entity_types}
text: {input_text}
######################
output:
"""


input_text = """
The XYZ Company is a leading technology organization that specializes in software development and data analytics. Alice is the CEO of the company and she is responsible for setting the strategic direction and overseeing the overall operations. Bob is the head of the engineering department and he leads a team of talented software engineers who develop innovative solutions for clients. Carol is the chief data scientist and she is in charge of analyzing large datasets to extract valuable insights for the organization. Debby is the project manager and she ensures that projects are delivered on time and within budget. Emily is a senior software engineer who works closely with Bob and the engineering team to implement new features and improve existing software. Francis is the marketing manager and he is responsible for promoting the company's products and services to potential clients. The strong relationship among Alice, Bob, Carol, Debby, Emily, and Francis is crucial for the success of the XYZ Company. They collaborate closely, share information, and support each other to achieve the company's goals and deliver high-quality solutions to clients.
"""



class XInferenceLLM:
    def __init__(self, base_url: str, api_key: str, model: str):
        self.base_url = base_url
        self.api_key = api_key
        self.model_name = model
        self.client = Client(base_url=self.base_url, api_key=self.api_key)

    def do_it(self, context: str):
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": ENTITY_RELATIONSHIPS_GENERATION_PROMPT.format(entity_types="ORGANIZATION,PERSON,LOCATION", input_text=context)},
                # {
                #     "role": "user",
                #     "content": context,
                # },
            ],
            temperature=0,
        )
        
        return response.choices[0].message.content


if __name__ == "__main__":
    from app.utils.config import env
    x = XInferenceLLM(
        base_url=env.EMBEDDING_ENDPOINT,
        api_key="speak and see it done",
        model=env.LLM_MODEL_UID
    )
    print(x.do_it(context=input_text))

