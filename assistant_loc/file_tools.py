from pathlib import Path
import pymupdf
from docx import Document


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

def search_in_pdf(pdf_path, keyword):
    pdf_path = Path(pdf_path)

    if not pdf_path.exists():
        return []

    keyword_lower = keyword.lower()
    results = []

    try:
        document = pymupdf.open(pdf_path)

        for page_number, page in enumerate(document, start=1):
            text = page.get_text()
            text_lower = text.lower()

            position = text_lower.find(keyword_lower)

            if position != -1:
                start = max(0, position - 100)
                end = min(len(text), position + len(keyword) + 100)

                snippet = text[start:end].strip()

                results.append(
                    (
                        page_number,
                        snippet
                    )
                )

        document.close()

    except (OSError, RuntimeError):
        return []

    return results

def search_in_all_pdfs(folder, keyword):
    folder = Path(folder)

    if not folder.exists():
        return []

    results = []

    for pdf_path in folder.rglob("*.pdf"):

        if not pdf_path.is_file():
            continue

        matches = search_in_pdf(
            pdf_path,
            keyword
        )

        for page_number, snippet in matches:
            results.append(
                (
                    pdf_path,
                    page_number,
                    snippet
                )
            )

    return results

def search_in_docx(docx_path, keyword):
    docx_path = Path(docx_path)

    if not docx_path.exists():
        return []

    keyword_lower = keyword.lower()
    results = []

    try:
        document = Document(docx_path)

        for paragraph_number, paragraph in enumerate(
            document.paragraphs,
            start=1
        ):
            text = paragraph.text

            if keyword_lower in text.lower():
                results.append(
                    (
                        paragraph_number,
                        text.strip()
                    )
                )

    except (OSError, ValueError):
        return []

    return results

def search_in_all_docx(folder, keyword):
    folder = Path(folder)

    if not folder.exists():
        return []

    results = []

    for docx_path in folder.rglob("*.docx"):

        if not docx_path.is_file():
            continue

        matches = search_in_docx(
            docx_path,
            keyword
        )

        for paragraph_number, text in matches:
            results.append(
                (
                    docx_path,
                    paragraph_number,
                    text
                )
            )

    return results

def search_content(folder, keyword, file_type=None):

    if file_type == "pdf":
        raw_results = search_in_all_pdfs(
            folder,
            keyword
        )

        location_type = "Page"
        result_file_type = "pdf"

    elif file_type == "docx":
        raw_results = search_in_all_docx(
            folder,
            keyword
        )

        location_type = "Paragraphe"
        result_file_type = "docx"

    else:
        raw_results = search_in_contents(
            folder,
            keyword
        )

        location_type = "Ligne"
        result_file_type = "text"

    results = []

    for path, position, snippet in raw_results:
        result = {
            "path": path,
            "file_type": result_file_type,
            "location_type": location_type,
            "position": position,
            "snippet": snippet
        }

        results.append(result)

    return results