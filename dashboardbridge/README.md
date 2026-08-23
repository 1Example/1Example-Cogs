# DashboardBridge

Generic [Red-Web-Dashboard](https://github.com/AAA3A-AAA3A/Red-Web-Dashboard) settings pages for any loaded cog that doesn't ship its own Dashboard integration.

## What it does

Most cogs don't register a Dashboard "Third Party" page, so their settings can only be changed via Discord commands. DashboardBridge reads a target cog's public `.config` (Red's Config API) and auto-generates an editable settings form for it on the Dashboard, without modifying the target cog at all.

## Requirements

- The `Dashboard` cog (from AAA3A-cogs) must be loaded.
- Target cogs must expose their Config object as `self.config` (true for the large majority of Red cogs).

## Usage

```
[p]dashboardbridge add <CogName>
[p]dashboardbridge remove <CogName>
[p]dashboardbridge list
```

`<CogName>` is the cog's class name, e.g. `Welcome`, `ExtendedModLog`, `RoleTools`. Use `[p]cogs` if you're unsure of the exact spelling/casing.

Once added, the cog's settings appear under **Third Parties -> DashboardBridge** on the web dashboard.

## Notes / Known limitations

- Only guild-scope Config is exposed (not global, member, or channel scope) in this version.
- Nested values (lists/dicts) are edited as raw JSON text rather than dedicated widgets.
- The exact `web_content` return contract was written against the general Red-Web-Dashboard third-party convention. If saving doesn't work on your Dashboard version, check your Dashboard cog's version and open an issue with the error from your bot's console.

## Changelog

- **1.0.0** - Initial release.
