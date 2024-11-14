from unitxt import evaluate, load_dataset, settings
from unitxt.inference import (
    LiteLLMInferenceEngine,
)
from unitxt.text_utils import print_dict

with settings.context(
    disable_hf_datasets_cache=False,
    allow_unverified_code=True,
):
    test_dataset = load_dataset("benchmarks.bluebench", split="test")

# Infer
inference_model = LiteLLMInferenceEngine(
    model="watsonx/meta-llama/llama-3-8b-instruct",
    max_tokens=30,
    max_requests_per_second=6,
)

predictions = inference_model.infer(test_dataset)
evaluated_dataset = evaluate(predictions=predictions, data=test_dataset)

print_dict(
    evaluated_dataset[0],
    keys_to_print=[
        "source",
        "prediction",
        "subset",
    ],
)
print_dict(
    evaluated_dataset[0]["score"]["subsets"],
)