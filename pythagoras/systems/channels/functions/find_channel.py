import discord
import re
import unicodedata


def normalize(text):
    text = unicodedata.normalize("NFKC", text)
    text = text.lower()
    text = re.sub(r"[\u200b-\u200f\u202a-\u202e]", "", text)
    return text


def find_channel(guild, query):

    if guild is None:
        return None

    if not query:
        return None

    query = query.strip()

    # Channel mention: <#123456789>
    if query.startswith("<#") and query.endswith(">"):
        query = query[2:-1]

    # Channel ID
    if query.isdigit():
        channel = guild.get_channel(int(query))

        if channel:
            return channel

    # Remove # from normal names
    if query.startswith("#"):
        query = query[1:].strip()

    query = normalize(query)

    # Exact normalized name
    for channel in guild.channels:
        if normalize(channel.name) == query:
            return channel

    # Partial normalized name
    for channel in guild.channels:
        if query in normalize(channel.name):
            return channel

    return None