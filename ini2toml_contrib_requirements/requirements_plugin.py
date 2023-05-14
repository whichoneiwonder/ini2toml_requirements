# import ini2toml.types
# import ini2toml.translator

from functools import partial

from ini2toml.types import Translator, Profile, IntermediateRepr as M, CommentedList
HELP_TEXT = """
Turns a requirements file into pyproject.toml [project.dependencies] section
"""
NAME = "requirements.txt"


def activate(translator: Translator):
    profile: Profile = translator[NAME]  # profile.name will be ``setup.cfg``
    # translator["*requirements.txt]
    profile.description = HELP_TEXT
    plugin = RequirementsPlugin()

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
        output = """
        [project.dependencie]
        """
        output = ""
        cont = False
        for line in text.splitlines(keepends=False):
            if not cont:
                pass
                # output += '['
            cont = line.endswith("\\")
            output += "   " + line
            if not cont:
                output += '\n'
        return output

    def intermediate(self, data: M) -> M:
        "Assume is a list"
        if not isinstance(data, (list, CommentedList)):
            ...
        result = M(
            elements={"project": {"dependencies": data}},
            inline_comment="From requirements.txt"
        )
        return result