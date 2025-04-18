from unitxt.blocks import LoadHF, Set, TaskCard
from unitxt.catalog import add_to_catalog, get_from_catalog
from unitxt.collections_operators import Explode, Wrap
from unitxt.image_operators import ToImage
from unitxt.operators import Copy, Shuffle
from unitxt.splitters import RenameSplits
from unitxt.test_utils.card import test_card

templates = get_from_catalog("templates.qa.with_context.all")

for language in ["en", "fr"]:
    card = TaskCard(
        loader=LoadHF(path="cmarkea/doc-vqa", data_classification_policy=["public"]),
        preprocess_steps=[
            Shuffle(),
            "splitters.small_no_dev",
            Explode(field=f"qa/{language}", to_field="pair"),
            Copy(field="pair/question", to_field="question"),
            Copy(field="pair/answer", to_field="answers"),
            Wrap(field="answers", inside="list"),
            ToImage(field="image", to_field="context"),
            Set(fields={"context_type": "image"}),
        ],
        task="tasks.qa.with_context.abstractive[metrics=[metrics.anls]]",
        templates=["templates.qa.with_context.doc_vqa", *templates.items],
        __tags__={
            "license": "apache-2.0",
            "multilinguality": "monolingual",
            "modalities": ["image", "text"],
            "size_categories": "10K<n<100K",
            "task_categories": "question-answering",
            "task_ids": "extractive-qa",
        },
        __description__=(
            "The doc-vqa Dataset integrates images from the Infographic_vqa dataset sourced from HuggingFaceM4 The Cauldron dataset, as well as images from the dataset AFTDB (Arxiv Figure Table Database) curated by cmarkea. This dataset consists of pairs of images and corresponding text, with each image linked to an average of five questions and answers available in both English and French. These questions and answers were generated using Gemini 1.5 Pro, thereby rendering the dataset well-suited for multimodal tasks involving image-text pairing and multilingual question answering."
        ),
    )

    test_card(card)
    add_to_catalog(card, f"cards.doc_vqa.{language}", overwrite=True)


card = TaskCard(
    loader=LoadHF(
        path="lmms-lab/DocVQA", name="DocVQA", data_classification_policy=["public"]
    ),
    preprocess_steps=[
        Shuffle(),
        RenameSplits(mapper={"validation": "test"}),
        ToImage(field="image", to_field="context"),
        Set(fields={"context_type": "image"}),
    ],
    task="tasks.qa.with_context.abstractive[metrics=[metrics.anls]]",
    templates=["templates.qa.with_context.doc_vqa", *templates.items],
    __tags__={
        "license": "apache-2.0",
        "multilinguality": "monolingual",
        "modalities": ["image", "text"],
        "size_categories": "10K<n<100K",
        "task_categories": "question-answering",
        "task_ids": "extractive-qa",
    },
    __description__=(
        "The doc-vqa Dataset integrates images from the Infographic_vqa dataset sourced from HuggingFaceM4 The Cauldron dataset, as well as images from the dataset AFTDB (Arxiv Figure Table Database) curated by cmarkea. This dataset consists of pairs of images and corresponding text, with each image linked to an average of five questions and answers available in both English and French. These questions and answers were generated using Gemini 1.5 Pro, thereby rendering the dataset well-suited for multimodal tasks involving image-text pairing and multilingual question answering."
    ),
)

test_card(card)
add_to_catalog(card, "cards.doc_vqa.lmms_eval", overwrite=True)
