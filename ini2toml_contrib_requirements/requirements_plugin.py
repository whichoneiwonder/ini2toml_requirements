# import ini2toml.types
# import ini2toml.translator

from functools import partial
from os import linesep
from typing import Dict, TypeVar
from ini2toml.types import Translator, Profile, IntermediateRepr as M, CommentedList
_T = TypeVar("_T")
HELP_TEXT = """
Turns a requirements file into pyproject.toml [project.dependencies] section
"""
NAME = "requirements.txt"


def activate(translator: Translator):
    profile: Profile = translator[NAME]  # profile.name will be ``requirements.txt``
    # translator["*requirements.txt]
    profile.description = HELP_TEXT
    plugin = ExtraRequirementsPlugin()

    # print(dir(profile))
    profile.pre_processors.append(plugin.pre_processing)
    profile.intermediate_processors.append(plugin.intermediate)
    

class RequirementsPlugin:
    """
    A plugin profile to import requirements.txt or *-requirements.txt files
    """

    def pre_processing(self, text: str) -> str:
        "Take the raw requirements file and pretend it is "
        print(text)
        output = """[project:dependencies]\n"""
        accum = []
        num = 0
        for line in text.splitlines(keepends=False):
            if line.endswith("\\"):
                accum += line
                continue
            newline = " ".join([*accum, line])
            output += f'{num}={newline}{linesep}' 
            accum = []
            num += 1

        if accum:
            output +=  f"{num}=" + " ".join(accum) + linesep
        return output

    def intermediate(self, data: M) -> M:
        "Assume is a list"
        if not isinstance(data, (list, CommentedList)):
            ...
        listified = list(data["project:dependencies"].values())
        elements = self.get_deps_position(listified)        
        result = M(
            elements=elements,
            inline_comment="From requirements.txt"
        )
        return result
    
    def get_deps_position(self, data: _T) -> Dict[str, Dict[str, _T]]:
        return {"project": {"dependencies": data}}


class ExtraRequirementsPlugin(RequirementsPlugin):
    """
    A plugin profile to import requirements.txt or *-requirements.txt files
    """

    def get_deps_position(self, data: _T) -> Dict[str, Dict[str, _T]]:
        return {"project": {"optional-dependencies": {"Extras": data}}}
    
