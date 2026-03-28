import importlib.util
from pathlib import Path

import pytest


NOTEBOOK_PATH = Path(__file__).resolve().parents[1] / "notebook.py"
SPEC = importlib.util.spec_from_file_location("student_notebook", NOTEBOOK_PATH)
NOTEBOOK_MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC is not None and SPEC.loader is not None
SPEC.loader.exec_module(NOTEBOOK_MODULE)

summarize_sales_debug = NOTEBOOK_MODULE.summarize_sales_debug


@pytest.mark.parametrize(
    ("data", "expected"),
    [
        pytest.param(
            [
                {"product": "Notebook", "units": 4, "unit_price": 2.5},
                {"product": "Pen", "units": 10, "unit_price": 1.2},
                {"product": "Bag", "units": 2, "unit_price": 25.0},
            ],
            (16, 72.0, 4.5),
            id="uses-units-key-example-data",
        ),
        pytest.param(
            [
                {"product": "Pencil", "units": 3, "unit_price": 1.5},
            ],
            (3, 4.5, 1.5),
            id="uses-units-key-single-record",
        ),
        pytest.param(
            [
                {"product": "Marker", "units": 0, "unit_price": 3.5},
                {"product": "Ruler", "units": 2, "unit_price": 7.25},
            ],
            (2, 14.5, 7.25),
            id="uses-units-key-with-zero-unit-row",
        ),
        pytest.param(
            [
                {"product": "Eraser", "units": 3, "unit_price": 2.33},
                {"product": "Sharpener", "units": 1, "unit_price": 1.0},
            ],
            (4, 7.99, 2.0),
            id="uses-units-key-rounds-summary-values",
        ),
        pytest.param(
            [
                {"product": "Binder", "units": 100, "unit_price": 0.4},
                {"product": "Folder", "units": 50, "unit_price": 2.4},
            ],
            (150, 160.0, 1.07),
            id="uses-units-key-large-values",
        ),
    ],
)
def test_summarize_sales_debug_uses_units_key(data, expected):
    assert summarize_sales_debug(data) == expected


@pytest.mark.parametrize(
    ("data", "expected"),
    [
        pytest.param(
            [
                {"product": "Notebook", "qty": 4, "unit_price": 2.5},
                {"product": "Pen", "qty": 10, "unit_price": 1.2},
                {"product": "Bag", "qty": 2, "unit_price": 25.0},
            ],
            (16, 72.0, 4.5),
            id="average-uses-total-units-example-data",
        ),
        pytest.param(
            [
                {"product": "Stapler", "qty": 5, "unit_price": 9.99},
            ],
            (5, 49.95, 9.99),
            id="average-uses-total-units-single-record",
        ),
        pytest.param(
            [
                {"product": "Tape", "qty": 1, "unit_price": 2.0},
                {"product": "Paper", "qty": 9, "unit_price": 4.0},
            ],
            (10, 38.0, 3.8),
            id="average-uses-total-units-mixed-quantities",
        ),
        pytest.param(
            [
                {"product": "Pen", "qty": 2, "unit_price": 5.0},
                {"product": "Pen", "qty": 3, "unit_price": 7.0},
            ],
            (5, 31.0, 6.2),
            id="average-uses-total-units-repeated-products",
        ),
        pytest.param(
            [
                {"product": "Glue", "qty": 3, "unit_price": 1.99},
                {"product": "Scissors", "qty": 2, "unit_price": 2.49},
            ],
            (5, 10.95, 2.19),
            id="average-rounds-to-two-decimals",
        ),
    ],
)
def test_summarize_sales_debug_average_per_unit(data, expected):
    assert summarize_sales_debug(data) == expected
