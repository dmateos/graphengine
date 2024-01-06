import transformers
import json
import numpy as np
import base64
import io
import torch

from PIL import Image

from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.pydantic_v1 import BaseModel, Field
from langchain.output_parsers import PydanticOutputParser

from torchvision.models.detection import fasterrcnn_resnet50_fpn_v2, FasterRCNN_ResNet50_FPN_V2_Weights
from torchvision.utils import draw_bounding_boxes
from torchvision.transforms.functional import to_pil_image, pil_to_tensor
from torchvision.io import decode_image


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
        img = Image.open(input)
        img = pil_to_tensor(img)

        weights = FasterRCNN_ResNet50_FPN_V2_Weights.DEFAULT
        model = fasterrcnn_resnet50_fpn_v2(weights=weights, box_score_thresh=0.9)
        model.eval()

        preprocess = weights.transforms()
        batch = [preprocess(img)]

        prediction = model(batch)[0]
        labels = [weights.meta["categories"][i] for i in prediction["labels"]]
        box = draw_bounding_boxes(img, boxes=prediction["boxes"], labels=labels, colors="red", width=4, font_size=30)
        pil_img = to_pil_image(box.detach())

        buffered = io.BytesIO()
        pil_img.save(buffered, format="JPEG")
        pil_img = base64.b64encode(buffered.getvalue())
        return str(pil_img)[2:-1]


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
        buffered = io.BytesIO()
        im_out = Image.open(input)
        im_out.save(buffered, format="JPEG")
        image = base64.b64encode(buffered.getvalue())
        return str(image)[2:-1]


class TestDriverRNGImage:
    def run(self, input, metadata):
        a = np.random.rand(1024, 1024, 3) * 255
        im_out = Image.fromarray(a.astype('uint8')).convert('RGB')
        buffered = io.BytesIO()
        im_out.save(buffered, format="JPEG")
        image = base64.b64encode(buffered.getvalue())
        return str(image)[2:-1]


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
    "testRNGImage": TestDriverRNGImage(),
    "facebook/bart-large-mnli": BartLaegeMNLI(),
    "google/vit-base-patch16-224": VitBasePatch16_224(),
    "google/owlvit-base-patch32": OwlvitBasePatch32(),
    "ChatGPTProcessPlanning": ChatGPTProcessPlanner(),
    "TransformersPipelineLLM": TransformersPipelineLLM(),
    "RestNet50": Rresnet50(),
}
