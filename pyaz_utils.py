"""
Utility functions for the pyaz generated code to use
"""
import json
import subprocess
from typing import Dict

def call_az(command: str, parameters: Dict) -> object:
    """
    Runs an az command (supplied as a string, and parameters as dictionary) 
    Calls az cli via a subprocess
    Returns the az cli json converted to python object
    
    Example:
    `
    call_az("az group create", locals())
    `
    """
    params = _get_params(parameters)
    commands = command.split()
    commands.extend(params)
    full_command = " ".join(commands)
    print(f"Executing command: {full_command}")
    output = subprocess.run(commands, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout = output.stdout.decode("utf-8")
    stderr = output.stderr.decode("utf-8")
    if stdout:
        return json.loads(stdout)
        print(stdout)
    elif stderr:
        raise Exception(stderr)
        print(stderr)  
    

def _get_cli_name(name: str) -> str:
    """
    converts name back to cli format from pythonic version
    - strips trailing underscore from keywords
    - converts remaining underscores to dashes
    - adds leading dashes
    """
    if name[-1] == "_":
        name = name[0:-1]
    name = name.replace("_","-")
    name = f"--{name}"
    return name

def _get_params(locals: Dict) -> str:
    """
    given the built-in locals dictionary returns a formatted string
    with the az cli formatted parameter names and values in a comma-separated list
    """
    #return params
    output = []
    
    # loop through locals and append list of parameters and their values
    # as long as the parameter has a value
    for param in locals:
        if locals[param]:
            
            # if value is a boolean then don't append value, just param, used for flags
            if type(locals[param]) == bool:
                output.append(_get_cli_name(param))
            else:
                output.append(_get_cli_name(param))
                output.append(locals[param])    
    
    return output
