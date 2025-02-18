from markdown import Markdown
from markdown.preprocessors import Preprocessor
from markdown.extensions import Extension
import re


class StaticPathPreprocessor(Preprocessor):
    """
    Markdown extension that adjusts the static path for images referenced
    to match the common shared static endpoint.
    """

    def run(self, lines: list[str]) -> list[str]:
        processed_lines = []

        for line in lines:
            # Find any line that contains a path reference to static file.
            match = re.search("static\/", line)

            if match is not None:
                index = match.start()
                # Change it to an absolute path.
                patched = line[:index] + "/" + line[index:]
                processed_lines.append(patched)
            else:
                processed_lines.append(line)

        return processed_lines


class CTFExtension(Extension):
    """Contains markdown extensions related to the CTF project"""

    def extendMarkdown(self, md: Markdown) -> None:
        md.preprocessors.register(StaticPathPreprocessor(md.parser), "static-path", 175)
