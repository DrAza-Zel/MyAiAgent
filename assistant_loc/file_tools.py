from pathlib import Path


def search_documents(folder, extension):
    folder = Path(folder)

    if not folder.exists():
        return []

    if not extension.startswith("."):
        extension = "." + extension

    files = []

    for path in folder.rglob(f"*{extension}"):
        if path.is_file():
            files.append(path)

    return files
def search_by_name(folder, keyword):
    folder = Path(folder)

    if not folder.exists():
        return []

    keyword = keyword.lower()
    files = []

    for path in folder.rglob("*"):
        if path.is_file():
            if keyword in path.name.lower():
                files.append(path)

    return files
def search_in_contents(folder, keyword):
    folder = Path(folder)

    if not folder.exists():
        return []

    allowed_extensions = {
        ".txt",
        ".py",
        ".java",
        ".md",
        ".csv"
    }

    keyword = keyword.lower()
    results = []

    for path in folder.rglob("*"):

        if not path.is_file():
            continue

        if path.suffix.lower() not in allowed_extensions:
            continue

        try:
            with path.open(
                "r",
                encoding="utf-8",
                errors="ignore"
            ) as file:

                for line_number, line in enumerate(file, start=1):

                    if keyword in line.lower():
                        results.append(
                            (
                                path,
                                line_number,
                                line.strip()
                            )
                        )

                        break

        except (PermissionError, OSError):
            continue

    return results