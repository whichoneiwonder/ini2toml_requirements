import unittest
from ini2toml import api, errors, types
from tomli import loads as toml_loads
from pathlib import Path

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
            ini=f"test{linesep}", profile_name=ExtraRequirementsPlugin.NAME
        )
        print("toml_out:", empty, sep="\n")
        reloaded = toml_loads(empty)
        self.assertIn("project", reloaded)
        project = reloaded["project"]
        print(project)
        self.assertIn("optional-dependencies", project)
        self.assertIn("Extras", project["optional-dependencies"])
        self.assertEqual(["test"], project["optional-dependencies"]["Extras"])

    def test_inline_comment(self):
        comment_file = Path(__file__).parent / "testdata" / "comment_2.txt"
        with comment_file.open() as reqfile:
            req_content = reqfile.read()
        t = api.Translator()
        pre_func = t.profiles[RequirementsPlugin.NAME].pre_processors[0]
        intermediate_text = pre_func(req_content)
        self.assertIn("# comment", intermediate_text)

        output = api.Translator().translate(req_content, RequirementsPlugin.NAME)
        print("datas", output, sep='\n')
        self.assertIn("# comment", output)


    def test_big_file(self):
        comment_file = Path(__file__).parent / "testdata" / "rtfd_requirements.txt"
        with comment_file.open() as reqfile:
            req_content = reqfile.read()
        t = api.Translator()
        pre_func = t.profiles[RequirementsPlugin.NAME].pre_processors[0]
        intermediate_text = pre_func(req_content)
        # self.assertIn("# comment", intermediate_text)

        output = api.Translator().translate(req_content, RequirementsPlugin.NAME)
        print("datas", output, sep='\n')
        self.assertIn("# comment", output)
