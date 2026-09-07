import re
import discord
from discord import app_commands

from .game import WerewolfGame


@app_commands.command(
    name="werewolf",
    description="Start a game of Werewolf."
)
@app_commands.describe(
    players="Mention at least 1 player.",
    werewolves="Number of werewolves.",
    seers="Number of seers.",
    doctors="Number of doctors.",
    villagers="Number of villagers."
)
async def werewolf(
    interaction: discord.Interaction,
    players: str,
    werewolves: int | None = None,
    seers: int | None = None,
    doctors: int | None = None,
    villagers: int | None = None
):
    if not interaction.guild:
        await interaction.response.send_message(
            "Werewolf can only be played in a server."
        )
        return

    player_ids = re.findall(r"<@!?(\d+)>", players)

    if not player_ids:
        await interaction.response.send_message(
            "You need to mention at least one player."
        )
        return

    player_ids = list(dict.fromkeys(map(int, player_ids)))

    members = []

    for user_id in player_ids:
        member = interaction.guild.get_member(user_id)

        if member is None:
            continue

        if member.bot:
            continue

        members.append(member)

    if not members:
        await interaction.response.send_message(
            "You need to mention at least one real member."
        )
        return

    while len(members) < 3:
        members.append(
            await interaction.guild.fetch_member(interaction.client.user.id)
        )

        break

    total_players = len(members)

    role_counts = {
        "werewolf": werewolves,
        "seer": seers,
        "doctor": doctors,
        "villager": villagers
    }

    provided_roles = {
        role: count
        for role, count in role_counts.items()
        if count is not None
    }

    for role, count in provided_roles.items():
        if count < 0:
            await interaction.response.send_message(
                f"`{role}` cannot be negative."
            )
            return

    if provided_roles and sum(provided_roles.values()) != total_players:
        await interaction.response.send_message(
            f"The role counts must add up to exactly "
            f"{total_players} players."
        )
        return

    game = WerewolfGame(
        guild=interaction.guild,
        channel=interaction.channel,
        players=members,
        role_counts=provided_roles
    )

    await interaction.response.send_message(
        "🐺 Werewolf game created!"
    )

    await game.start()


bot.tree.add_command(werewolf)