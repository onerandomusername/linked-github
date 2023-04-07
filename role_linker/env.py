import environs
import yarl


env = environs.Env(eager=False)

env.read_env()
with env.prefixed("ROLE_LINKER_"):
    DISCORD_CLIENT_ID: int = env.int("DISCORD_CLIENT_ID")
    DISCORD_CLIENT_SECRET: str = env.str("DISCORD_CLIENT_SECRET")
    DISCORD_BOT_TOKEN: str = env.str("DISCORD_BOT_TOKEN")
    PUBLIC_URL: yarl.URL = yarl.URL(env.str("PUBLIC_URL", default="https://role_linker.arielle.codes/"))

    GITHUB_ORG: str = env.str("GITHUB_ORG")
    GITHUB_REPO: str = env.str("GITHUB_REPO")

    GITHUB_TOKEN: str = env.str("GITHUB_TOKEN", "")

env.seal()
