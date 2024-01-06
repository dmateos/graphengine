import transformers
import json
import numpy as np
import base64
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.pydantic_v1 import BaseModel, Field
from langchain.output_parsers import PydanticOutputParser
#from torchvision.models import resnet50, ResNet50_Weights


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


# Image output
class Rresnet50:
    def run(self, input, metadata):
        pass


# Image detection
class OwlvitBasePatch32:
    def run(self, input, metadata):
        model = transformers.pipeline(
            model="google/owlvit-base-patch32",
            task="zero-shot-object-detection"
        )
        output = model(input, candidate_labels=metadata.split(","))
        return output


class TransformersPipelineLLM:
    def run(self, input, metadata):
        model = transformers.pipeline(model=metadata)
        output = model(input)
        return output


class TestDriver:
    def run(self, input, metadata):
        return f"{input} {metadata}"


class TestDriverImage:
    def run(self, input, metadata):
        # Generate a image out of random noise and return it
        image = np.random.randint(0, 255, (224, 224, 3))
        # Encode as base64
        image = image.tobytes()
        image = base64.b64encode(image)
        return image


class Step(BaseModel):
    id: str = Field(description="The step number")
    description: str = Field(description="The step description")
    detailed_description: str = Field(description="The step detailed description")


class Process(BaseModel):
    description: str = Field(description="The process description")
    steps: list[Step] = Field(description="The process steps")
    step_count: int = Field(description="The process step count")


class ChatGPTProcessPlanner:
    def run(self, input, metadata):
        llm = ChatOpenAI(
            model_name=metadata
        )

        query = f"#{input}"
        parser = PydanticOutputParser(pydantic_object=Process)
        prompt = PromptTemplate(
            template="Answer the user query.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )

        llm_chain = LLMChain(
            llm=llm,
            prompt=prompt,
            verbose=True
        )

        output = llm_chain.run(query)
        output = json.loads(parser.parse(output).json())
        output = json.dumps(output, indent=4)
        return output


SUPPORTED_MODELS = {
    "test": TestDriver(),
    "testImage": TestDriverImage(),
    "facebook/bart-large-mnli": BartLaegeMNLI(),
    "google/vit-base-patch16-224": VitBasePatch16_224(),
    "google/owlvit-base-patch32": OwlvitBasePatch32(),
    "ChatGPTProcessPlanning": ChatGPTProcessPlanner(),
    "TransformersPipelineLLM": TransformersPipelineLLM(),
}
