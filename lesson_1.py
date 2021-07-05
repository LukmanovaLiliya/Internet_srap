import requests

import json


def repo_list(users):
    url = "https://api.github.com/users/" + users + "/repos"
    rep = requests.get(url).json()
    return rep


def write_f(path, rep):
    with open(path, "w") as f:
        json.dump(rep, f)


def read_f(path):
    with open(path, "r") as f:
        json_rep = json.load(f)
    return json_rep


if __name__ == "__main__":
    user = "LukmanovaLiliya"
    write_f("repo.json", repo_list(user))
    print("Список репозиториев пользователя " + user + ":")
    for i in read_f("repo.json"):
        print(i["name"])