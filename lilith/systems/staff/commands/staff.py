import discord
from discord import app_commands

STAFF_RANKS = {
    "Head Administrator": 5,
    "Administrator": 4,
    "Senior Moderator": 3,
    "Moderator": 2,
    "Support Team": 1
}

staff_commands = app_commands.Group(name="staff", description="Community staff management")

staff_commands.command(name="add", description="add a member to the staff team")