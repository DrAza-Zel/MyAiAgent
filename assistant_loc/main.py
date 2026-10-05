from pathlib import Path
from file_tools import search_documents, search_by_name


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
            extension = extract_extension(message)

            # Pour l'instant, recherche dans tout ton dossier utilisateur
            houss = Path.home()

            if extension is not None:

                files = search_documents(houss, extension)

                print(
                    f"Assistant > {len(files)} fichiers "
                    f"{extension} trouvés."
                )

            else:
                keyword = extract_keyword(message)

                if keyword is None:
                    print("Assistant > Que veux-tu rechercher ?")
                    continue

                files = search_by_name(houss, keyword)

                print(
                    f"Assistant > {len(files)} fichiers "
                    f"contenant '{keyword}' trouvés."
                )

            for file in files:
                print(file)

        else:
            print(f"Assistant > Intention détectée : {intent}")


if __name__ == "__main__":
    main()