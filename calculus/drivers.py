import transformers
import json
# from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.pydantic_v1 import BaseModel, Field
from langchain.output_parsers import PydanticOutputParser


# Sentence classification
class BartLaegeMNLI:
    def run(self, input, metadata):
        model = transformers.pipeline(model="facebook/bart-large-mnli")
        output = model(input, candidate_labels=metadata.split(","))
        return output


# Image classification
class VitBasePatch16_224:
    def run(self, input, metadata):
        model = transformers.pipeline(model="google/vit-base-patch16-224")
        output = model(images=input)
        output = [{"score": round(pred["score"], 4), "label": pred["label"]} for pred in output]
        return output


# Image detection
class OwlvitBasePatch32:
    def run(self, input, metadata):
        model = transformers.pipeline(
            model="google/owlvit-base-patch32",
            task="zero-shot-object-detection"
        )
        output = model(input, candidate_labels=metadata.split(","))
        return output


class TestDriver:
    def run(self, input, metadata):
        return f"{input} {metadata}"


class Step(BaseModel):
    id: str = Field(description="The step number")
    description: str = Field(description="The step description")
    detailed_descrition: str = Field(description="The step detailed description")


class Process(BaseModel):
    description: str = Field(description="The process description")
    steps: list[Step] = Field(description="The process steps")
    step_count: int = Field(description="The process step count")


class OpenAIDriver:
    def run(self, input, metadata):
        llm = OpenAI(
            model_name="gpt-4"
        )

        query = f"#{input}"
        parser = PydanticOutputParser(pydantic_object=Process)
        prompt = PromptTemplate(
            template="Answer the user query.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )
        output = llm(prompt.format_prompt(query=query).to_string())
        output = json.loads(parser.parse(output).json())
        output = json.dumps(output, indent=4)
        return output


SUPPORTED_MODELS = {
    "facebook/bart-large-mnli": BartLaegeMNLI(),
    "google/vit-base-patch16-224": VitBasePatch16_224(),
    "google/owlvit-base-patch32": OwlvitBasePatch32(),
    "openai": OpenAIDriver(),
    "test": TestDriver(),
}
