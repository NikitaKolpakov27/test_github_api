import os
import time

import requests
from github import Github
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv('./.env')

personal_access_token = os.getenv('GITHUB_PERSONAL_TOKEN')
username = os.getenv('GITHUB_USERNAME')
repo_name = os.getenv('NEW_REPOSITORY')

# Получение всех публичных репозиториев пользователя
def get_user_repos():
    global username

    g = Github()
    user = g.get_user(username)

    return list(user.get_repos())


# Проверка, что репозиторий с заданным именем, присутствует в общем списке репозиториев пользователя
def is_repo_exists(r_name):

    repo_list = get_user_repos()
    for r in repo_list:

        if r.name == r_name:
            return True

    return False

# Создание репозитория
def make_new_repo():
    global personal_access_token
    global repo_name

    api_base_url = "https://api.github.com"
    headers = {'Accept': 'application/vnd.github.v3+json',
               'Authorization': 'token {}'.format(personal_access_token)}

    data = {
        "name": repo_name,
        "private": False
    }
    response = requests.post(f"{api_base_url}/user/repos", json=data, headers=headers)

    print(response.status_code)

# Удаление репозитория
def remove_repo():
    global personal_access_token
    global repo_name

    api_base_url = "https://api.github.com"
    headers = {'Accept': 'application/vnd.github.v3+json',
               'Authorization': 'token {}'.format(personal_access_token)}

    response = requests.delete(
        '{}/repos/{}/{}/?access_token={}'.format(api_base_url, username, repo_name, personal_access_token), headers=headers
    )

    print(response.status_code)


if __name__ == "__main__":

    # Проверяем, что репозитория с таким именем изначально в списке не было
    if not is_repo_exists(repo_name):

        # Создаем новый репозиторий
        make_new_repo()

        # Проверяем, появился ли он в общем списке
        if is_repo_exists(repo_name):

            # Удаляем его
            remove_repo()

            # В завершение проверяем, что удаление прошло успешно (репозитория нет в списке)
            if not is_repo_exists(repo_name):
                print("Тестирование прошло успешно")


