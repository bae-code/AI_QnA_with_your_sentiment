from transformers import pipeline


class HuggingFaceClient:
    def __init__(self):
        self.pipe = pipeline(
            "text-classification", model="tabularisai/multilingual-sentiment-analysis"
        )

    def classify(self, sentence: str) -> list:
        result = self.pipe(sentence)
        return result


hugging_face_client = HuggingFaceClient()
