from channels.layers import get_channel_layer


class WebSocketBroadcaster:
    def __init__(self, group_name="obs_group"):
        self.group_name = group_name
        self.channel_layer = get_channel_layer()

    async def broadcast(self, event_type: str, payload: dict):
        await self.channel_layer.group_send(
            self.group_name,
            {"type": "obs.message", "data": {"type": event_type, "payload": payload}},
        )
