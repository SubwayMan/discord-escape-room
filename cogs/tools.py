import discord


def admin_command():
    """Decorator used to mark a slash command as
    admin-only."""
    pass


def inspect_guild(guild: discord.Guild):
    """Verifies the integrity of a guild's escape room components,
    or whether or not they exist."""
    status = {
        "RoomCategoryExists": False,
        "RoomIntegrity": 0,
        "RoleIntegrity": 0
    }



