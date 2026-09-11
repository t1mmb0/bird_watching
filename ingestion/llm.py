from pydantic import BaseModel, Field
from typing import Literal
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.common_tools.duckduckgo import duckduckgo_search_tool
import os
import asyncio
from dotenv import load_dotenv
load_dotenv()

States = Literal["Sachsen",
                 "Sachsen-Anhalt",
                 "Thüringen",
                 "Niedersachsen",
                 "Brandenburg",
                 "Berlin",
                 "Bremen",
                 "Hamburg",
                 "Bayern",
                 "Baden-Württemberg",
                 "Saarland",
                 "Rheinland-Pfalz",
                 "Hessen",
                 "Nordrhein-Westfalen",
                 "Mecklenburg-Vorpommern",
                 "Schleswig-Holstein"]

class BirdInformation(BaseModel):
    Scientific_name: str = Field(description="Name of the bird")
    min_weight_g: float = Field(description="min weight of bird")
    max_weight_g: float = Field(description="max weight of bird")
    min_body_length_cm: float = Field(description="min body length of bird")
    max_body_length_cm: float = Field(description="max body length of bird")
    wingspan_cm: float | None = Field(default = None, description="wingspan of adult bird. If unsure, leave out.")
    trivia: str = Field(description="interesting trivia about the bird.")
    state: list[States] | None = Field(default = None, description="give Location of bird. Leave out if unsure.")

_MODEL = OpenAIChatModel(
    model_name = "qwen3.6-35b-a3b",
    provider=OpenAIProvider(
        base_url = "https://gpustack.test.hs-itz.de/v1",
        api_key = os.getenv("GPUSTACK_API_KEY")
    )
)

_PROMPT = "Du bist ein Ornithologie-Experte. Fülle das Schema aus indem du die Informationen mit dem Tool nachschlägst."

LLM = Agent(_MODEL,
            instructions = _PROMPT,
            output_type = BirdInformation,
            retries=3,
            tools=[duckduckgo_search_tool()])

async def run_agent(agent, call):
    result = await agent.run(call)
    return result

async def main(agent, call):
    return await run_agent(agent, call)
    
if __name__ == "__main__":
    bird = input("Zu welchem Vogel soll recherchiert werden? (DEUTSCHER NAME UND WISSENSCHAFTLICH)")
    result = asyncio.run(main(LLM, bird))
    print(result.output)