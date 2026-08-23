from redbot.core.bot import Red

from .dashboardbridge import DashboardBridge


async def setup(bot: Red) -> None:
    await bot.add_cog(DashboardBridge(bot))
