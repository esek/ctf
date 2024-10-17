import ast


def load_ast_tree(file):
    """Loads file contents from files and parses the AST tree"""
    with open(file) as f:
        contents = f.read()
        return ast.parse(contents)


def write_ast_tree(file, tree):
    """Writes the ast tree generated python code back into the file"""
    with open(file, "w") as f:
        contents = ast.unparse(tree)
        f.write(contents)


def patch_module(module_path, title, use_makefile):
    """Applies some CTF related patches to the generated Django app"""
    apps_file = f"{module_path}/apps.py"
    tree = load_ast_tree(apps_file)

    tree = AppsPatch(title, use_makefile).visit(tree)
    tree = ast.fix_missing_locations(tree)

    write_ast_tree(apps_file, tree)


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
