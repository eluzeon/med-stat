import os

import settings


def make_path(base: str, *paths: str) -> str:
    """ Создает папки если они не существуют """
    path = os.path.join(base, *paths)
    os.makedirs(path, exist_ok=True)
    return path


def resolve_path(path: str) -> str:
    """
    Функция которая позволяет указывать @ - как абсолютный пусть до корня проекта, напр
    если проект лежит в /Users/me/work/project

    >>> resolve_path('@/my/path')
    '/Users/me/work/project/my/path'
    """
    if path.startswith("@/"):
        # @ - шорт для корня проекта
        path = path.replace('@', settings.PROJECT_DIR, 1)
    return path
