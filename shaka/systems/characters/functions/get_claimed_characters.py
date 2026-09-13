import mycord


db = mycord.DB()


def get_claimed_characters(guild_id):
    claims = db.fetchall("character_claims")

    return [
        claim
        for claim in claims
        if claim[0] == guild_id
    ]