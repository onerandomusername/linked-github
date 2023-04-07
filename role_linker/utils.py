from disnake import ApplicationRoleConnectionMetadata, ApplicationRoleConnectionMetadataType
from yarl import URL

from role_linker.env import DISCORD_CLIENT_ID, GITHUB_ORG, GITHUB_REPO


def get_metadata() -> list[ApplicationRoleConnectionMetadata]:
    """Get Discord Role Connection Metadata objects."""
    metadata = []
    metadata.append(
        ApplicationRoleConnectionMetadata(
            type=ApplicationRoleConnectionMetadataType.integer_greater_than_or_equal,
            key="commits",
            name="Commits",
            description=(f"Number of commits made to the GitHub repository {GITHUB_ORG}/{GITHUB_REPO}"),
        )
    )
    metadata.append(
        ApplicationRoleConnectionMetadata(
            type=ApplicationRoleConnectionMetadataType.boolean_equal,
            key="contributor",
            name="Contributor",
            description=f"Has made at least one contribution to {GITHUB_ORG}/{GITHUB_REPO}",
        )
    )
    metadata.append(
        ApplicationRoleConnectionMetadata(
            type=ApplicationRoleConnectionMetadataType.boolean_equal,
            key="maintainer",
            name="Maintainer",
            description=f"Maintainer of {GITHUB_ORG}/{GITHUB_REPO}",
        )
    )
    metadata.append(
        ApplicationRoleConnectionMetadata(
            type=ApplicationRoleConnectionMetadataType.integer_greater_than_or_equal,
            key="merged_pull_requests",
            name="Merged Pull Requests",
            description=f"Number of pull requests merged to {GITHUB_ORG}/{GITHUB_REPO}",
        )
    )
    metadata.append(
        ApplicationRoleConnectionMetadata(
            type=ApplicationRoleConnectionMetadataType.integer_greater_than_or_equal,
            key="total_issues",
            name="Issues Made",
            description=f"Number of issues made on {GITHUB_ORG}/{GITHUB_REPO}",
        )
    )
    return metadata


def get_discord_oauth_url(
    redirect_uri: str | URL,
    *,
    state: str,
    client_id: int = DISCORD_CLIENT_ID,
    scopes: list[str] | tuple[str, ...] = ("role_connections.write", "connections", "identify"),
    base_url: str = "https://discord.com/api/oauth2/authorize",
) -> str:
    """Get a Discord oauth2 url to send the user to Discord."""
    ret = URL(base_url)
    ret = ret.with_query(
        {
            "redirect_uri": str(redirect_uri),
            "client_id": str(client_id),
            "scope": " ".join(scopes),
            "state": state,
            "response_type": "code",
        }
    )
    return str(ret)
