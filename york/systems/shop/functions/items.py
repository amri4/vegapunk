from ....shaka.functions.bounty import add_bounty


def bounty(interaction, amount):
    add_bounty(
        interaction.guild.id,
        interaction.user.id,
        amount
    )