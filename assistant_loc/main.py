from pathlib import Path

from file_tools import (
    search_documents,
    search_by_name,
    search_content
)

from math_tools import calculate


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


def extract_file_type(message):
    message = message.lower()

    if "pdf" in message:
        return "pdf"

    elif "word" in message or "docx" in message:
        return "docx"

    else:
        return None


def extract_math_expression(message):
    message = message.lower()

    if "calcule" not in message:
        return None

    expression = message.split(
        "calcule",
        1
    )[1].strip()

    if expression == "":
        return None

    return expression


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

            # Recherche dans le contenu
            content_keyword = extract_content_keyword(message)

            if content_keyword is not None:
                file_type = extract_file_type(message)

                results = search_content(
                    houss,
                    content_keyword,
                    file_type
                )

                print(
                    f"Assistant > {len(results)} résultat(s) trouvés."
                )

                for result in results:
                    print(f"\n{result['path']}")

                    print(
                        f"{result['location_type']} "
                        f"{result['position']}"
                    )

                    print(result["snippet"])

                continue

            # Recherche par extension
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

            # Recherche par nom
            else:
                keyword = extract_keyword(message)

                if keyword is None:
                    print(
                        "Assistant > Que veux-tu rechercher ?"
                    )
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

        elif intent == "MATH":
            expression = extract_math_expression(
                message
            )

            if expression is None:
                print(
                    "Assistant > Quelle expression "
                    "veux-tu calculer ?"
                )
                continue

            try:
                result = calculate(expression)

                print(
                    f"Assistant > Résultat : {result}"
                )

            except (
                ValueError,
                SyntaxError,
                ZeroDivisionError,
                TypeError
            ) as error:

                print(
                    f"Assistant > Calcul impossible : "
                    f"{error}"
                )

        else:
            print(
                f"Assistant > Intention détectée : {intent}"
            )


if __name__ == "__main__":
    main()