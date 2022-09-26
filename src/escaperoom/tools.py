import discord


def false_perms():
    """Returns a dict with all discord channel
    permissions set to False."""
    return {
        "view_channel": False,
        "manage_channels": False,
        "manage_permissions": False,
        "manage_webhooks": False,
        "create_instant_invite": False,
        "send_messages": False,
        "send_messages_in_threads": False,
        "create_public_threads": False,
        "create_private_threads": False,
        "embed_links": False,
        "attach_files": False,
        "add_reactions": False,
        "external_emojis": False,
        "external_stickers": False,
        "mention_everyone": False,
        "manage_messages": False,
        "manage_threads": False,
        "read_message_history": False,
        "send_tts_messages": False,
        "use_application_commands": False
    }

def true_perms():
    """Opposite of false_perms."""
    return dict((k, not v) for k, v in false_perms())




