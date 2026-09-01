import pandas as pd
import pytest
from app.pipeline import run_pipeline

def test_pipeline_creates_summary_file(tmp_path):
    input_file = tmp_path / "sales.csv"
    output_file = tmp_path / "summary.csv"

    input_file.write_text(
        "order_id,customer,amount\n"
        "1,Ana,100.0\n"
        "2,Bruno,200.0\n",
        encoding="utf-8",
    )

    run_pipeline(str(input_file), str(output_file))

    result = pd.read_csv(output_file)

    assert result.loc[0, "total_sales"] == 300.0
    assert result.loc[0, "avg_sales"] == 150.0
    assert result.loc[0, "total_orders"] == 2


def test_pipeline_raises_error_for_negative_values(tmp_path):
    input_file = tmp_path / "sales_invalid.csv"
    output_file = tmp_path / "summary.csv"

    input_file.write_text(
        "order_id,customer,amount\n"
        "1,Ana,-10.0\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="Valores negativos"):
        run_pipeline(str(input_file), str(output_file))


def test_creates_annual_report(tmp_path):
    input_file = tmp_path / "sales.csv"
    output_file = tmp_path / "annual_summary.csv"

    input_file.write_text(
        "order_id,customer,amount,date\n"
        "1,Ana,100.0,2023-01-15\n"
        "2,Bruno,200.0,2023-02-20\n"
        "3,Carlos,150.0,2024-03-10\n",
        encoding="utf-8",
    )

    from app.pipeline import create_annual_report

    create_annual_report(str(input_file), str(output_file))

    result = pd.read_csv(output_file)

    assert len(result) == 2
    assert result.loc[result["year"] == 2023, "total_sales"].values[0] == 300.0
    assert result.loc[result["year"] == 2024, "total_sales"].values[0] == 150.0