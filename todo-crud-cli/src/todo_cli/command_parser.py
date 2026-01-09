import re
from typing import Optional, Dict, Any, List

# Number word mappings for fuzzy recognition
NUMBER_WORDS = {
    'zero': 0, 'one': 1, 'two': 2, 'to': 2, 'too': 2, 'three': 3, 'four': 4, 'for': 4, 'fr': 4, 'fore': 4,
    'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'ate': 8, 'nine': 9, 'ten': 10,
    'eleven': 11, 'twelve': 12, 'thirteen': 13, 'fourteen': 14, 'fifteen': 15,
    'sixteen': 16, 'seventeen': 17, 'eighteen': 18, 'nineteen': 19, 'twenty': 20
}

# Command synonyms
ADD_KEYWORDS = ['add', 'create', 'new', 'make', 'insert', 'append']
DELETE_KEYWORDS = ['delete', 'remove', 'rm', 'undo', 'destroy', 'erase', 'del', 'trash', 'discard']
COMPLETE_KEYWORDS = ['done', 'complete', 'finish', 'mark', 'tick', 'check', 'accomplish']
EDIT_KEYWORDS = ['edit', 'update', 'change', 'modify', 'alter', 'revise']
LIST_KEYWORDS = ['list', 'show', 'display', 'view', 'all', 'see']

def normalize_number_words(text: str) -> str:
    """
    Convert number words to digits for better parsing.
    Context-aware: doesn't convert 'to/too' when used as preposition.
    """
    words = text.split()
    normalized = []

    for i, word in enumerate(words):
        # Skip 'to' if it appears after edit keywords (used as preposition)
        if word in ['to', 'too'] and i > 0:
            prev_word = words[i-1].lower()
            # If previous word looks like a number or ID, it's probably "task 2 to..."
            # So keep "to" as-is
            if prev_word.isdigit() or any(k in ' '.join(words[max(0,i-3):i]) for k in ['edit', 'update', 'change', 'modify', 'alter', 'revise']):
                normalized.append(word)
                continue

        if word in NUMBER_WORDS:
            normalized.append(str(NUMBER_WORDS[word]))
        else:
            normalized.append(word)

    return ' '.join(normalized)

def parse_voice_command(text: str) -> Optional[Dict[str, Any]]:
    """
    Parses voice text into structured commands with enhanced synonym support.
    Returns a dict with 'action' and optional parameters.
    """
    text = text.lower().strip()

    # Early exit for empty string
    if not text:
        return None

    # Normalize number words to digits
    text = normalize_number_words(text)

    # Help command
    if "help" in text:
        return {"action": "help"}

    # Batch operations - delete all
    delete_all_pattern = '|'.join(DELETE_KEYWORDS)
    if re.search(rf"(?:{delete_all_pattern})(?:\s+all|\s+everything)", text):
        return {"action": "delete_all"}

    # Batch operations - delete completed (check before single delete)
    if re.search(rf"(?:{delete_all_pattern})(?:\s+(?:completed|finished|done|completed\s+tasks|finished\s+tasks))", text):
        return {"action": "delete_completed"}

    # Delete task with expanded synonyms
    delete_pattern = '|'.join(DELETE_KEYWORDS)
    rm_match = re.search(rf"(?:{delete_pattern})(?:\s+task)?(?:\s+(?:id|number))?\s+(\d+)", text)
    if rm_match:
        return {"action": "rm", "id": int(rm_match.group(1))}

    # Edit/Update task - check BEFORE complete to avoid conflicts
    # Pattern requires "to" or "with" which distinguishes from other commands
    edit_pattern = '|'.join(EDIT_KEYWORDS)
    edit_match = re.search(rf"(?:{edit_pattern})(?:\s+task)?(?:\s+(?:id|number))?\s+(\d+)\s+(?:to|with)\s+(.+)", text)
    if edit_match:
        description = edit_match.group(2).strip()
        return {"action": "edit", "id": int(edit_match.group(1)), "description": description}

    # Complete task with expanded synonyms
    complete_pattern = '|'.join(COMPLETE_KEYWORDS)
    done_match = re.search(rf"(?:{complete_pattern})(?:\s+task)?(?:\s+(?:id|number))?\s+(\d+)", text)
    if done_match:
        return {"action": "done", "id": int(done_match.group(1))}

    # Add task with expanded synonyms - check LAST to avoid greedy matching
    add_pattern = '|'.join(ADD_KEYWORDS)
    add_match = re.search(rf"(?:{add_pattern})(?:\s+task)?(?:\s+as)?[:\s]+(.+)", text)
    if add_match:
        description = add_match.group(1).strip()
        if description:
            return {"action": "add", "description": description}

    # List tasks with expanded synonyms
    list_pattern = '|'.join(LIST_KEYWORDS)
    if re.search(rf"\b(?:{list_pattern})\b", text):
        return {"action": "ls"}

    # Fallback/Ambiguous
    return None

def parse_multi_command(text: str) -> List[Dict[str, Any]]:
    """
    Parses multiple commands from a single voice input.
    Splits on 'and', 'then', 'also' keywords.
    Returns a list of command dictionaries.
    """
    text = text.lower().strip()

    # Split on command separators
    separators = [' and ', ' then ', ' also ', ' plus ']
    parts = [text]

    for sep in separators:
        new_parts = []
        for part in parts:
            new_parts.extend(part.split(sep))
        parts = new_parts

    # Parse each part
    commands = []
    for part in parts:
        part = part.strip()
        if part:
            cmd = parse_voice_command(part)
            if cmd:
                commands.append(cmd)

    return commands if commands else []
