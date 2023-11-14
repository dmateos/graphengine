import transformers


class BartLaegeMNLI:
    def run(self, input, metadata):
        model = transformers.pipeline(model="facebook/bart-large-mnli")
        output = model(input, candidate_labels=metadata.split(","))
        return output


class VitBasePatch16_224:
    def run(self, input, metadata):
        model = transformers.pipeline(model="google/vit-base-patch16-224")
        output = model(images=input)
        output = [{"score": round(pred["score"], 4), "label": pred["label"]} for pred in output]
        return output


class TestDriver:
    def run(self, input, metadata):
        return str(input) + " " + str(metadata)


SUPPORTED_MODELS = {
    "facebook/bart-large-mnli": BartLaegeMNLI(),
    "google/vit-base-patch16-224": VitBasePatch16_224(),
    "test": TestDriver(),
}
