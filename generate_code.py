"""Module to generate code for az-cli-py."""

import os
import keyword
import shutil
import tooling


class Constants:
    """Static class for constants."""

    COMMAND_ROOT = "pyaz"  # the root name of the command path
    OUTPUT_DIR_NAME = "output"  # the name of the output folder for generating code
    UTILS_FILE_NAME = "pyaz_utils.py"  # the name of module with utilities


def pythonize_name(name: str) -> str:
    """
    Given a name, makes it pythonic.

    - removes leading dashes
    - replaces remaining dashes with underscores
    - checks for keywords and appends a trailing underscore
    """
    name = name.replace("--", "").replace("-", "_")
    if name in keyword.kwlist:
        name = name + "_"
    return name


def get_commands():
    """
    Return a dictionary with all the az cli commands.

    The dictionary is keyed by the path to the command
    inside each dictionary entry is another dictionary of verbs for that command
    with the command object (from cli core module) being stored in that.
    """
    # using Microsoft VSCode tooling module to load the az cli command table
    tooling.initialize()
    commands = tooling.load_command_table()

    command_dict = {}  # initialize empty dict for our return

    # iterate through the all the commands
    for command_name in commands:

        # get the command object
        command = commands[command_name]

        # split apart each command segment
        command_list = command_name.split(" ")

        # pythonize the names
        command_list = [pythonize_name(name) for name in command_list]

        # remove the last command which is the action verb
        command_verb = command_list.pop()

        # build path of commands prefixed by the command root (pyaz)
        command_path = os.path.join(Constants.COMMAND_ROOT, *command_list)

        # add command path to dictionary if not already there
        if command_path not in command_dict:
            command_dict[command_path] = {}

            # add a subcommands list object to store the sub commands for later use
            command_dict[command_path]["_subcommands"] = []

            # if this is a subcommand then add it to the subcommands list of the parent
            if command_path.count(os.path.sep) > 0:
                parent = os.path.dirname(command_path)

                # add command path to dictionary if not already there
                if parent not in command_dict:
                    command_dict[parent] = {}
                    command_dict[parent]["_subcommands"] = []
                command_dict[parent]["_subcommands"].append(
                    os.path.basename(command_path)
                )

        # add the command object to the dictionary using the path and verb as keys
        command_dict[command_path][command_verb] = command

    return command_dict


def generate_code(base_dir):
    """
    Generate code for pyaz from the az cli command table.

    Create a folder structure starting from the base_dir based on the hierarchy of
    the commands, with a folder for each command containing an __init__ module
    that contains the "verb" functions (if any) associated with that command
    """
    commands = get_commands()

    for command_path, command_group in commands.items():
        print(f"generating code module for: {command_path}")

        # translate the command back into the az syntax so that we can use it to get help
        az_command = command_path.split(os.path.sep)
        az_command.pop(0)
        az_command = " ".join(az_command)

        # get the help for the module
        module_summary = None
        module_help = tooling.get_help(az_command)
        if module_help:
            module_summary = module_help.get("short-summary", None)

        # get the module path and create it if it doesn't exist
        module_dir = os.path.join(base_dir, command_path)
        os.makedirs(name=module_dir, exist_ok=True)

        # create the module __init__ file that will contain the verb functions
        with open(f"{module_dir}/__init__.py", mode="w", encoding="utf-8") as file:

            # add help to the top of the module
            if module_summary:
                file.write(f"'''\n{module_summary}\n'''\n")

            # get the level of depth for this command based on the path separator
            # add one so that the top-most is level 1
            command_depth = command_path.count(os.path.sep) + 1

            # create import_dots to represent level of depth for importing the pyaz_utils
            import_dots = "." * command_depth

            # write the imports to the top of each module
            # f.write("import json, subprocess\n")
            file.write(f"from {import_dots} pyaz_utils import _call_az\n")

            # build list of subcommands and add import statement
            subcommands = command_group["_subcommands"]
            if len(subcommands) > 0:
                file.write(f'from . import {", ".join(sorted(subcommands))}\n\n')

            # del the subcommands list as it is no longer needed
            del command_group["_subcommands"]

            # for each command verb write a function with a boiler plate format
            for command_verb, command in command_group.items():

                # placeholder list for the output arguments
                required_args = []
                optional_args = []
                required_arg_names = []
                optional_arg_names = []

                # get the command object from the command table
                #command = commands[command_path][command_verb]

                # get the dictionary of arguments for the command
                arguments = tooling.get_arguments(command)

                # loop through each argument in the arguments dictionary
                for argument in arguments:

                    # get the argument object
                    arg = arguments[argument]

                    # create instance of Argument class
                    output_arg = Argument()

                    # get the options_list which is the options for this argument in the format:
                    # ['--resource-group', '-g']
                    options_list = arg.type.settings.get("options_list", [])

                    # if there are options then derive the argument name from the options
                    if len(options_list) > 0:

                        # remove any non strings from options_list
                        # when testing, found one option with an object of type
                        # knack.deprecation.Deprecated object
                        options_list = [
                            option for option in options_list if isinstance(option, str)
                        ]

                        # get the first option from the options list as that is the one we want
                        # the second option is the shorter one
                        # and pythonize the name of the argument
                        name = pythonize_name(options_list[0])

                        if not name.startswith("_") and name not in ["__cmd__", "cmd"]:

                            output_arg.name = name

                            # get the argument's help text
                            output_arg.help = arg.type.settings.get("help", None)

                            # get the argument's default value
                            output_arg.default = arg.type.settings.get("default", None)

                            # get whether the argument is required
                            output_arg.required = arg.type.settings.get(
                                "required", False
                            )

                            if output_arg.required:
                                required_arg_names.append(output_arg.formatted_name())
                                required_args.append(output_arg)
                            else:
                                optional_arg_names.append(output_arg.formatted_name())
                                optional_args.append(output_arg)

                # sort args by name
                required_args = sorted(required_args, key=lambda arg: arg.name)
                optional_args = sorted(optional_args, key=lambda arg: arg.name)

                # build final list of args from sorted required and optional args
                required_args_formatted = ", ".join(sorted(required_arg_names))
                optional_args_formatted = ", ".join(sorted(optional_arg_names))

                if required_args and optional_args:
                    arguments_formatted = (
                        required_args_formatted + ", " + optional_args_formatted
                    )
                elif required_args:
                    arguments_formatted = required_args_formatted
                else:
                    arguments_formatted = optional_args_formatted

                # get help for commmand
                command_help = tooling.get_help(command.name)
                if command_help:
                    short_summary = command_help.get("short-summary", "")
                else:
                    short_summary = ""

                function_doc = short_summary

                # combine with arguments
                # required_args_doc = ""
                # if len(required_args) > 0:
                #    for arg in required_args:
                #        required_args_doc = required_args_doc.
                if len(required_args) > 0:
                    required_args_doc = "\n\n    Required Parameters:\n"
                    required_args_doc += "\n".join(
                        [f"    - {arg.name} -- {arg.help}" for arg in required_args]
                    )
                    function_doc += required_args_doc

                if len(optional_args) > 0:
                    optional_args_doc = "\n\n    Optional Parameters:\n"
                    optional_args_doc += "\n".join(
                        [f"    - {arg.name} -- {arg.help}" for arg in optional_args]
                    )
                    function_doc += optional_args_doc

                # write the command verb's function body using the parts
                # to the command's __init__ module
                # if help summary then include that
                function_def = _get_az_function_def(
                    command.name, command_verb, arguments_formatted, function_doc
                )
                file.write(function_def)


def _get_az_function_def(full_command, command_verb, arguments, command_doc):
    """Given a function name, arguments, and doc,returns a formatted string function def."""
    if command_doc:
        function_def = f"""
def {command_verb}({arguments}):
    '''
    {command_doc}
    '''
    return _call_az("az {full_command}", locals())

"""
    else:
        function_def = f"""
def {command_verb}({arguments}):
    return _call_az("az {full_command}", locals())

"""
    return function_def


class Argument:
    """Represents an argument to a command."""

    name = ""
    help = None
    required = False
    default = None

    def formatted_name(self):
        """Return a formatted argument name."""
        if self.required:
            return self.name
        else:
            return self.name + "=None"


if __name__ == "__main__":
    # get path to the current file's directory
    current_dir = os.path.dirname(os.path.realpath(__file__))

    # set up test dir where to create code
    output_dir = os.path.join(current_dir, Constants.OUTPUT_DIR_NAME)

    # call function to generate the code in the test dir
    generate_code(output_dir)

    # copy the utilities module into the output directory
    source_file = os.path.join(current_dir, Constants.UTILS_FILE_NAME)
    target_file = os.path.join(
        output_dir, Constants.COMMAND_ROOT, Constants.UTILS_FILE_NAME
    )
    shutil.copy(source_file, target_file)
