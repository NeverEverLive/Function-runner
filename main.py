from fastapi import FastAPI
from datetime import date
from os import path, mkdir
from subprocess import run
from pydantic import BaseModel
from typing import Any, List
from sys import executable

app = FastAPI()
base_dir = '~/Data/Python/micro_service_function_runner'
static_dir = base_dir + '/static'


class Function(BaseModel):
    name: str
    user_solution: str
    owner_solution: str
    user: str
    args: List[Any]


files={}


class FunctionResponse(BaseModel):
    user_result: List[Any]
    owner_result: List[Any]


@app.post('/process_function')
def process_function(function: Function): # , *args

    file_name = str(date.today())+ '~' + function.user + '.py'
    directory_path = f'{static_dir}/{function.name}'
    file_path = f'{directory_path}/{file_name}'

    if not path.exists(f'../static/{function.name}'):
        mkdir(f'../static/{function.name}')
    
    with open(f'../static/{function.name}/{file_name}', mode='w+') as file:
        file.write(function.user_solution)

    if not path.exists(f'../static/{function.name}/{file_name}'):
        raise FileExistsError('File not exist')
    
    with open(f'../static/{function.name}/solution.py', mode='w+') as file:
        file.write(function.owner_solution)

    if not path.exists(f'../static/{function.name}/solution.py'):
        raise FileExistsError('File not exist')

    
    owner_results = []
    user_results = []
    for argument in function.args:
        input_argument = f'{argument}'
        user_result = run([executable, "-c", function.user_solution], input=input_argument, capture_output=True, text=True, check=True)
        owner_result = run([executable, "-c", function.owner_solution], input=input_argument, capture_output=True, text=True, check=True)
        
        print(argument)

        user_results.append(user_result)
        owner_results.append(owner_result)

        if user_result.stdout != owner_result.stdout:
            return False
    
    return True
