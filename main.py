import asyncio
import importlib
import os
from pathlib import Path

import mycord
from dotenv import load_dotenv

load_dotenv()

ROOT = Path(__file__).parent


# =========================================
# FIND BOTS
# =========================================

def find_bots():
    bots = []

    for folder in ROOT.iterdir():
        if not folder.is_dir():
            continue

        bot_file = folder / "bot.py"

        if not bot_file.exists():
            continue

        try:
            module = importlib.import_module(f"{folder.name}.bot")
            bot = module.bot

            bots.append((folder, bot))

        except Exception as error:
            print(
                f"[ERROR] Failed to load "
                f"{folder.name}: {error}"
            )

    return bots


# =========================================
# LOAD FILES
# =========================================

async def load_folder(bot_folder, bot, folder_name):

    folder = bot_folder / folder_name

    if not folder.exists():
        return

    for file in folder.rglob("*.py"):

        if file.name == "__init__.py":
            continue

        relative = file.relative_to(ROOT)

        module_name = ".".join(
            relative.with_suffix("").parts
        )

        try:
            module = importlib.import_module(module_name)

            setup = getattr(module, "setup", None)

            if setup is None:
                continue

            result = setup(bot)

            if hasattr(result, "__await__"):
                await result

            print(
                f"[LOADED] {bot_folder.name} "
                f"{folder_name}/{file.stem}"
            )

        except Exception as error:
            print(
                f"[ERROR] Failed to load "
                f"{module_name}: {error}"
            )


# =========================================
# LOAD SYSTEMS
# =========================================

async def load_systems(bot_folder, bot):

    await load_folder(
        bot_folder,
        bot,
        "systems"
    )


# =========================================
# LOAD PREFIX COMMANDS
# =========================================

async def load_prefix_commands(bot_folder, bot):

    await load_folder(
        bot_folder,
        bot,
        "commands"
    )


# =========================================
# LOAD SLASH COMMANDS
# =========================================

async def load_slash_commands(bot_folder, bot):

    await load_folder(
        bot_folder,
        bot,
        "slash_commands"
    )


# =========================================
# RUN BOT
# =========================================

async def run_bot(bot_folder, bot):

    await load_systems(
        bot_folder,
        bot
    )

    await load_prefix_commands(
        bot_folder,
        bot
    )

    await load_slash_commands(
        bot_folder,
        bot
    )

    # Sync slash commands
    try:
        synced = await bot.tree.sync()

        print(
            f"[SLASH] {bot_folder.name}: "
            f"{len(synced)} commands synced"
        )

    except Exception as error:
        print(
            f"[ERROR] Failed to sync slash commands "
            f"for {bot_folder.name}: {error}"
        )

    tokens = {
        "atlas": os.getenv("ATLAS_TOKEN"),
        "lilith": os.getenv("LILITH_TOKEN"),
        "shaka": os.getenv("SHAKA_TOKEN"),
        "york": os.getenv("YORK_TOKEN"),
        "pythagoras": os.getenv("PYTHAGORAS_TOKEN"),
    }

    token = tokens.get(
        bot_folder.name.lower()
    )

    if not token:
        print(
            f"[ERROR] No token found for "
            f"{bot_folder.name}"
        )
        return

    try:
        await bot.start(token)

    except Exception as error:
        print(
            f"[ERROR] {bot_folder.name}: {error}"
        )


# =========================================
# MAIN
# =========================================

async def main():

    bots = find_bots()

    if not bots:
        print("[ERROR] No bots found.")
        return

    await asyncio.gather(
        *(
            run_bot(folder, bot)
            for folder, bot in bots
        )
    )


if __name__ == "__main__":
    asyncio.run(main())