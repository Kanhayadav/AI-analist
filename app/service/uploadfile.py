import pandas as pd
import numpy as np
from io import BytesIO
from fastapi import FastAPI,UploadFile,HTTPException
from pathlib import Path
from app.cleaning.cleaning import clean_df
from app.service.file_manager import (
    save_raw_file,
    save_clean_dataframe
)
from app.dataset_understanding.analyzer import analyze_dataset
from app.user_query_understanding.parser import parse_user_query
from app.ml_pipline.featureselection.selector import feature_selector
from app.ml_pipline.preprocessing.preprocessing import preprocess
from app.ml_pipline.training.trainer import train_model
from app.ml_pipline.prediction.predictor import predict
from app.llm.business_summary import explain_results
from app.feature_engineering.feature_engineering import engineer_features
from fastapi import (
    FastAPI,
    UploadFile,
    HTTPException,
    Form
)

app = FastAPI()

@app.post("/uploadfile/")
async def upload_csv(file:UploadFile,query: str = Form(...)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="This is not a csv file")

    contents=await file.read()
    raw_path = save_raw_file(
    contents,
    file.filename
)

    try:
        df=pd.read_csv(BytesIO(contents)) 
        cleaned_df, cleaning_report = clean_df(df)

        dataset_report = analyze_dataset(cleaned_df)

        query_report = parse_user_query(
            query,
            cleaned_df.columns.tolist()
        )          

        featured_df, feature_report = engineer_features(
            cleaned_df,
            dataset_report["final_mapping"]
        )


        X, y, feature_selection_report = feature_selector(
            featured_df,
            query_report
        )
        (
            X_train,
            X_test,
            y_train,
            y_test,
            scaler,
            preprocessing_report
        ) = preprocess(
            X,
            y
        )   

        training_report = train_model(
        X_train,
        X_test,
        y_train,
        y_test,
        query_report
    )

        predictions = predict(
            training_report["model"],
            X_test
        )

        business_summary = explain_results(
        query_report,
        training_report,
        feature_selection_report
    )

        clean_path = save_clean_dataframe(
        featured_df,
        raw_path
        )

        Path(raw_path).unlink(missing_ok=True)

        data_dict = featured_df.to_dict(orient="records")
        rows,cols=featured_df.shape
        column_names=featured_df.columns.tolist()
        datatypes={
            column:str(dtype)
            for column, dtype in featured_df.dtypes.items()
            }
        Missing_values=featured_df.isna().sum().to_dict()
        Duplicate_rows=int(featured_df.duplicated().sum())
        Summary_statistics = (
        featured_df
        .describe(include="all")
        .replace([np.nan, np.inf, -np.inf], None)
        .to_dict()
    )
    except Exception as e:
        try:
            Path(raw_path).unlink(missing_ok=True)
        except Exception:
            pass

        raise HTTPException(status_code=400,detail=f'Could not Parse the file: {str(e)}')
    return {
        "fileName":file.filename,
        "rows":rows,
        "cols":cols,
        "column_names":column_names,
        "data_types":datatypes,
        "Missing_values":Missing_values,  
        "Duplicate_rows":Duplicate_rows,
        "Summary_statistics":Summary_statistics,
        "raw_file": None,
        "clean_file": str(clean_path),
        "cleaning_report": cleaning_report,
        "feature_report": feature_report,
        "dataset_understanding": dataset_report,
        "query_understanding": query_report,
        "feature_selection": feature_selection_report,
        "preprocessing": preprocessing_report,
        "training": {
            "best_model": training_report["best_model_name"],
            "metrics": training_report["metrics"],
            "model_path": training_report["model_path"]
        },
        "predictions": predictions[:10],
        "business_summary": business_summary,
        "preview":data_dict[:5]
    }