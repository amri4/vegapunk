import discord


FACTIONS = {
    "pirate": {
        "label": "Pirate",
        "role_name": "Pirate",
        "emoji": "🏴‍☠️",
        "style": discord.ButtonStyle.danger,
        "confirmation": "You're a Pirate now. Welcome to the crew."
    },
    "marine": {
        "label": "Marine",
        "role_name": "Marine",
        "emoji": "⚓",
        "style": discord.ButtonStyle.primary,
        "confirmation": "You're a Marine now. Justice will prevail."
    }
}


def faction_role(guild, role_name):
    return discord.utils.get(
        guild.roles,
        name=role_name
    )


class FactionButton(discord.ui.Button):

    def __init__(self, faction):
        details = FACTIONS[faction]

        super().__init__(
            label=details["label"],
            emoji=details["emoji"],
            style=details["style"],
            custom_id=f"edison:faction:{faction}"
        )

        self.faction = faction
        self.details = details

    async def callback(self, interaction: discord.Interaction):
        if interaction.guild is None:
            await interaction.response.send_message(
                "This only works in a server.",
                ephemeral=True
            )
            return

        member = interaction.user

        if not isinstance(member, discord.Member):
            await interaction.response.send_message(
                "This only works in a server.",
                ephemeral=True
            )
            return

        chosen_name = self.details["role_name"]
        chosen_role = faction_role(
            interaction.guild,
            chosen_name
        )

        if chosen_role is None:
            await interaction.response.send_message(
                f"❌ The **{chosen_name}** role doesn't exist.",
                ephemeral=True
            )
            return

        held = []

        for details in FACTIONS.values():
            role = faction_role(
                interaction.guild,
                details["role_name"]
            )

            if role is not None and role in member.roles:
                held.append(details["role_name"])

        if held:
            if chosen_name in held:
                await interaction.response.send_message(
                    f"You're already a **{chosen_name}**.",
                    ephemeral=True
                )
                return

            current = held[0]
            await interaction.response.send_message(
                f"You already belong to the **{current}s**. "
                "You can't join another faction.",
                ephemeral=True
            )
            return

        bot_member = interaction.guild.me

        if bot_member is None or chosen_role >= bot_member.top_role:
            await interaction.response.send_message(
                f"❌ I can't assign {chosen_role.mention}. "
                "My highest role must be above that role.",
                ephemeral=True
            )
            return

        try:
            await member.add_roles(
                chosen_role,
                reason="Faction selection"
            )
        except discord.Forbidden:
            await interaction.response.send_message(
                f"❌ I don't have permission to assign {chosen_role.mention}.",
                ephemeral=True
            )
            return
        except discord.HTTPException:
            await interaction.response.send_message(
                "❌ Discord rejected the role assignment.",
                ephemeral=True
            )
            return

        await interaction.response.send_message(
            self.details["confirmation"],
            ephemeral=True
        )


class FactionView(discord.ui.View):

    def __init__(self):
        super().__init__(
            timeout=None
        )

        self.add_item(
            FactionButton("pirate")
        )
        self.add_item(
            FactionButton("marine")
        )


def faction_embed():
    return discord.Embed(
        title="Choose Your Faction",
        description=(
            "The sea doesn't care who you were before you arrived.\n\n"
            "Pick a side. You can only belong to one faction.\n\n"
            "🏴‍☠️ **Pirate** — sail under your own flag.\n"
            "⚓ **Marine** — uphold justice for the World Government."
        ),
        color=discord.Color.dark_gold()
    ).set_footer(
        text="You can only choose one faction."
    )


async def send_faction_panel(interaction: discord.Interaction):
    channel = interaction.channel

    if channel is None:
        await interaction.response.send_message(
            "❌ I can't send a panel in this channel.",
            ephemeral=True
        )
        return

    await interaction.response.defer(
        ephemeral=True
    )

    try:
        await channel.send(
            embed=faction_embed(),
            view=FactionView()
        )
    except discord.Forbidden:
        await interaction.followup.send(
            "❌ I don't have permission to send messages in this channel.",
            ephemeral=True
        )
        return
    except discord.HTTPException:
        await interaction.followup.send(
            "❌ Discord rejected the faction panel.",
            ephemeral=True
        )
        return

    await interaction.followup.send(
        "✅ Faction panel sent.",
        ephemeral=True
    )


def setup(bot):
    bot.add_view(
        FactionView()
    )
