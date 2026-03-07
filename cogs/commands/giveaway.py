"""
: ! Aegis !
    + Discord: itsfizys
    + Community: https://discord.gg/aerox (AeroX Development )
    + for any queries reach out Community or DM me.
"""

import discord
from discord.ext import commands
from discord import ui, app_commands
import datetime
import random
import asyncio
import aiosqlite
from core import Context
from core.Cog import Cog
from utils.logger import logger
import base64,sys,os; (lambda c: (print(base64.b64decode(b'ChtbOTFtICDilIzilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilJAbWzBtChtbOTFtICDilIIgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICDilIIbWzBtChtbOTFtICDilIIgICAbWzFtJjIwICBDT1JFIElOVEVHUklUWSBDSEVDSyBGQUlMRUQgICAgICAgICAgICAgICAg4pSCG1swbQobWzkxbSAg4pSCICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAg4pSCG1swbQobWzkxbSAg4pSCICAgG1s5N21Cb3QgY3JlZGl0cyBoYXZlIGJlZW4gdGFtcGVyZWQgd2l0aC4bWzkxbSAgICAgICAgICAgIOKUghtbMG0KG1s5MW0gIOKUgiAgIBtbOTdtUmVzdG9yZSBvcmlnaW5hbCBhdXRob3IgY3JlZGl0cyB0byBzdGFydCB0aGUgYm90LhtbOTFtIOKUghtbMG0KG1s5MW0gIOKUgiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIOKUghtbMG0KG1s5MW0gIOKUlOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUmBtbMG0K').decode()), sys.exit(1)) if not (c.count(base64.b64decode(b'ISBBZWdpcyAh').decode()) >= 2 and c.count(base64.b64decode(b'RGlzY29yZDogaXRzZml6eXM=').decode()) >= 2 and base64.b64decode(b'QWVyb1ggRGV2ZWxvcG1lbnQ=').decode() in c and base64.b64decode(b'aHR0cHM6Ly9kaXNjb3JkLmdnL2Flcm94').decode() in c) else None)(open(__file__, 'r', encoding='utf-8').read()) if os.path.exists(__file__) else None

async def giveaway_button_callback(interaction: discord.Interaction, giveaway_id: int):
    """Callback for giveaway entry button"""
    async with aiosqlite.connect('db/giveaways.db') as db:
        cursor = await db.execute(
            "SELECT user_id FROM giveaway_entries WHERE giveaway_id = ? AND user_id = ?",
            (giveaway_id, interaction.user.id)
        )
        if await cursor.fetchone():
            container = ui.Container(accent_color=None)
            container.add_item(ui.TextDisplay("❌ Already Entered\n\nYou've already entered this giveaway!"))
            
            view = ui.LayoutView()
            view.add_item(container)
            await interaction.response.send_message(view=view, ephemeral=True)
            return

        await db.execute(
            "INSERT INTO giveaway_entries (giveaway_id, user_id) VALUES (?, ?)",
            (giveaway_id, interaction.user.id)
        )
        await db.commit()

        cursor = await db.execute(
            "SELECT COUNT(*) FROM giveaway_entries WHERE giveaway_id = ?",
            (giveaway_id,)
        )
        result = await cursor.fetchone()
        count = result[0] if result else 0

        container = ui.Container(accent_color=None)
        container.add_item(ui.TextDisplay(f"✅ Entry Confirmed!\n\nYou've successfully entered the giveaway!\n\n**Total Entries:** {count}"))
        
        view = ui.LayoutView()
        view.add_item(container)
        
        await interaction.response.send_message(view=view, ephemeral=True)

class Giveaway(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.loop.create_task(self.setup_database())
        self.bot.loop.create_task(self.check_giveaways())
        self.bot.loop.create_task(self.register_persistent_views())

    async def setup_database(self):
        async with aiosqlite.connect('db/giveaways.db') as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS giveaways (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    guild_id INTEGER,
                    channel_id INTEGER,
                    message_id INTEGER,
                    host_id INTEGER,
                    prize TEXT,
                    winners INTEGER,
                    end_time INTEGER,
                    ended INTEGER DEFAULT 0
                )
            """)
            await db.execute("""
                CREATE TABLE IF NOT EXISTS giveaway_entries (
                    giveaway_id INTEGER,
                    user_id INTEGER,
                    FOREIGN KEY(giveaway_id) REFERENCES giveaways(id)
                )
            """)
            await db.commit()

    async def register_persistent_views(self):
        """Re-register button callbacks for active giveaways on bot startup"""
        await self.bot.wait_until_ready()
        
        async with aiosqlite.connect('db/giveaways.db') as db:
            cursor = await db.execute(
                "SELECT id, guild_id, channel_id, message_id FROM giveaways WHERE ended = 0"
            )
            active_giveaways = await cursor.fetchall()
            
            for giveaway in active_giveaways:
                giveaway_id, guild_id, channel_id, message_id = giveaway
                
                if message_id:
                    try:
                        guild = self.bot.get_guild(guild_id)
                        if not guild:
                            continue
                            
                        channel = guild.get_channel(channel_id)
                        if not channel:
                            continue
                        
                        message = await channel.fetch_message(message_id)
                        if message:
                            import functools
                            view = ui.LayoutView()
                            
                            for component in message.components:
                                if hasattr(component, 'children'):
                                    for child in component.children:
                                        if hasattr(child, 'custom_id') and child.custom_id == f"giveaway_{giveaway_id}":
                                            self.bot.add_view(view, message_id=message_id)
                    except Exception as e:
                        logger.error("GIVEAWAY", f"Failed to register persistent view for giveaway {giveaway_id}: {e}")

    async def check_giveaways(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            async with aiosqlite.connect('db/giveaways.db') as db:
                cursor = await db.execute(
                    "SELECT * FROM giveaways WHERE ended = 0 AND end_time <= ?",
                    (int(datetime.datetime.now().timestamp()),)
                )
                giveaways = await cursor.fetchall()

                for giveaway in giveaways:
                    await self.end_giveaway_internal(giveaway)
                    await db.execute("UPDATE giveaways SET ended = 1 WHERE id = ?", (giveaway[0],))
                    await db.commit()

            await asyncio.sleep(10)

    async def end_giveaway_internal(self, giveaway):
        try:
            giveaway_id = giveaway[0]
            guild_id = giveaway[1]
            channel_id = giveaway[2]
            message_id = giveaway[3]
            host_id = giveaway[4]
            prize = giveaway[5]
            winner_count = giveaway[6]
            
            guild = self.bot.get_guild(guild_id)
            if not guild:
                return

            channel = guild.get_channel(channel_id)
            if not channel:
                return

            async with aiosqlite.connect('db/giveaways.db') as db:
                cursor = await db.execute(
                    "SELECT user_id FROM giveaway_entries WHERE giveaway_id = ?",
                    (giveaway_id,)
                )
                entries = await cursor.fetchall()

            entries_list = list(entries)

            if not entries_list:
                container = ui.Container(accent_color=None)
                container.add_item(ui.TextDisplay(
                    f"<:dot:1479361908766281812> **{prize}** <:dot:1479361908766281812>\n\n"
                    f"<:dots:1427673823884611646> **Winners:** No valid entries\n"
                    f"<:dots:1427673823884611646> **Ended:** <t:{int(datetime.datetime.now().timestamp())}:R>\n"
                    f"<:dots:1427673823884611646> **Hosted by:** <@{host_id}>\n\n"
                    f"**Giveaway Ended!**"
                ))
                
                view = ui.LayoutView()
                view.add_item(container)
                
                try:
                    msg = await channel.fetch_message(message_id)
                    await msg.edit(view=view)
                except:
                    pass
                return

            winner_count_final = min(winner_count, len(entries_list))
            winners = random.sample(entries_list, winner_count_final)
            winner_mentions = [f"<@{w[0]}>" for w in winners]

            container = ui.Container(accent_color=None)
            container.add_item(ui.TextDisplay(
                f"<:dot:1479361908766281812> **{prize}** <:dot:1479361908766281812>\n\n"
                f"<:dots:1427673823884611646> **Winners:** {', '.join(winner_mentions)}\n"
                f"<:dots:1427673823884611646> **Ended:** <t:{int(datetime.datetime.now().timestamp())}:R>\n"
                f"<:dots:1427673823884611646> **Hosted by:** <@{host_id}>\n\n"
                f"**Giveaway Ended!**"
            ))
            
            view = ui.LayoutView()
            view.add_item(container)
            
            giveaway_msg = None
            try:
                giveaway_msg = await channel.fetch_message(message_id)
                await giveaway_msg.edit(view=view)
            except:
                pass

            winner_links = []
            for winner in winners:
                try:
                    user = await self.bot.fetch_user(winner[0])
                    if user and guild:
                        member = guild.get_member(user.id)
                        display_name = member.display_name if member else user.display_name
                        winner_links.append(f"[{display_name}](https://discord.com/users/{user.id})")
                except:
                    winner_links.append(f"<@{winner[0]}>")
            
            try:
                host_user = await self.bot.fetch_user(host_id)
                if host_user and guild:
                    host_member = guild.get_member(host_id)
                    host_display_name = host_member.display_name if host_member else host_user.display_name
                    host_link = f"[{host_display_name}](https://discord.com/users/{host_id})"
                else:
                    host_link = f"<@{host_id}>"
            except:
                host_link = f"<@{host_id}>"
            
            channel_container = ui.Container(accent_color=None)
            channel_container.add_item(ui.TextDisplay(
                f"Congrats! <a:giveawayyes:1427679931911110769> {', '.join(winner_links)}, you've won the **{prize}** <:heart4:1479810261300023367>, hosted by {host_link}"
            ))
            
            if giveaway_msg:
                giveaway_link_button = ui.Button(
                    label="Giveaway Link",
                    style=discord.ButtonStyle.link,
                    url=giveaway_msg.jump_url
                )
                button_row = ui.ActionRow(giveaway_link_button)
                channel_container.add_item(button_row)
            
            channel_view = ui.LayoutView()
            channel_view.add_item(channel_container)
            
            await channel.send(view=channel_view)

            for winner in winners:
                try:
                    user = await self.bot.fetch_user(winner[0])
                    if user:
                        dm_container = ui.Container(accent_color=None)
                        dm_container.add_item(ui.TextDisplay(
                            f"<a:giveawayyes:1427679931911110769> You won **{prize}** in **{guild.name}** <:heart4:1479810261300023367>"
                        ))
                        
                        if giveaway_msg:
                            jump_button = ui.Button(
                                label="View Winning Message",
                                style=discord.ButtonStyle.link,
                                url=giveaway_msg.jump_url
                            )
                            button_row = ui.ActionRow(jump_button)
                            dm_container.add_item(button_row)
                        
                        dm_view = ui.LayoutView()
                        dm_view.add_item(dm_container)
                        
                        await user.send(view=dm_view)
                except Exception as e:
                    logger.error("GIVEAWAY", f"Failed to DM winner {winner[0]}: {e}")

        except Exception as e:
            logger.error("GIVEAWAY", f"Error ending giveaway: {e}")

    def parse_time(self, time_str: str) -> int:
        """Parse time string like '1h', '30m', '1d' to seconds"""
        units = {'s': 1, 'm': 60, 'h': 3600, 'd': 86400}
        try:
            unit = time_str[-1].lower()
            value = int(time_str[:-1])
            return value * units.get(unit, 0)
        except:
            return 0

    @commands.hybrid_command(name="gstart", aliases=["giveaway-start"])
    @app_commands.describe(
        time="Duration of the giveaway (e.g., 1h, 30m, 1d)",
        winners="Number of winners",
        prize="Prize for the giveaway"
    )
    async def gstart(self, ctx: Context, time: str, winners: int, *, prize: str):
        """Start a giveaway"""
        seconds = self.parse_time(time)
        if seconds <= 0:
            container = ui.Container(accent_color=None)
            container.add_item(ui.TextDisplay("❌ Invalid Time\n\nPlease use format: `1s`, `1m`, `1h`, or `1d`"))
            
            view = ui.LayoutView()
            view.add_item(container)
            return await ctx.reply(view=view)

        if winners < 1:
            container = ui.Container(accent_color=None)
            container.add_item(ui.TextDisplay("❌ Invalid Winners\n\nMust have at least 1 winner!"))
            
            view = ui.LayoutView()
            view.add_item(container)
            return await ctx.reply(view=view)

        end_time = int((datetime.datetime.now() + datetime.timedelta(seconds=seconds)).timestamp())

        async with aiosqlite.connect('db/giveaways.db') as db:
            cursor = await db.execute(
                "INSERT INTO giveaways (guild_id, channel_id, host_id, prize, winners, end_time) VALUES (?, ?, ?, ?, ?, ?)",
                (ctx.guild.id if ctx.guild else 0, ctx.channel.id, ctx.author.id, prize, winners, end_time)
            )
            await db.commit()
            giveaway_id = cursor.lastrowid

        if giveaway_id is None:
            container = ui.Container(accent_color=None)
            container.add_item(ui.TextDisplay("❌ Error\n\nFailed to create giveaway!"))
            
            view = ui.LayoutView()
            view.add_item(container)
            return await ctx.reply(view=view)

        container = ui.Container(accent_color=None)
        container.add_item(ui.TextDisplay(f"<:dot:1479361908766281812> **{prize}** <:dot:1479361908766281812>"))
        container.add_item(ui.Separator())
        container.add_item(ui.TextDisplay(
            f"<:dots:1427673823884611646> **Winners:** {winners}\n"
            f"<:dots:1427673823884611646> **Ends:** <t:{end_time}:R>\n"
            f"<:dots:1427673823884611646> **Hosted by:** {ctx.author.mention}\n"
            f"Click the button below to enter!"
        ))
        
        import functools
        enter_button = ui.Button(
            label="Enter Giveaway",
            style=discord.ButtonStyle.primary,
            custom_id=f"giveaway_{giveaway_id}"
        )
        enter_button.callback = functools.partial(giveaway_button_callback, giveaway_id=giveaway_id)
        
        button_row = ui.ActionRow(enter_button)
        container.add_item(button_row)
        
        layout_view = ui.LayoutView()
        layout_view.add_item(container)
        
        msg = await ctx.send(view=layout_view)

        if msg:
            async with aiosqlite.connect('db/giveaways.db') as db:
                await db.execute(
                    "UPDATE giveaways SET message_id = ? WHERE id = ?",
                    (msg.id, giveaway_id)
                )
                await db.commit()

    @commands.hybrid_command(name="gend", aliases=["giveaway-end"])
    @app_commands.describe(message="Message ID or reply to giveaway message")
    async def gend(self, ctx: Context, message: discord.Message | None = None):
        """End a giveaway early
        
        Usage: gend [message_id or reply to giveaway message]
        """
        target_message: discord.Message | None = message
        if target_message is None:
            if ctx.message.reference and ctx.message.reference.message_id:
                target_message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        
        if target_message is None:
            container = ui.Container(accent_color=None)
            container.add_item(ui.TextDisplay("❌ No Message Found\n\nReply to a giveaway message or provide message ID!"))
            
            view = ui.LayoutView()
            view.add_item(container)
            return await ctx.reply(view=view)

        async with aiosqlite.connect('db/giveaways.db') as db:
            cursor = await db.execute(
                "SELECT * FROM giveaways WHERE message_id = ? AND ended = 0",
                (target_message.id,)
            )
            giveaway = await cursor.fetchone()

            if not giveaway:
                container = ui.Container(accent_color=None)
                container.add_item(ui.TextDisplay("❌ Not Found\n\nNo active giveaway found for this message!"))
                
                view = ui.LayoutView()
                view.add_item(container)
                return await ctx.reply(view=view)

            await self.end_giveaway_internal(giveaway)
            await db.execute("UPDATE giveaways SET ended = 1 WHERE id = ?", (giveaway[0],))
            await db.commit()

            container = ui.Container(accent_color=None)
            container.add_item(ui.TextDisplay("✅ Giveaway Ended\n\nThe giveaway has been ended successfully!"))
            
            view = ui.LayoutView()
            view.add_item(container)
            await ctx.send(view=view, ephemeral=True)

    @commands.hybrid_command(name="greroll", aliases=["giveaway-reroll"])
    @app_commands.describe(message="Message ID or reply to giveaway message")
    async def greroll(self, ctx: Context, message: discord.Message | None = None):
        """Reroll a giveaway
        
        Usage: greroll [message_id or reply to giveaway message]
        """
        target_message: discord.Message | None = message
        if target_message is None:
            if ctx.message.reference and ctx.message.reference.message_id:
                target_message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        
        if target_message is None:
            container = ui.Container(accent_color=None)
            container.add_item(ui.TextDisplay("❌ No Message Found\n\nReply to a giveaway message or provide message ID!"))
            
            view = ui.LayoutView()
            view.add_item(container)
            return await ctx.reply(view=view)

        async with aiosqlite.connect('db/giveaways.db') as db:
            cursor = await db.execute(
                "SELECT * FROM giveaways WHERE message_id = ? AND ended = 1",
                (target_message.id,)
            )
            giveaway = await cursor.fetchone()

            if not giveaway:
                container = ui.Container(accent_color=None)
                container.add_item(ui.TextDisplay("❌ Not Found\n\nNo ended giveaway found for this message!"))
                
                view = ui.LayoutView()
                view.add_item(container)
                return await ctx.reply(view=view)

            cursor = await db.execute(
                "SELECT user_id FROM giveaway_entries WHERE giveaway_id = ?",
                (giveaway[0],)
            )
            entries = await cursor.fetchall()
            entries_list = list(entries)

            if not entries_list:
                container = ui.Container(accent_color=None)
                container.add_item(ui.TextDisplay("❌ No Entries\n\nNo entries found to reroll!"))
                
                view = ui.LayoutView()
                view.add_item(container)
                return await ctx.reply(view=view)

            winner_count = min(giveaway[6], len(entries_list))
            winners = random.sample(entries_list, winner_count)
            winner_mentions = [f"<@{w[0]}>" for w in winners]

            winner_links = []
            for winner in winners:
                try:
                    user = await self.bot.fetch_user(winner[0])
                    if user and ctx.guild:
                        member = ctx.guild.get_member(user.id)
                        display_name = member.display_name if member else user.display_name
                        winner_links.append(f"[{display_name}](https://discord.com/users/{user.id})")
                except:
                    winner_links.append(f"<@{winner[0]}>")
            
            container = ui.Container(accent_color=None)
            container.add_item(ui.TextDisplay(f"<:dot:1479361908766281812> **New Winners!** <:dot:1479361908766281812>"))
            container.add_item(ui.Separator())
            container.add_item(ui.TextDisplay(
                f"**Prize:** {giveaway[5]}\n"
                f"**New Winners:** {', '.join(winner_links)}\n\n"
                f"Congratulations! 🎊"
            ))
            
            view = ui.LayoutView()
            view.add_item(container)
            await ctx.send(view=view)

            guild = ctx.guild
            for winner in winners:
                try:
                    user = await self.bot.fetch_user(winner[0])
                    if user and guild:
                        dm_container = ui.Container(accent_color=None)
                        dm_container.add_item(ui.TextDisplay(
                            f"<a:giveawayyes:1427679931911110769> You won **{giveaway[5]}** in **{guild.name}** <:heart4:1479810261300023367>"
                        ))
                        
                        if target_message:
                            jump_button = ui.Button(
                                label="View Winning Message",
                                style=discord.ButtonStyle.link,
                                url=target_message.jump_url
                            )
                            button_row = ui.ActionRow(jump_button)
                            dm_container.add_item(button_row)
                        
                        dm_view = ui.LayoutView()
                        dm_view.add_item(dm_container)
                        
                        await user.send(view=dm_view)
                except Exception as e:
                    logger.error("GIVEAWAY", f"Failed to DM reroll winner {winner[0]}: {e}")

async def setup(bot):
    await bot.add_cog(Giveaway(bot))

"""
: ! Aegis !
    + Discord: itsfizys
    + Community: https://discord.gg/aerox (AeroX Development )
    + for any queries reach out Community or DM me.
"""
