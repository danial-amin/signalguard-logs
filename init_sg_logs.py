import os

PROJECT_ROOT = "signalguard-logs"

DIRS = [
    "signalguard_logs",
    "signalguard_logs/models",
    "signalguard_logs/parsing",
    "signalguard_logs/features",
    "signalguard_logs/detectors",
    "signalguard_logs/recipes",
    "signalguard_logs/examples",
    "tests",
]

FILES = {
    "signalguard_logs/__init__.py": '''"""
signalguard_logs
----------------
Lightweight log AIOps toolkit for parsing, templating, and anomaly detection.
"""
__version__ = "0.1.0"
''',

    "signalguard_logs/models/__init__.py": "from .record import LogRecord\nfrom .stream import LogStream\n",
    "signalguard_logs/models/record.py": "# TODO: paste LogRecord implementation here\n",
    "signalguard_logs/models/stream.py": "# TODO: paste LogStream implementation here\n",

    "signalguard_logs/parsing/__init__.py": "from .regex_parser import RegexLogParser\nfrom .json_parser import JsonLogParser\n",
    "signalguard_logs/parsing/regex_parser.py": "# TODO: paste RegexLogParser implementation here\n",
    "signalguard_logs/parsing/json_parser.py": "# TODO: paste JsonLogParser implementation here\n",

    "signalguard_logs/features/__init__.py": "from .templates import LogTemplateExtractor\nfrom .text_vectorizer import TFIDFVectorizer\n",
    "signalguard_logs/features/templates.py": "# TODO: paste LogTemplateExtractor implementation here\n",
    "signalguard_logs/features/text_vectorizer.py": "# TODO: paste TFIDFVectorizer implementation here\n",

    "signalguard_logs/detectors/__init__.py": "from .burst import LogBurstDetector\nfrom .new_template import NewTemplateDetector\nfrom .semantic_iforest import SemanticIForestDetector\n",
    "signalguard_logs/detectors/base.py": "# TODO: paste BaseLogDetector implementation here\n",
    "signalguard_logs/detectors/burst.py": "# TODO: paste LogBurstDetector implementation here\n",
    "signalguard_logs/detectors/new_template.py": "# TODO: paste NewTemplateDetector implementation here\n",
    "signalguard_logs/detectors/semantic_iforest.py": "# TODO: paste SemanticIForestDetector implementation here\n",

    "signalguard_logs/recipes/__init__.py": "from .error_burst import ErrorBurstRecipe\nfrom .new_pattern import NewErrorPatternRecipe\nfrom .combined_health import CombinedLogHealthRecipe\n",
    "signalguard_logs/recipes/error_burst.py": "# TODO: paste ErrorBurstRecipe implementation here\n",
    "signalguard_logs/recipes/new_pattern.py": "# TODO: paste NewErrorPatternRecipe implementation here\n",
    "signalguard_logs/recipes/combined_health.py": "# TODO: paste CombinedLogHealthRecipe implementation here\n",

    "signalguard_logs/examples/synthetic_error_burst.py": "# TODO: paste synthetic error burst demo here\n",
    "signalguard_logs/examples/synthetic_new_pattern.py": "# TODO: paste new pattern demo here\n",

    "tests/test_templates.py": "# TODO: simple tests for template extraction\n",

    ".gitignore": "__pycache__/\n*.pyc\n.env\n.venv/\n.idea/\n.vscode/\n",
    "README.md": "# signalguard-logs\n\nLog AIOps toolkit for parsing, templating, and anomaly detection.\n",
    "pyproject.toml": """[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "signalguard-logs"
version = "0.1.0"
description = "Log AIOps toolkit for parsing, templating, and anomaly detection"
authors = [
  { name = "Danial Amin" }
]
requires-python = ">=3.9"
dependencies = [
  "numpy",
  "pandas",
  "scikit-learn"
]
"""
}


def main():
    print(f"Creating project at ./{PROJECT_ROOT}")
    os.makedirs(PROJECT_ROOT, exist_ok=True)

    for d in DIRS:
        path = os.path.join(PROJECT_ROOT, d)
        os.makedirs(path, exist_ok=True)
        print("dir:", path)

    for rel, content in FILES.items():
        path = os.path.join(PROJECT_ROOT, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        if not os.path.exists(path):
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            print("file:", path)
        else:
            print("skip (exists):", path)

    print("Done.")


if __name__ == "__main__":
    main()
