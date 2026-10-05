from pathlib import Path

from file_tools import (
    search_documents,
    search_by_name,
    search_in_contents
)


def detect_intent(message):
    message = message.lower()

    if "cherche" in message:
        return "SEARCH"

    elif "calcule" in message:
        return "MATH"

    elif "image" in message:
        return "VISION"

    else:
        return "UNKNOWN"


def extract_extension(message):
    message = message.lower()

    if "pdf" in message:
        return ".pdf"

    elif "java" in message:
        return ".java"

    elif "python" in message or "py" in message:
        return ".py"

    elif "texte" in message or "txt" in message:
        return ".txt"

    else:
        return None


def extract_keyword(message):
    message = message.lower()

    if "cherche" not in message:
        return None

    keyword = message.split("cherche", 1)[1].strip()

    if keyword == "":
        return None

    return keyword


def extract_content_keyword(message):
    message = message.lower()

    if "contenu" not in message:
        return None

    keyword = message.split("contenu", 1)[1].strip()

    if keyword == "":
        return None

    return keyword


def main():
    print("Assistant démarré.")
    print("Écris 'quit' pour quitter.\n")

    while True:
        message = input("Houssam > ")

        if message.lower() == "quit":
            print("Assistant arrêté.")
            break

        intent = detect_intent(message)

        if intent == "SEARCH":
            houss = Path.home()

            content_keyword = extract_content_keyword(message)

            if content_keyword is not None:
                results = search_in_contents(
                    houss,
                    content_keyword
                )

                print(
                    f"Assistant > {len(results)} fichiers "
                    f"contenant '{content_keyword}' trouvés."
                )

                for path, line_number, line in results:
                    print(
                        f"\n{path}"
                        f"\nLigne {line_number} : {line}"
                    )

                continue

            extension = extract_extension(message)

            if extension is not None:
                files = search_documents(
                    houss,
                    extension
                )

                print(
                    f"Assistant > {len(files)} fichiers "
                    f"{extension} trouvés."
                )

            else:
                keyword = extract_keyword(message)

                if keyword is None:
                    print("Assistant > Que veux-tu rechercher ?")
                    continue

                files = search_by_name(
                    houss,
                    keyword
                )

                print(
                    f"Assistant > {len(files)} fichiers "
                    f"contenant '{keyword}' trouvés."
                )

            for file in files:
                print(file)

        else:
            print(
                f"Assistant > Intention détectée : {intent}"
            )


if __name__ == "__main__":
    main()