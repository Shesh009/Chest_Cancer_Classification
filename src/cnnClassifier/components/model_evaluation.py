import tensorflow as tf
from pathlib import Path
import mlflow
import mlflow.keras
from urllib.parse import urlparse
from mlflow.models.signature import infer_signature
from cnnClassifier.entity.config_entity import EvaluationConfig
from cnnClassifier.utils.common import save_json

class Evaluation:
    def __init__(self,config:EvaluationConfig):
        self.config=config

    def _valid_generator(self):
        datagenerator_kwargs=dict(
            rescale=1./255,
            validation_split=0.25
        )

        dataflow_kwargs=dict(
            target_size=self.config.params_image_size[:-1],
            batch_size=self.config.params_batch_size,
            interpolation="bilinear"
        )

        valid_datagenerator=tf.keras.preprocessing.image.ImageDataGenerator(
            **datagenerator_kwargs
        )

        self._valid_generator=valid_datagenerator.flow_from_directory(
            directory=self.config.training_data,
            subset='validation',
            shuffle=False,
            **dataflow_kwargs
        )
    
    @staticmethod
    def load_model(path):
        return tf.keras.models.load_model(path)
    
    def evaluation(self):
        self.model=self.load_model(Path("model/model.h5"))
        self._valid_generator()
        self.score=self.model.evaluate(self._valid_generator)
        self.save_score()

    def save_score(self):
        scores={"loss":self.score[0],"accuracy":self.score[1]}
        save_json(path=Path("scores.json"),data=scores)

    def log_into_mlflow(self):
        mlflow.set_registry_uri(self.config.mlflow_uri)
        tracking_url_type_store=urlparse(mlflow.get_tracking_uri()).scheme

        sample_input = next(self._valid_generator)[0]
        signature = infer_signature(sample_input)

        with mlflow.start_run():
            mlflow.log_params(self.config.all_params)
            mlflow.log_metrics(
                {"loss":self.score[0],"accuracy":self.score[1]}
            )

            if tracking_url_type_store != "file":
                mlflow.keras.log_model(self.model, "model", registered_model_name="VGG16Model",signature=signature)
            else:
                mlflow.keras.log_model(self.model, "model", signature=signature)