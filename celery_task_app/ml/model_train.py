import joblib
import os
import pandas as pd
# import time

MODEL_PATH = '/home/toan/ainocode-project/project-v1/ServingMLFastCelery/celery_task_app/ml/churn_pipeline.pkl'


class ClassificationModel:

    """ Wrapper for loading and serving pre-trained model"""

    def __init__(self):
        self.model = self._load_model_from_path(MODEL_PATH)

    @staticmethod
    def _load_model_from_path(path):
        model = joblib.load(path)
        return model

    def multitask_s3_bucket(path_file, name_project, key, option):
        session = create_session("us-east-1")
        s3 = session.client("s3")
        if option == "uploadfile":
            s3.upload_file(Filename=path_file, Bucket=name_project, Key=key)
        elif option == "downloadfile":
            s3.download_file(name_project, key, path_file)

    # model anh Thinh dua vao
    def mode_A():
        pass

    def train(self, data):
        """
        Make batch prediction on list of preprocessed feature dicts.
        Returns class probabilities if 'return_options' is 'Prob', otherwise returns class membership predictions
        """
        # multitask_s3_bucket('.', data["bucket_name"], data["key"], option="downloadfile")
        # df_train = pd.read_csv(data["file_name"]+".csv")

        # classifier = mode_A()
        # joblib.dump(nb_classifier, 'classifier.pkl')

        key_pkl = "/model-training-pkl/" + 'classifier.pkl'
        print(key_pkl)
        # multitask_s3_bucket('classifier.pkl', data["bucket_name"], key_pkl, option="uploadfile")
        
        return  {"bucket_name": data["bucket_name"], "key": key_pkl}