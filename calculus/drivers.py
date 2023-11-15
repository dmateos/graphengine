import transformers


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


SUPPORTED_MODELS = {
    "facebook/bart-large-mnli": BartLaegeMNLI(),
    "google/vit-base-patch16-224": VitBasePatch16_224(),
    "google/owlvit-base-patch32": OwlvitBasePatch32(),
    "test": TestDriver(),
}
