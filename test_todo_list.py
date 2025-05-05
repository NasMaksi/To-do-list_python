import os
import json
import pytest
from unittest.mock import patch, mock_open, MagicMock
import todo_list


@pytest.fixture
def mock_file():
    return mock_open(read_data=json.dumps([]))


@pytest.fixture
def mock_io(monkeypatch):
    mock_input = MagicMock()
    mock_print = MagicMock()
    monkeypatch.setattr('todo_list.get_input', mock_input)
    monkeypatch.setattr('todo_list.show_output', mock_print)
    return mock_input, mock_print


@pytest.fixture
def temp_file(tmp_path):
    def _create(content):
        file_path = tmp_path / "test_tasks.json"
        file_path.write_text(json.dumps(content), encoding='utf-8')
        return file_path

    return _create


class TestFileOperations:
    def test_load_empty_tasks(self, mock_file, monkeypatch):
        monkeypatch.setattr('todo_list.FILE_NAME', 'test.json')
        with patch('builtins.open', mock_file):
            tasks = todo_list.load_tasks()
            assert tasks == []

    def test_save_tasks(self, temp_file, monkeypatch):
        test_data = [{"task": "Test", "done": False}]
        file_path = temp_file([])
        monkeypatch.setattr('todo_list.FILE_NAME', str(file_path))

        todo_list.save_tasks(test_data)

        with open(file_path, 'r', encoding='utf-8') as f:
            saved = json.load(f)
            assert saved == test_data


class TestUserInteraction:
    def test_add_task(self, mock_io):
        mock_input, mock_print = mock_io
        mock_input.return_value = "New task"
        tasks = []

        todo_list.add_task(tasks)

        assert len(tasks) == 1
        assert tasks[0]["task"] == "New task"
        mock_print.assert_called_with("Задача добавлена!")

    def test_mark_done_valid(self, mock_io):
        mock_input, mock_print = mock_io
        mock_input.return_value = "1"
        tasks = [{"task": "Task", "done": False}]

        todo_list.mark_done(tasks)
        assert tasks[0]["done"] is True
        mock_print.assert_called_with("Задача отмечена выполненной!")

    def test_delete_task(self, mock_io):
        mock_input, mock_print = mock_io
        mock_input.return_value = "1"
        tasks = [{"task": "Delete me", "done": False}]

        todo_list.delete_task(tasks)
        assert len(tasks) == 0
        mock_print.assert_called_with("Задача 'Delete me' удалена!")


if __name__ == "__main__":
    pytest.main(["-v", os.path.abspath(__file__)])