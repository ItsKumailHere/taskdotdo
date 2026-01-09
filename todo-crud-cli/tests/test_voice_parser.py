"""
Tests for voice command parser.
Tests various natural language phrasings to ensure robust keyword extraction.
"""
import pytest
from todo_cli.command_parser import parse_voice_command


class TestListCommands:
    """Tests for list/show commands."""

    def test_list_basic(self):
        result = parse_voice_command("list")
        assert result == {"action": "ls"}

    def test_show_all_tasks(self):
        result = parse_voice_command("show all tasks")
        assert result == {"action": "ls"}

    def test_display_tasks(self):
        result = parse_voice_command("display tasks")
        assert result == {"action": "ls"}

    def test_show_me_all(self):
        result = parse_voice_command("show me all")
        assert result == {"action": "ls"}

    def test_list_with_noise(self):
        result = parse_voice_command("please list my todos")
        assert result == {"action": "ls"}


class TestAddCommands:
    """Tests for add/create task commands."""

    def test_add_simple(self):
        result = parse_voice_command("add buy milk")
        assert result == {"action": "add", "description": "buy milk"}

    def test_add_with_please(self):
        result = parse_voice_command("please add do boxing as a todo")
        assert result == {"action": "add", "description": "do boxing as a todo"}

    def test_create_task(self):
        result = parse_voice_command("create task record the video")
        assert result == {"action": "add", "description": "record the video"}

    def test_new_task(self):
        result = parse_voice_command("new task review pull requests")
        assert result == {"action": "add", "description": "review pull requests"}

    def test_add_long_description(self):
        result = parse_voice_command("add prepare slides for tomorrow's hackathon presentation")
        assert result == {"action": "add", "description": "prepare slides for tomorrow's hackathon presentation"}

    def test_create_with_as(self):
        result = parse_voice_command("create as finish documentation")
        assert result == {"action": "add", "description": "finish documentation"}


class TestCompleteCommands:
    """Tests for mark complete/done commands."""

    def test_done_basic(self):
        result = parse_voice_command("done 1")
        assert result == {"action": "done", "id": 1}

    def test_complete_with_id(self):
        result = parse_voice_command("complete id 5")
        assert result == {"action": "done", "id": 5}

    def test_mark_task_complete(self):
        result = parse_voice_command("mark task 3 complete")
        assert result == {"action": "done", "id": 3}

    def test_mark_as_complete(self):
        result = parse_voice_command("mark task as complete, id is 2")
        assert result == {"action": "done", "id": 2}

    def test_mark_done(self):
        result = parse_voice_command("mark 7 done")
        assert result == {"action": "done", "id": 7}

    def test_complete_task_number(self):
        result = parse_voice_command("complete task number 10")
        assert result == {"action": "done", "id": 10}


class TestDeleteCommands:
    """Tests for delete/remove commands."""

    def test_delete_basic(self):
        result = parse_voice_command("delete 1")
        assert result == {"action": "rm", "id": 1}

    def test_remove_task(self):
        result = parse_voice_command("remove task 4")
        assert result == {"action": "rm", "id": 4}

    def test_delete_with_id(self):
        result = parse_voice_command("delete id 8")
        assert result == {"action": "rm", "id": 8}

    def test_remove_task_id(self):
        result = parse_voice_command("remove task id 12")
        assert result == {"action": "rm", "id": 12}


class TestEditCommands:
    """Tests for edit/update commands."""

    def test_edit_basic(self):
        result = parse_voice_command("edit 1 to buy chocolate")
        assert result == {"action": "edit", "id": 1, "description": "buy chocolate"}

    def test_update_task(self):
        result = parse_voice_command("update task 5 to review the code")
        assert result == {"action": "edit", "id": 5, "description": "review the code"}

    def test_change_with_id(self):
        result = parse_voice_command("change id 3 with finish the report")
        assert result == {"action": "edit", "id": 3, "description": "finish the report"}

    def test_edit_task_to(self):
        result = parse_voice_command("edit task id 2 to make tutorial video")
        assert result == {"action": "edit", "id": 2, "description": "make tutorial video"}

    def test_update_long_description(self):
        result = parse_voice_command("update 7 to complete all unit tests for the new feature")
        assert result == {"action": "edit", "id": 7, "description": "complete all unit tests for the new feature"}


class TestHelpCommand:
    """Tests for help command."""

    def test_help_basic(self):
        result = parse_voice_command("help")
        assert result == {"action": "help"}

    def test_help_with_please(self):
        result = parse_voice_command("please help me")
        assert result == {"action": "help"}


class TestAmbiguousCommands:
    """Tests for ambiguous or unparseable commands."""

    def test_empty_string(self):
        result = parse_voice_command("")
        assert result is None

    def test_random_text(self):
        result = parse_voice_command("hello there")
        assert result is None

    def test_incomplete_add(self):
        # "add" without description returns None (no valid command)
        result = parse_voice_command("add")
        assert result is None

    def test_delete_without_id(self):
        result = parse_voice_command("delete task")
        assert result is None

    def test_mark_complete_without_id(self):
        result = parse_voice_command("mark complete")
        assert result is None

    def test_edit_without_new_description(self):
        result = parse_voice_command("edit 5")
        assert result is None


class TestCaseInsensitivity:
    """Tests to ensure case-insensitive parsing."""

    def test_uppercase_add(self):
        result = parse_voice_command("ADD BUY MILK")
        assert result == {"action": "add", "description": "buy milk"}

    def test_mixed_case_list(self):
        result = parse_voice_command("SHOW All Tasks")
        assert result == {"action": "ls"}

    def test_uppercase_done(self):
        result = parse_voice_command("DONE 3")
        assert result == {"action": "done", "id": 3}


class TestNaturalLanguageVariations:
    """Tests for natural language variations and edge cases."""

    def test_polite_add(self):
        result = parse_voice_command("could you please add clean the room")
        assert result == {"action": "add", "description": "clean the room"}

    def test_conversational_list(self):
        result = parse_voice_command("can you show me all my tasks")
        assert result == {"action": "ls"}

    def test_verbose_complete(self):
        result = parse_voice_command("I want to mark task number 5 as complete")
        assert result == {"action": "done", "id": 5}

    def test_add_with_punctuation(self):
        result = parse_voice_command("add: review the documentation!")
        assert result == {"action": "add", "description": "review the documentation!"}

    def test_multiple_numbers_picks_first(self):
        # When multiple numbers exist, parser should pick contextually
        result = parse_voice_command("delete 3 tasks starting from 1")
        # Should pick the first number after delete keyword
        assert result == {"action": "rm", "id": 3}


class TestEdgeCases:
    """Tests for edge cases and boundary conditions."""

    def test_whitespace_handling(self):
        result = parse_voice_command("   add    buy   milk   ")
        assert result == {"action": "add", "description": "buy   milk"}

    def test_numeric_task_description(self):
        # When "task" appears after "add", the regex captures after "task"
        result = parse_voice_command("add task 123 is important")
        assert result == {"action": "add", "description": "123 is important"}

    def test_id_zero(self):
        result = parse_voice_command("done 0")
        assert result == {"action": "done", "id": 0}

    def test_large_id(self):
        result = parse_voice_command("delete 999999")
        assert result == {"action": "rm", "id": 999999}

    def test_special_characters_in_description(self):
        result = parse_voice_command("add buy @groceries #urgent")
        assert result == {"action": "add", "description": "buy @groceries #urgent"}
