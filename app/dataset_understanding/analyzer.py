from .column_mapper import map_columns
from .llm_mapper import llm_column_mapper
from .task_detector import detect_task
from .model_recommender import recommend_models

def analyze_dataset(df):

    report = {}

    mapping, unknown_columns = map_columns(df)

    report["rule_based_mapping"] = mapping
    report["unknown_columns"] = unknown_columns
    llm_mapping = {}
    if unknown_columns:

        llm_mapping = llm_column_mapper(unknown_columns)

        report["llm_mapping"] = llm_mapping

        for column, details in llm_mapping.items():

            mapping[column] = details["mapped_to"]

    report["final_mapping"] = mapping



    # NEW
    task_report = detect_task(df, mapping)
    models = recommend_models(
    task_report["recommended_task"]
    )

    report["task_detection"] = task_report
    report["recommended_models"] = models

    return report