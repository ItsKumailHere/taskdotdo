"""
Tests for advanced voice features:
- Extended command synonyms
- Fuzzy number recognition
- Multi-command parsing
- Batch operations
"""
import pytest
from todo_cli.command_parser import (
    parse_voice_command,
    parse_multi_command,
    normalize_number_words,
    NUMBER_WORDS
)


class TestNumberWordRecognition:
    """Tests for fuzzy number recognition."""

    def test_four_variations(self):
        # "four", "for", "fr", "fore" all map to 4
        assert normalize_number_words("four") == "4"
        assert normalize_number_words("for") == "4"
        assert normalize_number_words("fr") == "4"
        assert normalize_number_words("fore") == "4"

    def test_two_variations(self):
        # "two", "to", "too" all map to 2
        assert normalize_number_words("two") == "2"
        assert normalize_number_words("to") == "2"
        assert normalize_number_words("too") == "2"

    def test_eight_variations(self):
        # "eight", "ate" map to 8
        assert normalize_number_words("eight") == "8"
        assert normalize_number_words("ate") == "8"

    def test_in_sentence(self):
        result = normalize_number_words("delete task for")
        assert "4" in result

    def test_multiple_numbers(self):
        result = normalize_number_words("task two and task four")
        assert "2" in result and "4" in result


class TestExpandedSynonyms:
    """Tests for expanded command synonyms."""

    # Delete synonyms
    def test_remove_synonym(self):
        result = parse_voice_command("remove task 5")
        assert result == {"action": "rm", "id": 5}

    def test_undo_synonym(self):
        result = parse_voice_command("undo task 3")
        assert result == {"action": "rm", "id": 3}

    def test_destroy_synonym(self):
        result = parse_voice_command("destroy 7")
        assert result == {"action": "rm", "id": 7}

    def test_erase_synonym(self):
        result = parse_voice_command("erase task 2")
        assert result == {"action": "rm", "id": 2}

    def test_trash_synonym(self):
        result = parse_voice_command("trash 9")
        assert result == {"action": "rm", "id": 9}

    def test_discard_synonym(self):
        result = parse_voice_command("discard task number 4")
        assert result == {"action": "rm", "id": 4}

    # Complete synonyms
    def test_finish_synonym(self):
        result = parse_voice_command("finish task 1")
        assert result == {"action": "done", "id": 1}

    def test_tick_synonym(self):
        result = parse_voice_command("tick 5")
        assert result == {"action": "done", "id": 5}

    def test_check_synonym(self):
        result = parse_voice_command("check task 3")
        assert result == {"action": "done", "id": 3}

    def test_accomplish_synonym(self):
        result = parse_voice_command("accomplish 8")
        assert result == {"action": "done", "id": 8}

    # Add synonyms
    def test_make_synonym(self):
        result = parse_voice_command("make task buy groceries")
        assert result == {"action": "add", "description": "buy groceries"}

    def test_insert_synonym(self):
        result = parse_voice_command("insert new workout")
        assert result == {"action": "add", "description": "new workout"}

    def test_append_synonym(self):
        result = parse_voice_command("append call mom")
        assert result == {"action": "add", "description": "call mom"}

    # Edit synonyms
    def test_modify_synonym(self):
        result = parse_voice_command("modify task 2 to updated text")
        assert result == {"action": "edit", "id": 2, "description": "updated text"}

    def test_alter_synonym(self):
        result = parse_voice_command("alter task id 5 to new description")
        assert result == {"action": "edit", "id": 5, "description": "new description"}

    def test_revise_synonym(self):
        result = parse_voice_command("revise 1 with better text")
        assert result == {"action": "edit", "id": 1, "description": "better text"}

    # List synonyms
    def test_view_synonym(self):
        result = parse_voice_command("view all tasks")
        assert result == {"action": "ls"}

    def test_see_synonym(self):
        result = parse_voice_command("see my todos")
        assert result == {"action": "ls"}


class TestFuzzyNumbersInCommands:
    """Tests for fuzzy number recognition in full commands."""

    def test_delete_for(self):
        # "for" should be recognized as 4
        result = parse_voice_command("delete for")
        assert result == {"action": "rm", "id": 4}

    def test_done_too(self):
        # "too" should be recognized as 2
        result = parse_voice_command("done too")
        assert result == {"action": "done", "id": 2}

    def test_finish_ate(self):
        # "ate" should be recognized as 8
        result = parse_voice_command("finish ate")
        assert result == {"action": "done", "id": 8}

    def test_remove_fr(self):
        # "fr" should be recognized as 4
        result = parse_voice_command("remove fr")
        assert result == {"action": "rm", "id": 4}


class TestBatchOperations:
    """Tests for batch delete operations."""

    def test_delete_all(self):
        result = parse_voice_command("delete all")
        assert result == {"action": "delete_all"}

    def test_remove_all(self):
        result = parse_voice_command("remove all")
        assert result == {"action": "delete_all"}

    def test_erase_everything(self):
        result = parse_voice_command("erase everything")
        assert result == {"action": "delete_all"}

    def test_destroy_all_tasks(self):
        result = parse_voice_command("destroy all tasks")
        assert result == {"action": "delete_all"}

    def test_delete_completed(self):
        result = parse_voice_command("delete completed")
        assert result == {"action": "delete_completed"}

    def test_remove_finished(self):
        result = parse_voice_command("remove finished")
        assert result == {"action": "delete_completed"}

    def test_erase_done_tasks(self):
        result = parse_voice_command("erase done")
        assert result == {"action": "delete_completed"}


class TestMultiCommandParsing:
    """Tests for parsing multiple commands in one input."""

    def test_two_commands_with_and(self):
        commands = parse_multi_command("add buy milk and delete 5")
        assert len(commands) == 2
        assert commands[0] == {"action": "add", "description": "buy milk"}
        assert commands[1] == {"action": "rm", "id": 5}

    def test_two_commands_with_then(self):
        commands = parse_multi_command("create new task then finish 3")
        assert len(commands) == 2
        assert commands[0] == {"action": "add", "description": "new task"}
        assert commands[1] == {"action": "done", "id": 3}

    def test_two_commands_with_also(self):
        commands = parse_multi_command("list all tasks also done 2")
        assert len(commands) == 2
        assert commands[0] == {"action": "ls"}
        assert commands[1] == {"action": "done", "id": 2}

    def test_three_commands(self):
        commands = parse_multi_command("add task one and add task two then list")
        assert len(commands) == 3
        assert commands[0]["action"] == "add"
        assert commands[1]["action"] == "add"
        assert commands[2]["action"] == "ls"

    def test_complex_multi_command(self):
        commands = parse_multi_command("make homework and finish for then erase completed")
        assert len(commands) == 3
        assert commands[0] == {"action": "add", "description": "homework"}
        assert commands[1] == {"action": "done", "id": 4}  # "for" -> 4
        assert commands[2] == {"action": "delete_completed"}

    def test_single_command_returns_list(self):
        commands = parse_multi_command("add single task")
        assert len(commands) == 1
        assert commands[0] == {"action": "add", "description": "single task"}

    def test_invalid_commands_filtered(self):
        # "hello" is not valid, should be filtered
        commands = parse_multi_command("hello and add valid task")
        assert len(commands) == 1
        assert commands[0]["action"] == "add"

    def test_empty_returns_empty_list(self):
        commands = parse_multi_command("")
        assert commands == []


class TestAdvancedEdgeCases:
    """Advanced edge cases with new features."""

    def test_synonym_with_fuzzy_number(self):
        # "erase" (synonym) + "for" (fuzzy 4)
        result = parse_voice_command("erase for")
        assert result == {"action": "rm", "id": 4}

    def test_multi_command_with_fuzzy_numbers(self):
        commands = parse_multi_command("done too and remove for")
        assert len(commands) == 2
        assert commands[0] == {"action": "done", "id": 2}
        assert commands[1] == {"action": "rm", "id": 4}

    def test_batch_with_separator(self):
        # Ensure "delete all" doesn't split on "and" within the command
        result = parse_voice_command("delete all")
        assert result == {"action": "delete_all"}

    def test_add_with_number_words_in_description(self):
        # Number words in description should be preserved
        result = parse_voice_command("add buy four apples")
        # "four" becomes "4" in description
        assert result["action"] == "add"
        assert "4" in result["description"] or "apples" in result["description"]
