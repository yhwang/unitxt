from unitxt.blocks import (
    LoadHF,
    TaskCard,
)
from unitxt.catalog import add_to_catalog
from unitxt.collections_operators import GetLength
from unitxt.operators import Copy, FilterByCondition
from unitxt.settings_utils import get_settings
from unitxt.struct_data_operators import MapTableListsToStdTableJSON
from unitxt.task import Task
from unitxt.templates import InputOutputTemplate
from unitxt.test_utils.card import test_card
from unitxt.types import Table

settings = get_settings()

card = TaskCard(
    loader=LoadHF(path="ibm/finqa", streaming=False),
    preprocess_steps=[
        GetLength(field="table", to_field="table_length"),
        FilterByCondition(values={"table_length": 1}, condition="gt"),
        Copy(field="pre_text/0", to_field="pre_text"),
        Copy(field="post_text/0", to_field="post_text"),
        MapTableListsToStdTableJSON(field="table"),
    ],
    task=Task(
        inputs={
            "pre_text": str,
            "table": Table,
            "post_text": str,
            "question": str,
        },
        outputs={"program_re": str, "answer": str},
        prediction_type=str,
        metrics=["metrics.fin_qa_metric"],
        augmentable_inputs=["pre_text", "table", "post_text", "question"],
    ),
    templates=[
        InputOutputTemplate(
            instruction="""Presented with a financial report consisting of textual contents and a structured table, given a question, generate the reasoning program in the domain specific language (DSL) that will be executed to get the answer. \nThe DSL consists of mathematical operations and table operations as executable programs. The program consists of a sequence of operations. Each operation takes a list of arguments. \nThere are 6 mathematical operations: add, subtract, multiply, divide, greater, exp, and 4 table aggregation operations table-max, table-min, table-sum, table-average, that apply aggregation operations on table rows. The mathematical operations take arguments of either numbers from the given reports, or a numerical result from a previous step.\nThe table operations take arguments of table row names. We use the special token #n to denote the result from the nth step. \nFor example, in the example "divide(9413, 20.01), divide(8249, 9.48), subtract(#0, #1)", the program consists of 3 steps; The first and the second division steps take arguments from the table and the text, respectively, then the third step subtracts the results from the two previous steps.
                Definitions of all operations:
                [["Name", "Arguments", "Output", "Description"],
                ["add", "number1, number2", "number", "add two numbers: number1 + number2"],
                ["subtract", "number1, number2", "number", "subtract two numbers: number1 - number2"],
                ["multiply", "number1, number2", "number", "multiply two numbers: number1 * number2"],
                ["divide", "number1, number2", "number", "multiply two numbers: number1 / number2"],
                ["exp", "number1, number2", "number", "exponential: number1 ^ number2"],
                ["greater", "number1, number2", "bool", "comparison: number1 > number2"],
                ["table-sum", "table header", "number", "the summation of one table row"],
                ["table-average", "table header", "number", "the average of one table row"],
                ["table-max", "table header", "number", "the maximum number of one table row"],
                ["table-min", "table header", "number", "the minimum number of one table row"]]
                \nAnswer with only the program, without any additional explanation or introductory text.
                \nHere are some input-output examples. Read the examples carefully to figure out the mapping. The output of the last example is not given, and your job is to figure out what it is.
                """,
            input_format="""Pre-table text: {pre_text}
                Table: {table}
                Post-table text: {post_text}
                Question: {question}
                Program:
                    """,
            output_format="{program_re}",
            postprocessors=[
                "processors.take_first_non_empty_line",
            ],
        ),
    ],
    __description__=(
        "FINQA is an expert-annotated QA dataset that aims to tackle numerical reasoning over real-world "
        "financial data."
    ),
    __tags__={
        "modality": "table",
        "urls": {
            "arxiv": "https://www.semanticscholar.org/reader/99053e3a708fc27709c9dab33110dc98b187c158"
        },
        "languages": ["english"],
    },
)

test_card(
    card,
    num_demos=2,
    demos_pool_size=10,
)
add_to_catalog(card, "cards.fin_qa", overwrite=True)
