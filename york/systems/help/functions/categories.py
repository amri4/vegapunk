from pathlib import Path


def get_category(callback):
    try:
        path = Path(callback.__code__.co_filename)
        parts = path.parts

        if "systems" in parts:
            index = parts.index("systems")

            if index + 1 < len(parts):
                return parts[index + 1].replace("_", " ").title()

    except Exception:
        pass

    return "Other"