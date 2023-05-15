# import ini2toml.types
# import ini2toml.translator

from functools import partial
from os import linesep
from typing import Dict, List, TypeVar
from ini2toml.types import Translator, Profile, IntermediateRepr as M, CommentedList

_T = TypeVar("_T")


def activate(translator: Translator):
    for plugin in (RequirementsPlugin(), ExtraRequirementsPlugin()):
        profile: Profile = translator[plugin.NAME]
        profile.help_text = plugin.HELP_TEXT
        profile.name = plugin.NAME

        profile.pre_processors.append(plugin.pre_processing)
        profile.intermediate_processors.append(plugin.intermediate)


class RequirementsPlugin:
    """
    A plugin profile to import requirements.txt or *-requirements.txt files
    """

    HELP_TEXT = """
    Turns a requirements file into pyproject.toml [project.dependencies] section
    """
    NAME = "requirements.txt"

    def pre_processing(self, text: str) -> str:
        "Take the raw requirements file and pretend it is"

        output = f"""[dependencies]{linesep}"""
        accum: List[str] = []
        num = 0
        for line in text.splitlines(keepends=False):
            if line.endswith("\\"):
                accum += line
                continue
            newline = " ".join([*accum, line])
            output += f"{num}={newline}{linesep}"
            accum = []
            num += 1

        if accum:
            output += f"{num}=" + " ".join(accum) + linesep
        print("after_pre_processing:", output, sep=linesep)
        return output

    def intermediate(self, data: M) -> M:
        "Assume is a list"
        if not isinstance(data, (list, CommentedList)):
            ...

        listified = CommentedList(data.get("dependencies", M()).values())
        elements = self.get_deps_position(listified)
        result = M(elements=elements, inline_comment="From requirements.txt")

        return result

    def get_deps_position(self, data: M) -> M:
        return M({"project": {"dependencies": data}})


class ExtraRequirementsPlugin(RequirementsPlugin):
    """
    A plugin profile to import *-requirements.txt files
    that represent optional-dependencies
    """

    NAME = "extra-requirements.txt"

    def get_deps_position(self, data: M) -> M:
        return M({"project": {"optional-dependencies": {"Extras": data}}})
