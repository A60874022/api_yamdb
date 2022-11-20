import os

from .conftest import MANAGE_PATH, project_dir_content

# проверяем, что в папки приложения api не находятся модели
api_path = os.path.join(MANAGE_PATH, 'api')
if 'api' in project_dir_content and os.path.isdir(api_path):
    api_dir_content = os.listdir(api_path)
    assert 'models.py' not in api_dir_content, (
        f'В директории `{api_path}` не должно быть файла с моделями. '
        'В этом приложении они не нужны.'
    )
else:
    assert False, f'Не найдено приложение `api` в папке {MANAGE_PATH}'
