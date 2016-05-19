import json
from jinja2 import Template
from ansi2html import Ansi2HTMLConverter
from ansi2html.style import get_styles


conv = Ansi2HTMLConverter()

def shell_to_html(shell):
    return conv.convert(shell, False)


if __name__ == '__main__':
    result = Template(open("template.html", "r").read()).render(data=json.load(open("./logs.json")), convert=shell_to_html, shell_css="\n".join(map(str, get_styles(conv.dark_bg, conv.scheme))))
    open("index.html", "w").write(result.encode("Utf-8"))
