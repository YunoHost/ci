import json
from jinja2 import Template


if __name__ == '__main__':
    result = Template(open("template.html", "r").read()).render(data=json.load(open("./logs.json")))
    open("index.html", "w").write(result)
