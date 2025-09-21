import aiohttp


class TwitchOAuthClient:
    def __init__(self, client_id, client_secret, redirect_uri):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri

    def get_login_url(self, scopes):
        base_url = "https://id.twitch.tv/oauth2/authorize"
        scope_str = " ".join(scopes)
        return (
            f"{base_url}"
            f"?client_id={self.client_id}"
            f"&redirect_uri={self.redirect_uri}"
            f"&response_type=code"
            f"&scope={scope_str}"
        )

    async def fetch_token(self, code):
        url = "https://id.twitch.tv/oauth2/token"
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": self.redirect_uri,
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=data) as resp:
                return await resp.json()

    async def refresh_token(self, refresh_token):
        url = "https://id.twitch.tv/oauth2/token"
        data = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=data) as resp:
                return await resp.json()
