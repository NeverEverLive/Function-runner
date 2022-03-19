from fastapi import FastAPI
from subprocess import run
from pydantic import BaseModel
from typing import Any, List
from sys import executable

app = FastAPI()


class Solution(BaseModel):
    code: str
    args: List[Any]


@app.post('/execute')
def execute_code(solution: Solution):
    code = solution.code
    args = solution.args
    output = []
    for arg in args:
        if isinstance(arg,list):
            arg = list(map(str, arg))
            input_ = " ".join(arg)
        else:
            input_ = arg    
            
        execute_results = run([executable, "-c", code], input=input_, capture_output=True, text=True, check=True)
        output.append(execute_results.stdout)

    return {"output": output}
