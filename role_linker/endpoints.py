# three endpoints are needed
# discord oauth2 callback

# github webhook hook for automatic syncing without requiring fetching

# optional:
# github oauth2 callback to be able to link not through discord
# discord interactions for an /unlink command which simply deletes the database record

# for an initial POC we are only implementing discord oauth2 callback and read the
# github user from their connections
# we then check GitHub to see if they're a contributor

import httpx
from starlite import Response, get
from starlite.params import Parameter
from starlite.response import RedirectResponse

from role_linker.env import DISCORD_CLIENT_ID, DISCORD_CLIENT_SECRET, GITHUB_REPO, PUBLIC_URL
from role_linker.utils import get_discord_oauth_url


@get("/discord-oauth/register")
def start_oauth_flow() -> Response:
    """Redirect the user to the discord oauth2 url."""
    url = get_discord_oauth_url(redirect_uri=PUBLIC_URL / "discord-oauth/callback", state="FIXME")
    return RedirectResponse(url, status_code=307)


@get("/discord-oauth/callback")
async def continue_oauth_flow(code: str, host: str = Parameter(header="Host")) -> Response:
    """Continue the oauth2 flow and validate with Discord."""
    # todo: break up this function
    redirect_url = "https://" + host + "/discord-oauth/callback"
    # this will be moved to an injection at some point
    # right now, this is the only function which uses it.
    client = httpx.AsyncClient()
    r = await client.post(
        "https://discord.com/api/v10/oauth2/token",
        data={
            "client_id": DISCORD_CLIENT_ID,
            "client_secret": DISCORD_CLIENT_SECRET,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": redirect_url,
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    r.raise_for_status()
    resp = r.json()

    token = resp["access_token"]
    token_type = resp["token_type"]
    scopes = resp["scope"].split(" ")
    for scope in ("role_connections.write", "connections", "identify"):
        if scope not in scopes:
            return Response("missing required scopes", status_code=403)

    headers = {"Authorization": f"{token_type} {token}"}

    r = await client.get("https://discord.com/api/v10/users/@me", headers=headers)
    r.raise_for_status()

    r.json()["id"]

    r = await client.get("https://discord.com/api/v10/users/@me/connections", headers=headers)
    r.raise_for_status()

    json = r.json()
    for conn in json:
        if conn["type"] == "github":
            conn["name"]
            break
    else:
        return Response("Please link a GitHub account to your Discord user.")

    r = await client.put(
        f"https://discord.com/api/v10/users/@me/applications/{DISCORD_CLIENT_ID}/role-connection",
        headers=headers,
        json={
            "platform_name": f"{GITHUB_REPO} Contributions",
            "metadata": {
                "commits": 4,
                "contributor": True,
                "maintainer": True,
                "merged_pull_requests": 16,
                "total_issues": 69,
            },
        },
    )
    r.raise_for_status()
    return Response("", status_code=200)
