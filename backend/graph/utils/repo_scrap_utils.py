import os

# Lista de nomes que devem ser ignorados (case-sensitive)
IGNORE_NAMES = {"__pycache__", "__init__.py"}


def build_tree_string(root, prefix=""):
    lines = []
    try:
        entries = sorted([
            entry for entry in os.listdir(root)
            if not entry.startswith('.') and entry not in IGNORE_NAMES
        ])
    except PermissionError:
        return lines
    entries_count = len(entries)

    for i, entry in enumerate(entries):
        path = os.path.join(root, entry)
        is_last = (i == entries_count - 1)
        connector = "└── " if is_last else "├── "
        # Se for diretório, mas também ignora se o nome estiver na lista de ignorados
        if os.path.isdir(path):
            lines.append(prefix + connector + entry + "/")
            new_prefix = prefix + ("    " if is_last else "│   ")
            lines.extend(build_tree_string(path, new_prefix))
        else:
            lines.append(prefix + connector + entry)
    return lines


def get_tree_string(root_dir):
    """
    Function to get the tree structure of a directory.

    Example:
    root_dir/
    ├── dir1/
    │   ├── file1
    │   └── file2
    └── file3

    Args:
        root_dir (str): Diretório raiz.
    """
    tree_lines = [root_dir + "/"] + build_tree_string(root_dir)
    return "\n".join(tree_lines)


if __name__ == "__main__":
    root_directory = "/Users/matheussilva/Documents/projects/code-assistant"
    tree_str = get_tree_string(root_directory)
    print(tree_str)
