import unittest
from log_collector import LogCollector

class TestLogCollector(unittest.TestCase):
    def setUp(self):
        # Используем in-memory БД для тестов
        self.log_collector = LogCollector(':memory:')
        # Подготовка данных для тестов
        self.log_collector.add_log('INFO', 'First info log.')
        self.log_collector.add_log('ERROR', 'First error log.')
        self.log_collector.add_log('WARNING', 'First warning log.')

    def test_filter_logs_by_level(self):
        # Тестирование фильтрации по уровню лога
        logs = self.log_collector.filter_logs('ERROR', None, None)
        self.assertEqual(len(logs), 1)
        self.assertEqual(logs[0][2], 'ERROR')

    def test_filter_logs_by_dates(self):
        # Тестирование фильтрации по датам
        from datetime import datetime, timedelta
        today = datetime.now().isoformat()
        yesterday = (datetime.now() - timedelta(days=1)).isoformat()
        logs = self.log_collector.filter_logs(None, yesterday, today)
        self.assertEqual(len(logs), 3)  # Проверяем, что вернулись все сегодняшние логи

    def test_filter_logs_by_level_and_dates(self):
        # Тестирование комбинированной фильтрации
        from datetime import datetime, timedelta
        today = datetime.now().isoformat()
        yesterday = (datetime.now() - timedelta(days=1)).isoformat()
        logs = self.log_collector.filter_logs('INFO', yesterday, today)
        self.assertEqual(len(logs), 1)
        self.assertEqual(logs[0][2], 'INFO')

    def test_add_and_get_logs(self):
        # Базовый тест на добавление и получение логов
        self.log_collector.add_log('INFO', 'This is a test log.')
        logs = self.log_collector.get_logs()
        self.assertEqual(len(logs), 4)  # Должны быть 4 лога, т.к. 3 добавлено в setUp
        self.assertEqual(logs[0][2], 'INFO')
        self.assertEqual(logs[0][3], 'This is a test log.')

if __name__ == '__main__':
    unittest.main()
