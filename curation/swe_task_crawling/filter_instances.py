import re

def is_valid_pull(pull: dict) -> bool:
    """
    Check whether PR has an associated issue and is merged

    Args:
        pull (dict): pull request object
    Returns:
        bool: whether PR is valid
    """
    if pull["merged_at"] is None:
        return False
    if "resolved_issues" not in pull or len(pull["resolved_issues"]) < 1:
        return False
    return True

def has_code_edited(patch_content: str, language: str) -> bool:
    """
    Check if the patch contains code edits for the specified language.
    
    Args:
        patch_content (str): Git patch content to analyze
        language (str): Target programming language
    Returns:
        bool: True if patch contains code files for the specified language
    """
    # File extensions for major programming languages
    language_suffix = {
        "Python": [".py"],
        "Rust": [".rs"],
        "Go": [".go"],
        "TypeScript": [".ts", ".tsx"],
        "JavaScript": [".js", ".jsx", ".mjs"],
        "Java": [".java"],
        "C": [".c", ".h"],
        "C++": [".cpp", ".cc", ".cxx", ".h", ".hpp"],
        "PHP": [".php"],
        "Ruby": [".rb"]
    }
    
    # Extract changed file paths from patch
    pattern = r'^diff --git a/(.*?) b/'
    changed_files = set()
    # print(patch_content)
    for line in patch_content.split('\n'):
        match = re.match(pattern, line)
        if match:
            file_path = match.group(1).strip()
            changed_files.add(file_path)
    # print(changed_files)
    # Return True if any changed file matches the language's extensions
    return any(
        changed_file.endswith(tuple(language_suffix[language])) 
        for changed_file in changed_files
    )

def is_valid_instance_base(instance: dict) -> bool:
    """
    Check if task instance has all required fields and contains code edits.
    
    Args:
        instance (dict): Task instance object
    Returns:
        bool: Whether task instance is valid
    """
    if instance["patch"] is None or instance["patch"].strip() == "":
        return False
    if instance["test_patch"] is None or instance["test_patch"].strip() == "":
        return False
    if instance["problem_statement"] is None or instance["problem_statement"] == "":
        return False
    if not has_code_edited(instance["patch"], instance["language"]) or not has_code_edited(instance["test_patch"], instance["language"]):
        return False
    return True

def is_valid_instance_medium(instance: dict) -> bool:
    """
    Check if task instance meets medium-level validation criteria.
    
    Args:
        instance (dict): Task instance object
    Returns:
        bool: Whether task instance meets medium validation
    """
    if instance["patch"].count("\n") > 1000:
        return False
    if instance["patch"].count("diff --git a/") > 10:
        return False
    return True

def is_valid_instance_high(instance: dict) -> bool:
    """
    Check if task instance meets high-level validation criteria.
    
    Args:
        instance (dict): Task instance object
    Returns:
        bool: Whether task instance meets high validation
    """
    if instance["patch"].count("\n") > 500:
        return False
    if instance["patch"].count("diff --git a/") > 5:
        return False
    return True