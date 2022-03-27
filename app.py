from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from celery.result import AsyncResult

import boto3
import time
import aiofiles

from celery_task_app.tasks import train_model_classification
from models import Task, Prediction, ParamsPredict

app = FastAPI()

def create_session(regions):
    load_dotenv('.env')
    AWS_ACCESS_KEY=os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_KEY=os.getenv("AWS_SECRET_ACCESS_KEY")
    session = boto3.Session(
        aws_access_key_id = AWS_ACCESS_KEY, 
        aws_secret_access_key = AWS_SECRET_KEY,
        region_name = regions
    )
    return session

def multitask_s3_bucket(path_file, name_project, key, option):
    session = create_session("us-east-1")
    s3 = session.client("s3")
    if option == "uploadfile":
        s3.upload_file(Filename=path_file, Bucket=name_project, Key=key)
    elif option == "downloadfile":
        s3.download_file(name_project, key, path_file)

'''
============TRAINING ROUTE===========
'''
@app.post('/classification/train', response_model=Task, status_code=202)
async def training(project_name=Form(...), csv_file: UploadFile = File(...)):
    path_file= './' + csv_file.filename
    key = '/trainig-folder/' + time.ctime() + '-' + csv_file.filename + '.csv'
    # multitask_s3_bucket(path_file, project_name, key, option="uploadfile")

    async with aiofiles.open(csv_file.filename, 'wb') as out_file:
        content = await csv_file.read()  # async read
        await out_file.write(content)  # async write

    data = {"bucket_name": project_name, "key": key, "file_name": csv_file.filename}

    task_id = train_model_classification.delay(data)

    data_response = {"task_id": str(task_id), "status": "processing"}
    return data_response

@app.get('/classification/training-result/{task_id}', response_model=Prediction, status_code=200, responses={202: {'model': Task, 'description': 'Accepted: Not Ready'}})
async def training_result(task_id):
    """Fetch result for given task_id"""
    task = AsyncResult(task_id)
    print(task)
    if not task.ready():
        # print(app.url_path_for('classification'))
        return JSONResponse(status_code=202, content={'task_id': str(task_id), 'status': 'Processing'})
    result = task.get()
    return {'task_id': task_id, 'status': 'Success', 'probability': str(result)}


# @app.post('/classification/predict/real-time', params_predict: ParamsPredict)
# async def predict_real_time():
    