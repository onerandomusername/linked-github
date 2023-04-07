from __future__ import annotations

from typing import TYPE_CHECKING

import httpx
from starlite import Starlite
from starlite.openapi.config import OpenAPIConfig

from role_linker.endpoints import continue_oauth_flow, start_oauth_flow
from role_linker.env import DISCORD_BOT_TOKEN, DISCORD_CLIENT_ID
from role_linker.utils import get_metadata


if TYPE_CHECKING:
    from starlite.datastructures import State


def register_metadata(state: State) -> None:
    """Register app metadata with Discord on startup."""
    metadata = get_metadata()
    payload = [m.to_dict() for m in metadata]
    headers = {"Authorization": f"Bot {DISCORD_BOT_TOKEN}"}
    resp = httpx.put(
        f"https://discord.com/api/v10/applications/{DISCORD_CLIENT_ID}/role-connections/metadata",
        json=payload,
        headers=headers,
    )
    resp.raise_for_status()


app = Starlite(
    route_handlers=[start_oauth_flow, continue_oauth_flow],
    on_startup=[register_metadata],
    openapi_config=OpenAPIConfig(
        title="Discord Role Links",
        version="0.0.0",
        tags=[],
    ),
)
