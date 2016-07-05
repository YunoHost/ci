import os
import json
from urllib import urlretrieve


def argument_for_question(question):
    question_type = question.get("type")

    if question_type is None and question.get("choices"):
        question_type = "boolean"
    elif question_type is None and question.get("default"):
        question_type = "with_default"
    elif question_type is None and question["name"] == "admin":
        question_type = "user"
    elif question_type is None and question["name"] == "domain":
        question_type = "domain"

    if question_type == "domain":
        return (question["name"], "ynh.local")
    elif question_type in ("path", "with_default"):
        return (question["name"], question["default"])
    elif question_type == "boolean":
        if isinstance(question["default"], bool):
            if question["default"]:
                question["default"] = "Yes"
            else:
                question["default"] = "No"

        return (question["name"], question["default"])
    elif question_type == "password":
        return (question["name"], "ynh")
    elif question_type == "user":
        return (question["name"], "johndoe")
    else:
        raise Exception("Unknow question type: %s\n" % question_type, question)

def default_arguments_for_app(app_data):
    answers = []
    for question in app_data["manifest"]["arguments"]["install"]:
        answers.append(argument_for_question(question))

    return "&".join(["=".join([x[0], x[1]]) for x in answers])


def main():
    if not os.path.exists("/tmp/yunohost_official_apps_list.json"):
        urlretrieve("https://app.yunohost.org/official.json", "/tmp/yunohost_official_apps_list.json")

    app_list = json.load(open("/tmp/yunohost_official_apps_list.json"))

    for name, data in sorted(app_list.items(), key=lambda x: x[0]):
        print "%s:" % name, default_arguments_for_app(data)


if __name__ == '__main__':
    main()
