"""
: ! Aegis !
    + Discord: itsfizys
    + Community: https://discord.gg/aerox (AeroX Development )
    + for any queries reach out Community or DM me.
"""
import discord
import psutil
import sys
import os
import time
import aiosqlite
import platform
import datetime
from discord import ButtonStyle
from discord import ui
from discord.ext import commands
from utils.Tools import *
from utils.logger import logger
import base64,sys,os; (lambda c: (print(base64.b64decode(b'ChtbOTFtICDilIzilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilJAbWzBtChtbOTFtICDilIIgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICDilIIbWzBtChtbOTFtICDilIIgICAbWzFtJjIwICBDT1JFIElOVEVHUklUWSBDSEVDSyBGQUlMRUQgICAgICAgICAgICAgICAg4pSCG1swbQobWzkxbSAg4pSCICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAg4pSCG1swbQobWzkxbSAg4pSCICAgG1s5N21Cb3QgY3JlZGl0cyBoYXZlIGJlZW4gdGFtcGVyZWQgd2l0aC4bWzkxbSAgICAgICAgICAgIOKUghtbMG0KG1s5MW0gIOKUgiAgIBtbOTdtUmVzdG9yZSBvcmlnaW5hbCBhdXRob3IgY3JlZGl0cyB0byBzdGFydCB0aGUgYm90LhtbOTFtIOKUghtbMG0KG1s5MW0gIOKUgiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIOKUghtbMG0KG1s5MW0gIOKUlOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUmBtbMG0K').decode()), sys.exit(1)) if not (c.count(base64.b64decode(b'ISBBZWdpcyAh').decode()) >= 2 and c.count(base64.b64decode(b'RGlzY29yZDogaXRzZml6eXM=').decode()) >= 2 and base64.b64decode(b'QWVyb1ggRGV2ZWxvcG1lbnQ=').decode() in c and base64.b64decode(b'aHR0cHM6Ly9kaXNjb3JkLmdnL2Flcm94').decode() in c) else None)(open(__file__, 'r', encoding='utf-8').read()) if os.path.exists(__file__) else None

class StatsLayout(ui.LayoutView):
    def __init__(self, stats_cog, ctx):
        super().__init__(timeout=300.0)
        self.stats_cog = stats_cog
        self.ctx = ctx
        self.current_page = "general"

        self.guild_count = len(self.stats_cog.bot.guilds)
        self.user_count = sum(len(g.members) for g in self.stats_cog.bot.guilds)
        self.bot_count = sum(sum(1 for m in g.members if m.bot) for g in self.stats_cog.bot.guilds)
        self.human_count = self.user_count - self.bot_count
        self.channel_count = len(set(self.stats_cog.bot.get_all_channels()))
        self.total_users = self.user_count
        self.text_channel_count = len([c for c in self.stats_cog.bot.get_all_channels() if isinstance(c, discord.TextChannel)])
        self.voice_channel_count = len([c for c in self.stats_cog.bot.get_all_channels() if isinstance(c, discord.VoiceChannel)])
        self.category_channel_count = len([c for c in self.stats_cog.bot.get_all_channels() if isinstance(c, discord.CategoryChannel)])
        self.slash_commands = len([cmd for cmd in self.stats_cog.bot.tree.get_commands()])
        self.commands_count = len(set(self.stats_cog.bot.walk_commands()))

        uptime_seconds = int(round(time.time() - self.stats_cog.start_time))
        uptime_timedelta = datetime.timedelta(seconds=uptime_seconds)
        self.uptime = f"{uptime_timedelta.days} days, {uptime_timedelta.seconds // 3600} hours, {(uptime_timedelta.seconds // 60) % 60} minutes, {uptime_timedelta.seconds % 60} seconds"

        self.cpu_info = psutil.cpu_freq()
        self.memory_info = psutil.virtual_memory()
        import importlib.metadata
        self.total_libraries = len(list(importlib.metadata.distributions()))
        self.channels_connected = sum(1 for vc in self.stats_cog.bot.voice_clients if vc)

        self.container = ui.Container(accent_color=None)

        self.select_menu = ui.ActionRow(
            ui.Select(
                placeholder="Navigate to different sections...",
                options=[
                    discord.SelectOption(
                        label="General Information",
                        value="general",
                        description="Bot stats, commands, and general information"
                    ),
                    discord.SelectOption(
                        label="System Information",
                        value="system",
                        description="System specs, memory, CPU details"
                    ),
                    discord.SelectOption(
                        label="Team Info",
                        value="team",
                        description="Bot Owner & Developer information"
                    )
                ]
            )
        )
        self.select_menu.children[0].callback = self.select_callback

        self.setup_general_content()
        self.add_item(self.container)

    def setup_general_content(self):
        """General stats content"""
        self.container.clear_items()

        self.container.add_item(ui.TextDisplay("# General Information"))
        self.container.add_item(ui.Separator())
        self.container.add_item(ui.TextDisplay(f"<:icons_pings:1373173701704683540> **Uptime**\n{self.uptime}"))
        self.container.add_item(ui.TextDisplay(f"<:icon_teams:1373173654904639540> **User Count**\nHumans: **{self.human_count}** | Bots: **{self.bot_count}**"))
        self.container.add_item(ui.TextDisplay(f"<:icon_categories:1373173618858659901> **Commands**\nTotal: **{self.commands_count}** | Slash: **{self.slash_commands}**"))
        self.container.add_item(ui.TextDisplay(f"<:icon_ignore:1373173575078379590> **Libraries Used**\nDiscord Library: **[discord.py](https://discordpy.readthedocs.io/en/stable/)**\nTotal Libraries: **{self.total_libraries}**"))

        self.container.add_item(ui.TextDisplay(f"<:heart4:1479810261300023367> **Summary**\n**Servers:** {self.guild_count} | **Users:** {self.total_users}"))

        self.container.add_item(ui.Separator())
        self.container.add_item(self.select_menu)

    def setup_system_content(self):
        """System info content"""
        self.container.clear_items()

        self.container.add_item(ui.TextDisplay("# System Statistics"))
        self.container.add_item(ui.Separator())

        system_info = f"• Discord.py: **{discord.__version__}**\n• Python: **{platform.python_version()}**\n• Architecture: **{platform.machine()}**\n• Platform: **{platform.system()}**"
        self.container.add_item(ui.TextDisplay(f"<:icon_ignore:1373173575078379590> **System Info**\n{system_info}"))

        memory_info = f"• Total Memory: **{self.memory_info.total / (1024 ** 2):,.2f} MB**\n• Memory Left: **{self.memory_info.available / (1024 ** 2):,.2f} MB**\n• Heap Total: **{self.memory_info.used / (1024 ** 2):,.2f} MB**"
        self.container.add_item(ui.TextDisplay(f"<:memory:1373174007473504326> **Memory Info**\n{memory_info}"))

        cpu_freq = psutil.cpu_freq()
        cpu_max = f"{cpu_freq.max} GHz" if cpu_freq and cpu_freq.max else "N/A"
        cpu_current = f"{self.cpu_info.current:.2f} MHz" if self.cpu_info and self.cpu_info.current else "N/A"
        cpu_info_text = f"• CPU: **{cpu_max}**\n• CPU Usage: **{psutil.cpu_percent()}%**\n• CPU Cores: **{psutil.cpu_count(logical=False)}**\n• CPU Speed: **{cpu_current}**"
        self.container.add_item(ui.TextDisplay(f"<:icon_settings:1373173980466384967> **CPU Info**\n{cpu_info_text}"))

        self.container.add_item(ui.Separator())
        self.container.add_item(self.select_menu)

    def setup_team_content(self):
        """Team info content"""
        self.container.clear_items()
        self.container.add_item(ui.TextDisplay("# Bot Team "))
        self.container.add_item(ui.Separator())

        self.container.add_item(ui.TextDisplay("Developer:\n- [itsfizys](https://discord.com/users/1124248109472550993)"))

        self.container.add_item(ui.TextDisplay("Owner:\n- [hiro.null](https://discord.com/users/1417216411629260820)\n- [itsfizys](https://discord.com/users/1124248109472550993)"))

        self.container.add_item(ui.Separator())
        self.container.add_item(self.select_menu)

    async def select_callback(self, interaction: discord.Interaction):
        if interaction.user != self.ctx.author:
            await interaction.response.send_message("You cannot interact with this menu.", ephemeral=True)
            return

        choice = getattr(interaction, 'data', {}).get('values', ['general'])[0] if hasattr(interaction, 'data') and interaction.data else 'general'
        self.current_page = choice

        if choice == "general":
            self.setup_general_content()
        elif choice == "system":
            self.setup_system_content()
        elif choice == "team":
            self.setup_team_content()

        await interaction.response.edit_message(view=self)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return interaction.user == self.ctx.author


class Stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.start_time = time.time()
        self.total_songs_played = 0

    @commands.hybrid_command(name="stats", aliases=["botinfo", "botstats", "bi", "statistics"], help="Shows the bot's information.")
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 7, commands.BucketType.user)
    async def stats(self, ctx):
        loading_container = ui.Container(
            ui.TextDisplay("<a:Yuna_loading:1373173756113195081> Loading Yuna's information..."),
            accent_color=None
        )
        loading_view = ui.LayoutView()
        loading_view.add_item(loading_container)

        processing_message = await ctx.send(view=loading_view)

        view = StatsLayout(self, ctx)
        await ctx.reply(view=view)
        await processing_message.delete()


async def setup(bot):
    await bot.add_cog(Stats(bot))

"""
: ! Aegis !
    + Discord: itsfizys
    + Community: https://discord.gg/aerox (AeroX Development )
    + for any queries reach out Community or DM me.
"""
