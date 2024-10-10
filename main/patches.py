import libcst as cst
from black import format_str, Mode


def load_cst(file) -> cst.BaseExpression:
    """Loads file contents from files and parses a CST"""
    with open(file) as f:
        contents = f.read()
        return cst.parse_module(contents)


def write_cst(file, tree):
    """Writes a CST generated python code back into the file"""
    with open(file, "w") as f:
        contents = tree.code
        contents = format_str(contents, mode=Mode())
        f.write(contents)


def patch_module(module_path, title, use_makefile):
    """Applies some CTF related patches to the generated Django app"""

    def patch_file(submodule, patches, root=False):
        source_file = f"{module_path if root is False else 'ctf'}/{submodule}.py"
        tree = load_cst(source_file)

        for patch in patches:
            tree = tree.visit(patch)

        write_cst(source_file, tree)

    patch_file("apps", [AppsPatch(title, use_makefile)])
    patch_file("views", [ViewsPatch()])
    patch_file("settings", [SettingsPatch(module_path)], True)


class ViewsPatch(cst.CSTTransformer):
    def leave_Module(self, original_node: cst.Module, update_node: cst.Module):
        import_statement = cst.parse_statement(
            "from main.decorators import define_task"
        )
        return update_node.with_changes(body=(*update_node.body, import_statement))


class AppsPatch(cst.CSTTransformer):
    """Adds some CTF specific fields to the create Django app config belonging to the task module."""

    def __init__(self, title, use_makefile) -> None:
        super().__init__()

        self.title = str(title)
        self.use_makefile = use_makefile

    def leave_ClassDef(self, original_node: cst.ClassDef, updated_node: cst.ClassDef):
        # Creates the 'has_tasks' variable
        has_tasks = cst.parse_statement(f"has_tasks = {True}")

        # Creates the 'display_name' variable.
        display_name = cst.parse_statement(f"display_name = '{self.title}'")

        # New variables to declare in class
        variables = [has_tasks, display_name]

        if self.use_makefile:
            # Creates the 'use_makefile' field if the module uses a makefile.
            use_makefile = cst.parse_statement(f"use_makefile = {True}")

            # Add the new field to the class
            variables.append(use_makefile)

        # Add variables to class definition.
        updated_body = updated_node.body.with_changes(
            body=(*original_node.body.body, *variables)
        )

        return updated_node.with_changes(body=updated_body)


class SettingsPatch(cst.CSTTransformer):
    def __init__(self, title):
        super().__init__()

        self.title = title

    def leave_Assign(self, original_node: cst.Assign, updated_node: cst.Assign):
        name = updated_node.targets[0].target.value

        if name == "INSTALLED_APPS":
            # Create new list item
            list_item = cst.Element(value=cst.parse_expression(f"'{self.title}'"))

            # Append new app to installed apps list.
            updated_list = updated_node.value.with_changes(
                elements=(*updated_node.value.elements, list_item)
            )

            return updated_node.with_changes(value=updated_list)
        else:
            return updated_node
