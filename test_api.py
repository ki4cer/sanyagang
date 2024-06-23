import requests

base_url = 'http://localhost:5000'

def test_add_log():
    """Проверка добавления лога через POST-запрос."""
    response = requests.post(f"{base_url}/add_log", data={'log_level': 'INFO', 'message': 'Test log'})
    assert response.status_code == 200

def test_get_logs():
    """Проверка получения всех логов через GET-запрос."""
    response = requests.get(base_url)
    assert response.status_code == 200
    assert 'Test log' in response.text

def test_delete_log():
    """Проверка удаления лога."""
    log_id = 1
    response = requests.post(f"{base_url}/delete_log/{log_id}")
    assert response.status_code == 200

def test_filter_logs():
    """Проверка фильтрации логов."""
    response = requests.get(f"{base_url}/filter_logs", params={'log_level': 'INFO'})
    assert response.status_code == 200
    assert 'Test log' in response.text
