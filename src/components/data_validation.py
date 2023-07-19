from src.components.data_ingestion import DataIngestionArtifact

@dataclass
class DataValidationConfig:
    valid_data_file_path: str
    invalid_data_file_path: str

class DataValidationArtifact:
    validation-status:bool
    valid_train_file_path:str
    valid_test_file_path:str
    invalid_train_file_path:str
    invalid_test_file_path:str
    drift_report_file_path:str


class DataValidation:
    def __init__(self, data_ingestion_artifact:DataIngestionArtifact)
        self.data_ingestion_artifact = data_ingestion_artifact
        timestamp = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
        #self.valid_data_file_path = os.path.join("artifact",timestamp, "validation","")
