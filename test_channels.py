import os
import django
import asyncio

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'SkillSwap.settings'
)

django.setup()

from channels.layers import get_channel_layer


async def test_channels():

    channel_layer = get_channel_layer()

    print("Channel layer:")
    print(channel_layer)

    print("Testing Redis channel layer...")

    await channel_layer.group_add(
        "test_room",
        "test_channel"
    )

    print("GROUP ADD: SUCCESS")

    await channel_layer.group_send(
        "test_room",
        {
            "type": "test.message",
            "message": "Hello Redis"
        }
    )

    print("GROUP SEND: SUCCESS")

    await channel_layer.group_discard(
        "test_room",
        "test_channel"
    )

    print("GROUP DISCARD: SUCCESS")


asyncio.run(
    test_channels()
)