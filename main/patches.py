import ast
from black import format


def load_ast_tree(file):
    """Loads file contents from files and parses the AST tree"""
    with open(file) as f:
        contents = f.read()
        return ast.parse(contents)


def write_ast_tree(file, tree):
    """Writes the ast tree generated python code back into the file"""
    with open(file, "w") as f:
        contents = ast.unparse(tree)
        format()
        f.write(contents)


def patch_module(module_path, title, use_makefile):
    """Applies some CTF related patches to the generated Django app"""

    def patch_file(submodule, patches, root=False):
        source_file = f"{module_path if root is False else 'ctf'}/{submodule}.py"
        tree = load_ast_tree(source_file)

        for patch in patches:
            tree = patch.visit(tree)

        tree = ast.fix_missing_locations(tree)
        write_ast_tree(source_file, tree)

    patch_file("apps", [AppsPatch(title, use_makefile)])
    patch_file("settings", [SettingsPatch()], True)


class AppsPatch(ast.NodeTransformer):
    """Adds some CTF specific fields to the create Django app config belonging to the task module."""

    def __init__(self, title, use_makefile) -> None:
        super().__init__()

        self.title = title
        self.use_makefile = use_makefile

    def visit_ClassDef(self, node: ast.ClassDef):
        # Creates the 'has_tasks' variable
        has_tasks = ast.Assign(
            targets=[ast.Name(id="has_tasks", ctx=ast.Store())],
            value=ast.Constant(value=True),
        )

        # Add the new field to the class
        node.body.append(has_tasks)

        # Creates the 'display_name' variable.
        display_name = ast.Assign(
            targets=[ast.Name(id="display_name", ctx=ast.Store())],
            value=ast.Constant(value=self.title),
        )

        # Add the new field to the class
        node.body.append(display_name)

        if self.use_makefile:
            # Creates the 'use_makefile' field if the module uses a makefile.
            use_makefile = ast.Assign(
                targets=[ast.Name(id="use_makefile", ctx=ast.Store())],
                value=ast.Constant(value=self.use_makefile),
            )

            # Add the new field to the class
            node.body.append(use_makefile)

        return node


class SettingsPatch(ast.NodeTransformer):
    def visit_Name(self, node: ast.Name):
        print(node.id)
        self.generic_visit(node)
        
        return node
