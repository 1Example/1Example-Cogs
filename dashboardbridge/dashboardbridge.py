import json
import logging
import typing as t

import discord
import wtforms
from redbot.core import Config, checks, commands
from redbot.core.bot import Red

log = logging.getLogger("red.dashboardbridge")

# --- Exact pattern taken from a live, working third-party integration
# (vertyco/vrt-cogs -> levelup/dashboard/integration.py) that is already
# registered on this bot. This is the piece that actually plugs a cog
# into the Dashboard's "Third Parties" system.


def dashboard_page(*args: t.Any, **kwargs: t.Any) -> t.Callable[[t.Any], t.Any]:
    def decorator(func: t.Callable) -> t.Callable[[t.Any], t.Any]:
        func.__dashboard_decorator_params__ = (args, kwargs)
        return func

    return decorator


class DashboardIntegration:
    bot: Red

    @commands.Cog.listener()
    async def on_dashboard_cog_add(self, dashboard_cog: commands.Cog) -> None:
        log.info("Dashboard cog found, registering DashboardBridge as a third party.")
        dashboard_cog.rpc.third_parties_handler.add_third_party(self)


# --- helpers for turning arbitrary Config data into an editable web form


def _build_dynamic_form(data: t.Dict[str, t.Any]) -> t.Type[wtforms.Form]:
    """Builds a WTForms form on the fly from a flat dict of settings.

    Bools become dropdowns, ints/floats become number fields, short strings
    become text fields, and anything else (lists/dicts/long strings) falls
    back to a JSON textarea so nothing is silently dropped.
    """
    fields: t.Dict[str, t.Any] = {}
    for key, value in data.items():
        if isinstance(value, bool):
            fields[key] = wtforms.SelectField(
                key,
                choices=[("true", "True"), ("false", "False")],
                default="true" if value else "false",
            )
        elif isinstance(value, int) and not isinstance(value, bool):
            fields[key] = wtforms.IntegerField(key, default=value)
        elif isinstance(value, float):
            fields[key] = wtforms.FloatField(key, default=value)
        elif isinstance(value, str) and len(value) <= 200:
            fields[key] = wtforms.StringField(key, default=value)
        else:
            # dict, list, or long string: edit as raw JSON
            fields[key] = wtforms.TextAreaField(key, default=json.dumps(value, indent=2))
    fields["submit"] = wtforms.SubmitField("Save")
    return type("DynamicSettingsForm", (wtforms.Form,), fields)


def _coerce_back(original: t.Any, new_raw: str) -> t.Any:
    """Converts a submitted form value back to the original data's type."""
    if isinstance(original, bool):
        return new_raw == "true"
    if isinstance(original, int) and not isinstance(original, bool):
        return int(new_raw)
    if isinstance(original, float):
        return float(new_raw)
    if isinstance(original, str) and len(original) <= 200:
        return new_raw
    # JSON fallback for dict/list/long string
    return json.loads(new_raw)


class DashboardBridge(DashboardIntegration, commands.Cog):
    """Generic Dashboard settings pages for cogs that don't ship their own."""

    __author__ = "You"
    __version__ = "1.0.0"

    def __init__(self, bot: Red) -> None:
        self.bot = bot
        self.config = Config.get_conf(self, identifier=987654321012345, force_registration=True)
        self.config.register_global(bridged_cogs=[])

    async def red_delete_data_for_user(self, **kwargs) -> None:
        return

    # ---------- Discord-side management commands ----------

    @commands.group()
    @checks.is_owner()
    async def dashboardbridge(self, ctx: commands.Context) -> None:
        """Manage which cogs are exposed on the Dashboard via DashboardBridge."""

    @dashboardbridge.command(name="add")
    async def dashboardbridge_add(self, ctx: commands.Context, cog_name: str) -> None:
        """Expose a loaded cog's guild settings on the Dashboard.

        `cog_name` must match the cog's class name exactly, e.g. `Welcome`,
        `ExtendedModLog`, `RoleTools`. Use `[p]cogs` if you're unsure of the
        exact casing.
        """
        if self.bot.get_cog(cog_name) is None:
            await ctx.send(
                f"No loaded cog named `{cog_name}` was found. Check the exact name with `{ctx.prefix}cogs`."
            )
            return
        async with self.config.bridged_cogs() as bridged:
            if cog_name not in bridged:
                bridged.append(cog_name)
        await ctx.send(
            f"`{cog_name}` will now show up under Third Parties -> DashboardBridge on the Dashboard."
        )

    @dashboardbridge.command(name="remove")
    async def dashboardbridge_remove(self, ctx: commands.Context, cog_name: str) -> None:
        """Stop exposing a cog's settings on the Dashboard."""
        async with self.config.bridged_cogs() as bridged:
            if cog_name in bridged:
                bridged.remove(cog_name)
                await ctx.send(f"`{cog_name}` removed.")
            else:
                await ctx.send(f"`{cog_name}` wasn't bridged.")

    @dashboardbridge.command(name="list")
    async def dashboardbridge_list(self, ctx: commands.Context) -> None:
        """List cogs currently exposed on the Dashboard."""
        bridged = await self.config.bridged_cogs()
        if not bridged:
            await ctx.send("No cogs are bridged yet. Add one with `dashboardbridge add <CogName>`.")
            return
        await ctx.send("Bridged cogs:\n" + "\n".join(f"- {c}" for c in bridged))

    # ---------- Dashboard pages ----------

    @dashboard_page(name=None, description="Overview of bridged cogs.")
    async def dashboard_overview(
        self, user: discord.User, guild: discord.Guild, **kwargs
    ) -> t.Dict[str, t.Any]:
        bridged = await self.config.bridged_cogs()
        rows = "".join(
            f'<tr><td>{c}</td>'
            f'<td><a href="{{{{DASHBOARD_URL}}}}/{guild.id}/third-party/DashboardBridge/settings?cog={c}">'
            f"Configure</a></td></tr>"
            for c in bridged
            if self.bot.get_cog(c) is not None
        )
        source = (
            "<h4>Bridged cogs</h4>"
            "<table class='table'><thead><tr><th>Cog</th><th></th></tr></thead>"
            f"<tbody>{rows or '<tr><td colspan=2>None configured yet.</td></tr>'}</tbody></table>"
        )
        return {"status": 0, "web_content": {"source": source}}

    @dashboard_page(name="settings", description="Edit a bridged cog's settings.", methods=("GET", "POST"))
    async def dashboard_settings(
        self, user: discord.User, guild: discord.Guild, cog: str = None, **kwargs
    ) -> t.Dict[str, t.Any]:
        if not cog:
            return {"status": 1, "message": "No cog specified. Use ?cog=<CogName>."}

        target = self.bot.get_cog(cog)
        if target is None or not hasattr(target, "config"):
            return {"status": 1, "message": f"`{cog}` isn't loaded or doesn't expose a `.config` attribute."}

        target_config: Config = target.config
        data = await target_config.guild(guild).all()
        if not data:
            return {"status": 0, "web_content": {"source": f"<p>{cog} has no guild settings to show.</p>"}}

        FormClass = _build_dynamic_form(data)
        form = FormClass(data=kwargs.get("form_data"))

        if kwargs.get("request_method") == "POST" and form.validate():
            for key, original_value in data.items():
                submitted = getattr(form, key).data
                try:
                    new_value = _coerce_back(original_value, str(submitted))
                except (ValueError, json.JSONDecodeError) as exc:
                    return {"status": 1, "message": f"Couldn't save `{key}`: {exc}"}
                await target_config.guild(guild).set_raw(key, value=new_value)
            return {
                "status": 0,
                "notifications": [{"message": f"{cog} settings saved.", "category": "success"}],
            }

        fields_html = "".join(
            f"<div class='form-group'>{getattr(form, key).label} {getattr(form, key)()}</div>"
            for key in data.keys()
        )
        source = f"<h4>{cog} settings</h4><form method='POST'>{fields_html}{form.submit()}</form>"
        return {"status": 0, "web_content": {"source": source}}
