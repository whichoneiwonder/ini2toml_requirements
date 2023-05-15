import unittest
from ini2toml import api, errors, types
from tomli import loads as toml_loads

# from ini2toml.drivers.lite_toml import
from ini2toml_contrib_requirements.requirements_plugin import (
    activate,
    RequirementsPlugin,
    ExtraRequirementsPlugin,
    linesep,
)


class SimpleTestCases(unittest.TestCase):
    def test_empty(self):
        test_t = api.Translator()
        # activate(test_t)
        empty = test_t.translate(
            ini=f"test{linesep}", profile_name=RequirementsPlugin.NAME
        )
        print("toml_out:", empty, sep="\n")
        reloaded = toml_loads(empty)
        self.assertIn("project", reloaded)
        project = reloaded["project"]
        print(project)
        self.assertIn("dependencies", project)
        self.assertIn("test", project["dependencies"])
