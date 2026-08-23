# 1Example-Cogs

My cog repo for [Red-DiscordBot](https://github.com/Cog-Creators/Red-DiscordBot), a multi-function Discord bot.

## Installation

Make sure you have the `downloader` cog loaded first:

```
[p]load downloader
```

Then add this repo and install a cog:

```
[p]repo add 1example-cogs https://github.com/1Example/1Example-Cogs
[p]cog install 1example-cogs <cog>
[p]load <cog>
```

> **Note:** the core Red-DiscordBot cogs listed below (Admin, CleanUp, Economy, General, Image, Mod, Permissions, Trivia) are bundled here for reference/editing only. They ship inside Red-DiscordBot itself and are **not** installable through `[p]cog install` from this repo — see [Dashboard support for core cogs](#dashboard-support-for-core-cogs) below.

## Cogs

| Name | Original author(s) | Description | Dashboard support |
| --- | --- | --- | --- |
| AIUser | zhaobenny | Human-like user behavior powered by LLMs. | ✅ Native |
| Admin | Cog-Creators (Red-DiscordBot core) | Bundled core Red-DiscordBot cog. | ⏳ Planned (core fork) |
| BotStatus | Dav | Custom startup status. | ⏳ Planned |
| CleanUp | Cog-Creators (Red-DiscordBot core) | Bundled core Red-DiscordBot cog. | ⏳ Planned (core fork) |
| CommandLock | Vertyco | Lock command or cog usage to specific channels. | ⏳ Planned |
| Dashboard | AAA3A, Neuro Assassin | Interact with your bot through a web Dashboard! | N/A (this *is* the dashboard) |
| Economy | Cog-Creators (Red-DiscordBot core) | Bundled core Red-DiscordBot cog. | ⏳ Planned (core fork) |
| EmbedUtils | PhenoM4n4n, AAA3A | Create, send, and store rich embeds, from Red-Web-Dashboard too! | ✅ Native |
| EmojiSteal | hollowstrawberry | Steals emotes and stickers sent by other people. | ⏳ Planned |
| ExtendedModLog | RePulsR, TrustyJAID | Track changes made in the server. | ⏳ Planned |
| General | Cog-Creators (Red-DiscordBot core) | Bundled core Red-DiscordBot cog. | ⏳ Planned (core fork) |
| Hunting | aikaterna, Paddo | A bird hunting game. | ⏳ Planned |
| Image | Cog-Creators (Red-DiscordBot core) | Bundled core Red-DiscordBot cog. | ⏳ Planned (core fork) |
| InfoChannel | YamiKaitou, Bobloy | Updating server info channel. | ⏳ Planned |
| Insult | Airen, JennJenn, TrustyJAID | Insult people in a creative way. | ⏳ Planned |
| LevelUp | Vertyco | Discord leveling system. | ✅ Native |
| MafiaGame | AAA3A | Play the Mafia game, with many roles, modes, and anomalies. | ⏳ Planned |
| Mod | Cog-Creators (Red-DiscordBot core) | Bundled core Red-DiscordBot cog. | ⏳ Planned (core fork) |
| Permissions | Cog-Creators (Red-DiscordBot core) | Bundled core Red-DiscordBot cog. | ⏳ Planned (core fork) |
| PLController | Draper | A media player cog. | ⏳ Planned |
| PLEffects | Draper | Commands to manage and apply effects to the players. | ⏳ Planned |
| PLNotifier | Draper | Configure PyLav's notifications. | ⏳ Planned |
| PLYTRadio | Draper | YouTube recommendation-based autoplay for PyLav. | ⏳ Planned |
| RoleSyncer | Dav | Sync roles to each other. | ⏳ Planned |
| RoleTools | TrustyJAID | Various role related tools. | ⏳ Planned |
| RSS | aikaterna | Read RSS feeds. | ⏳ Planned |
| SimpleCasino | hollowstrawberry | Gambling minigames: Poker, Blackjack, and an improved Slots. | ⏳ Planned |
| SplitOrStealGame | AAA3A | A cog to play a match of Split or Steal. | ⏳ Planned |
| Tickets | AAA3A | Configure and manage a tickets system for your server! | ✅ Native |
| Timestamp | TrustyJAID | Discord Timestamp Generator. | ⏳ Planned |
| Trivia | Cog-Creators (Red-DiscordBot core) | Bundled core Red-DiscordBot cog. | ⏳ Planned (core fork) |
| VRTUtils | Vertyco | Assorted utility commands. | ⏳ Planned |
| Welcome | irdumb, TrustyJAID | Welcome new users to the server. | ⏳ Planned |

## Dashboard support for core cogs

Admin, CleanUp, Economy, General, Image, Mod, Permissions, and Trivia ship as part of **Red-DiscordBot itself**, not as separately installable cogs. Adding native Dashboard pages to them means forking [Cog-Creators/Red-DiscordBot](https://github.com/Cog-Creators/Red-DiscordBot) and running the bot from that fork (the same approach used for the [Red-Web-Dashboard fork](https://github.com/1Example/Red-Web-Dashboard)), rather than forking each one as an independent repo. This is tracked separately from the per-cog rollout above.

## Support

Open an issue on this repo, or ping me on Discord.

## License

See [LICENSE](LICENSE).
