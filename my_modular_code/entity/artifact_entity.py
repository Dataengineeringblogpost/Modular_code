from dataclasses import dataclass
@dataclass
class DataIngestionArtifact:
    feature_store_file_path:str
    train_file_path:str
    test_file_path:str

@dataclass
class DataValidationArtifact:
    report_file_path:str


@dataclass
class DataTransformationArtifact:
    trasform_object_path:str
    trasform_train_path:str
    trasform_test_path:str

@dataclass
class ModelTrainerArtifact:
    model_path:str
    r2_train_score :float
    r2_test_score : float
@dataclass
class ModelEvaluationArtifact:
    is_model_accepted :bool
    improved_accurcy : float