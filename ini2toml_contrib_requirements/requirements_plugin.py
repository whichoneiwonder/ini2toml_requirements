# import ini2toml.types
# import ini2toml.translator

from functools import partial
from os import linesep
from typing import Dict, List, TypeVar
from ini2toml.types import (
    Translator,
    Profile,
    IntermediateRepr as M,
    CommentedList,
    CommentedKV,
    Commented,
)
from ini2toml.transformations import split_comment

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
            if not line.strip():
                continue

            outline = " ".join([*accum, line])
            if outline.strip().startswith("#"):
                # this is a comment
                output += outline + linesep
            else:
                output += f"key_{num}={outline}{linesep}"
            accum = []
            num += 1

        if accum:
            # leftover line at end of file
            output += f"key_{num}=" + " ".join(accum) + linesep
        return output

    def intermediate(self, data: M) -> M:
        "Assume is a list"
        if not isinstance(data, (list, CommentedList)):
            p_rint("Inter Repr is ", type(data))
        # if isinstance(data, str):
        #     req, comment = data.split("#")
        #     return Commented(req.strip(), comment)

        section: M = data.get("dependencies", M())
        listified: CommentedList[str] = CommentedList()
        headline_comment = data.inline_comment

        p_rint("dependencies Repr is ", section, sep='\n')
        for _key, val in section.items():
            p_rint(_key, val)
            listified.append(split_comment(val))
        # for row in listified:
            # row.
        p_rint(listified)
        # .values())
        elements = self.get_deps_position(listified)
        result = M(elements=elements, inline_comment="From requirements.txt")
        p_rint(result)
        return result

    def get_deps_position(self, data: M) -> M:
        return M(project=M(dependencies=[*data]))


class ExtraRequirementsPlugin(RequirementsPlugin):
    """
    A plugin profile to import *-requirements.txt files
    that represent optional-dependencies
    """

    NAME = "extra-requirements.txt"

    def get_deps_position(self, data: M) -> M:
        return M({"project": {"optional-dependencies": {"Extras": [*data]}}})


def p_rint(*data, sep=' ', **kwargs):
    if True:
        print(*data, sep=sep, **kwargs)