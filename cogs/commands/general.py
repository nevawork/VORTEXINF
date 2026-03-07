"""
: ! Aegis !
    + Discord: itsfizys
    + Community: https://discord.gg/aerox (AeroX Development )
    + for any queries reach out Community or DM me.
"""
import asyncio
import discord
from discord.ext import commands, tasks
from discord.utils import get
import datetime
import random
import requests
import aiohttp
import re
from discord.ext.commands.errors import BadArgument
from discord.ext.commands import Cog
from discord.colour import Color
import hashlib
from utils.Tools import *
from traceback import format_exception
import discord
from discord.ext import commands
import datetime
from discord import ButtonStyle
from discord.ui import Button, View
import psutil
import time
from datetime import datetime, timezone, timedelta
import sqlite3
from typing import *
import string
import io

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
from utils.Tools import*

lawda =[
'8','3821','23','21','313','43','29','76','11','9',
'44','470','318','26','69'
]


class UserinfoLayout(ui.LayoutView):
    def __init__(self, user, ctx):
        super().__init__(timeout=300.0)
        self.user = user
        self.ctx = ctx
        self.current_page = "general"

        self.member = ctx.guild.get_member(user.id) if ctx.guild else None
        self.is_bot = user.bot
        self.created_at = user.created_at
        self.joined_at = self.member.joined_at if self.member else None

        account_age = datetime.datetime.now(datetime.timezone.utc) - self.created_at
        self.account_age_days = account_age.days

        if self.joined_at:
            join_age = datetime.datetime.now(datetime.timezone.utc) - self.joined_at
            self.join_age_days = join_age.days
        else:
            self.join_age_days = None

        self.status = str(self.member.status) if self.member else "Unknown"
        self.activity = self.member.activity.name if self.member and self.member.activity else "None"

        if self.member:
            self.roles = [role for role in self.member.roles if role.name != "@everyone"]
            self.top_role = self.member.top_role
            self.role_count = len(self.roles)
        else:
            self.roles = []
            self.top_role = None
            self.role_count = 0

        self.is_admin = self.member.guild_permissions.administrator if self.member else False
        self.key_permissions = []
        if self.member:
            perms = self.member.guild_permissions
            if perms.administrator:
                self.key_permissions.append("Administrator")
            elif perms.manage_guild:
                self.key_permissions.append("Manage Server")
            elif perms.manage_channels:
                self.key_permissions.append("Manage Channels")
            elif perms.manage_roles:
                self.key_permissions.append("Manage Roles")
            elif perms.kick_members:
                self.key_permissions.append("Kick Members")
            elif perms.ban_members:
                self.key_permissions.append("Ban Members")

        self.container = ui.Container(accent_color=None)

        self.select_menu = ui.ActionRow(
            ui.Select(
                placeholder="Navigate to different sections...",
                options=[
                    discord.SelectOption(
                        label="General Information",
                        value="general",
                        description="Basic user information and account details"
                    ),
                    discord.SelectOption(
                        label="Server Information",
                        value="server",
                        description="Server-specific information and roles"
                    ),
                    discord.SelectOption(
                        label="Permissions & Status",
                        value="permissions",
                        description="User permissions and current status"
                    )
                ]
            )
        )
        self.select_menu.children[0].callback = self.select_callback

        self.setup_general_content()

        self.add_item(self.container)

    def setup_general_content(self):
        """Set up the general user info content"""
        self.container.clear_items()

        self.container.add_item(ui.TextDisplay(f"# User Information: {self.user.display_name}"))
        self.container.add_item(ui.Separator())

        user_type = "Bot" if self.is_bot else "User"
        self.container.add_item(ui.TextDisplay(f"**Username:** {self.user.name}\n**Display Name:** {self.user.display_name}\n**User ID:** {self.user.id}\n**Type:** {user_type}"))

        created_time = f"<t:{int(self.created_at.timestamp())}:F>"
        created_relative = f"<t:{int(self.created_at.timestamp())}:R>"
        self.container.add_item(ui.TextDisplay(f"**Account Created**\n{created_time}\n{created_relative}"))

        self.container.add_item(ui.TextDisplay(f"**Account Age**\n{self.account_age_days} days old"))

        avatar_url = self.user.display_avatar.url
        self.container.add_item(ui.TextDisplay(f"**Avatar**\n[View Avatar]({avatar_url})"))

        self.container.add_item(ui.Separator())
        self.container.add_item(self.select_menu)

    def setup_server_content(self):
        """Set up the server-specific content"""
        self.container.clear_items()

        self.container.add_item(ui.TextDisplay(f"# Server Information: {self.user.display_name}"))
        self.container.add_item(ui.Separator())

        if not self.member:
            self.container.add_item(ui.TextDisplay("**Status:** Not a member of this server"))
        else:
            if self.joined_at:
                joined_time = f"<t:{int(self.joined_at.timestamp())}:F>"
                joined_relative = f"<t:{int(self.joined_at.timestamp())}:R>"
                self.container.add_item(ui.TextDisplay(f"**Joined Server**\n{joined_time}\n{joined_relative}"))

                self.container.add_item(ui.TextDisplay(f"**Server Membership**\n{self.join_age_days} days in server"))

            if self.roles:
                role_list = ", ".join([role.mention for role in self.roles[:10]])
                if len(self.roles) > 10:
                    role_list += f" and {len(self.roles) - 10} more..."
                self.container.add_item(ui.TextDisplay(f"**Roles ({self.role_count})**\n{role_list}"))

                if self.top_role:
                    self.container.add_item(ui.TextDisplay(f"**Highest Role**\n{self.top_role.mention}"))
            else:
                self.container.add_item(ui.TextDisplay("**Roles**\nNo roles assigned"))

            if hasattr(self.member, 'premium_since') and self.member.premium_since:
                boost_time = f"<t:{int(self.member.premium_since.timestamp())}:R>"
                self.container.add_item(ui.TextDisplay(f"**Server Booster**\nBoosting since {boost_time}"))

        self.container.add_item(ui.Separator())
        self.container.add_item(self.select_menu)

    def setup_permissions_content(self):
        """Set up the permissions and status content"""
        self.container.clear_items()

        self.container.add_item(ui.TextDisplay(f"# Permissions & Status: {self.user.display_name}"))
        self.container.add_item(ui.Separator())

        if not self.member:
            self.container.add_item(ui.TextDisplay("**Status:** Not a member of this server"))
        else:
            status_emoji = {
                "online": "🟢",
                "idle": "🟡",
                "dnd": "🔴",
                "offline": "⚫"
            }
            status_display = f"{status_emoji.get(self.status, '⚫')} {self.status.title()}"
            self.container.add_item(ui.TextDisplay(f"**Current Status**\n{status_display}"))

            self.container.add_item(ui.TextDisplay(f"**Activity**\n{self.activity}"))

            if self.key_permissions:
                perms_text = ", ".join(self.key_permissions)
                self.container.add_item(ui.TextDisplay(f"**Key Permissions**\n{perms_text}"))
            else:
                self.container.add_item(ui.TextDisplay("**Key Permissions**\nNo special permissions"))

            admin_status = "Yes" if self.is_admin else "No"
            self.container.add_item(ui.TextDisplay(f"**Administrator**\n{admin_status}"))

            flags = []
            if self.member.guild_permissions.administrator:
                flags.append("Administrator")
            if hasattr(self.member, 'premium_since') and self.member.premium_since:
                flags.append("Server Booster")
            if self.user.bot:
                flags.append("Bot Account")

            if flags:
                self.container.add_item(ui.TextDisplay(f"**User Flags**\n{', '.join(flags)}"))

        self.container.add_item(ui.Separator())
        self.container.add_item(self.select_menu)

    async def select_callback(self, interaction: discord.Interaction):
        """Handle page selection from dropdown"""
        if interaction.user != self.ctx.author:
            await interaction.response.send_message("You cannot interact with this menu.", ephemeral=True)
            return

        choice = getattr(interaction, 'data', {}).get('values', ['general'])[0] if hasattr(interaction, 'data') and interaction.data else 'general'
        self.current_page = choice

        if choice == "general":
            self.setup_general_content()
        elif choice == "server":
            self.setup_server_content()
        elif choice == "permissions":
            self.setup_permissions_content()

        await interaction.response.edit_message(view=self)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return interaction.user == self.ctx.author

class General(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self._URL_REGEX = r'(?P<url><[^: >]+:\/[^ >]+>|(?:https?|steam):\/\/[^\s<]+[^<.,:;\"\'\]\s])'
        self.color = 0x000000

    @commands.hybrid_command(
        usage ="Avatar <member>",
        name ='avatar',
        aliases =['av'],
        help ="Get User avatar/Guild avatar & Banner of a user."
    )
    @blacklist_check()
    @ignore_check()
    @commands.cooldown (1 ,3 ,commands .BucketType .user )
    async def _user (self ,ctx ,member :Optional [Union [discord .Member ,discord .User ]]=None ):
        try :
            if member is None :
                member =ctx .author
            user =await self .bot .fetch_user (member .id )

            view = discord.ui.LayoutView()
            container = discord.ui.Container(accent_color=None)

            container.add_item(discord.ui.TextDisplay(f"👤 **{member.display_name}'s Avatar**"))

            if user.avatar:
                user_info = f"**Username:** {user.name}\n**Display Name:** {member.display_name if hasattr(member, 'display_name') else user.display_name}"
                container.add_item(discord.ui.TextDisplay(user_info))

                download_row = discord.ui.ActionRow()
                download_row.add_item(discord.ui.Button(
                    label="Download Avatar",
                    url=user.avatar.url,
                    style=discord.ButtonStyle.link
                ))
                container.add_item(download_row)

                avatar_gallery = discord.ui.MediaGallery()
                avatar_gallery.add_item(media=user.avatar.url)
                container.add_item(avatar_gallery)
            else:
                container.add_item(discord.ui.TextDisplay("❌ **No Custom Avatar**\nThis user is using Discord's default avatar."))

            view.add_item(container)
            await ctx .send (view=view)
        except Exception as e :
            print (f"Error: {e}")

    @commands.hybrid_command (
        name ="servericon",
        help ="Get the server icon",
        usage ="Servericon"
    )
    @blacklist_check ()
    @ignore_check ()
    @commands .cooldown (1 ,3 ,commands .BucketType .user )
    async def servericon (self ,ctx : commands .Context ):
        server =ctx .guild
        if server .icon is None :
            error_view = discord.ui.LayoutView()
            error_container = discord.ui.Container(
                discord.ui.TextDisplay("❌ **Server Icon**\n\nThis server does not have an icon set."),
                accent_color=None
            )
            error_view.add_item(error_container)
            await ctx.reply(view=error_view)
            return

        view = discord.ui.LayoutView()
        container = discord.ui.Container(accent_color=None)

        container.add_item(discord.ui.TextDisplay(f"# 🖼️ {server.name}'s Icon"))
        container.add_item(discord.ui.Separator())

        webp =server .icon .replace (format ='webp')
        jpg =server .icon .replace (format ='jpg')
        png =server .icon .replace (format ='png')

        format_links = f"[`PNG`]({png}) | [`JPG`]({jpg}) | [`WEBP`]({webp})"
        if server .icon .is_animated ():
            gif =server .icon .replace (format ='gif')
            format_links +=f" | [`GIF`]({gif})"

        container.add_item(
            discord.ui.Section(
                discord.ui.TextDisplay(f"**Download Links:**\n{format_links}\n\n**Server:** {server.name}\n**Icon URL:** [Direct Link]({server.icon.url})"),
                accessory=discord.ui.Thumbnail(server.icon.url)
            )
        )

        container.add_item(discord.ui.Separator())

        download_row = discord.ui.ActionRow()
        download_row.add_item(discord.ui.Button(label="Download Icon", url=server.icon.url, style=discord.ButtonStyle.link))
        container.add_item(download_row)

        container.add_item(discord.ui.Separator())

        icon_gallery = discord.ui.MediaGallery()
        icon_gallery.add_item(media=server.icon.url)
        container.add_item(icon_gallery)

        view.add_item(container)
        await ctx .send (view=view)

    @commands.hybrid_command (name ="membercount",
    help ="Get total member count of the server",
    usage ="membercount",
    aliases =["mc"])
    @blacklist_check ()
    @ignore_check ()
    @commands .cooldown (1 ,2 ,commands .BucketType .user )
    async def membercount (self ,ctx : commands .Context ):
        total_members =len (ctx .guild .members )
        total_humans =len ([member for member in ctx .guild .members if not member .bot ])
        total_bots =len ([member for member in ctx .guild .members if member .bot ])

        online =len ([member for member in ctx .guild .members if member .status ==discord .Status .online ])
        offline =len ([member for member in ctx .guild .members if member .status ==discord .Status .offline ])
        idle =len ([member for member in ctx .guild .members if member .status ==discord .Status .idle ])
        dnd =len ([member for member in ctx .guild .members if member .status ==discord .Status .do_not_disturb ])

        view = discord.ui.LayoutView()
        container = discord.ui.Container(accent_color=None)

        container.add_item(discord.ui.TextDisplay(f"# Member Statistics"))
        container.add_item(discord.ui.Separator())

        count_stats = f"**Total Members:** {total_members}\n**Humans:** {total_humans}\n**Bots:** {total_bots}"
        container.add_item(discord.ui.TextDisplay(f"**Count Statistics**\n{count_stats}"))

        container.add_item(discord.ui.Separator())

        presence_stats = f"<:dot:1479361908766281812>  **Online:** {online}\n<:dot:1479361908766281812>  **Do Not Disturb:** {dnd}\n<:dot:1479361908766281812>  **Idle:** {idle}\n<:dot:1479361908766281812>  **Offline:** {offline}"

        if ctx.guild.icon:
            container.add_item(
                discord.ui.Section(
                    discord.ui.TextDisplay(f"**Presence Statistics**\n{presence_stats}"),
                    accessory=discord.ui.Thumbnail(ctx.guild.icon.url)
                )
            )
        else:
            container.add_item(discord.ui.TextDisplay(f"**Presence Statistics**\n{presence_stats}"))

        container.add_item(discord.ui.Separator())

        summary = f"**Server:** {ctx.guild.name}\n**Updated:** <t:{int(time.time())}:R>"
        container.add_item(discord.ui.TextDisplay(summary))

        view.add_item(container)
        await ctx .send (view=view)

    @commands.hybrid_command (name ="poll",usage ="Poll <message>")
    @blacklist_check ()
    @ignore_check ()
    @commands .cooldown (1 ,3 ,commands .BucketType .user )
    async def poll (self ,ctx : commands .Context ,*,message ):
        view = discord.ui.LayoutView()
        container = discord.ui.Container(accent_color=None)

        container.add_item(discord.ui.TextDisplay(f"# 📊 Poll"))
        container.add_item(discord.ui.Separator())

        poll_content = f"**Question:** {message}\n\n**React below to vote!**"

        if ctx.author.avatar:
            container.add_item(
                discord.ui.Section(
                    discord.ui.TextDisplay(poll_content),
                    accessory=discord.ui.Thumbnail(ctx.author.avatar.url)
                )
            )
        else:
            container.add_item(discord.ui.TextDisplay(poll_content))

        container.add_item(discord.ui.Separator())

        instructions = f"<:icon_tick:1372375089668161597> **Yes/Agree**\n<:icon_cross:1372375094336425986> **No/Disagree**\n\n⏰ **Created:** <t:{int(time.time())}:R>"
        container.add_item(discord.ui.TextDisplay(f"**Voting Instructions:**\n{instructions}"))

        view.add_item(container)
        msg = await ctx .send (view=view)
        await msg .add_reaction ("<:icon_tick:1372375089668161597>")
        await msg .add_reaction ("<:icon_cross:1372375094336425986>")

    @commands .command (name ="hack",
    help ="hack someone's discord account",
    usage ="Hack <member>")
    @blacklist_check ()
    @ignore_check ()
    @commands .cooldown (1 ,3 ,commands .BucketType .user )
    async def hack (self ,ctx : commands .Context ,member : discord .Member ):
        loading_view = discord.ui.LayoutView()
        loading_container = discord.ui.Container(
            discord.ui.TextDisplay(f"🔓 **Hacking in progress...**\n\nTarget: {member.mention}\n\n<a:Yuna_loading:1373173756113195081> Processing hack attempt..."),
            accent_color=None
        )
        loading_view.add_item(loading_container)

        processing_msg = await ctx .send (view=loading_view)
        await asyncio .sleep (2 )

        stringi =member .name
        random_pass =random .choice (lawda )
        random_pass2 =''.join (random .choices (string .ascii_letters +string .digits ,k =3 ))

        view = discord.ui.LayoutView()
        container = discord.ui.Container(accent_color=None)

        container.add_item(discord.ui.TextDisplay(f"# 🔓 Hack Complete!"))
        container.add_item(discord.ui.Separator())

        hack_results = f"**Target User:** {member.mention}\n**Email:** {''.join(letter for letter in stringi if letter.isalnum())}{random_pass}@gmail.com\n**Password:** {member.name}@{random_pass2}\n\n⚠️ **This is fake data for entertainment purposes only!**"

        if member.avatar:
            container.add_item(
                discord.ui.Section(
                    discord.ui.TextDisplay(hack_results),
                    accessory=discord.ui.Thumbnail(member.avatar.url)
                )
            )
        else:
            container.add_item(discord.ui.TextDisplay(hack_results))

        container.add_item(discord.ui.Separator())

        footer_info = f"⏰ **Completed:** <t:{int(time.time())}:R>\n\n*Note: This is a joke command and does not perform actual hacking.*"
        container.add_item(discord.ui.TextDisplay(footer_info))

        view.add_item(container)
        await processing_msg.edit(view=view)

    @commands .command (name ="token",usage ="Token <member>")
    @blacklist_check ()
    @ignore_check ()
    @commands .cooldown (1 ,2 ,commands .BucketType .user )
    async def token (self ,ctx : commands .Context ,user : discord .Member =None ):
        if user is None:
            user = ctx.author

        char_list =[
        "A","B","C","D","E","F","G","H","I","J","K","L","M","N",
        "O","P","Q","R","S","T","U","V","W","X","Y","Z","_",
        'a','b','c','d','e','f','g','h','i','j','k','l','m','n',
        'ñ','o','p','q','r','s','t','u','v','w','x','y','z','0',
        '1','2','3','4','5','6','7','8','9'
        ]
        token =random .choices (char_list ,k =59 )
        fake_token = ''.join(token)

        view = discord.ui.LayoutView()
        container = discord.ui.Container(accent_color=None)

        container.add_item(discord.ui.TextDisplay(f"# 🔑 Discord Token"))
        container.add_item(discord.ui.Separator())

        token_info = f"**User:** [{user.display_name}](https://discord.com/users/{user.id})\n**Generated Token:**\n```{fake_token}```\n\n⚠️ **Warning:** This is a fake token for entertainment purposes!"

        if user.avatar:
            container.add_item(
                discord.ui.Section(
                    discord.ui.TextDisplay(token_info),
                    accessory=discord.ui.Thumbnail(user.avatar.url)
                )
            )
        else:
            container.add_item(discord.ui.TextDisplay(token_info))

        view.add_item(container)
        await ctx .send (view=view)

    @commands .command (name ="users",help ="checks total users of Yuna-bot.")
    @blacklist_check ()
    @ignore_check ()
    @commands .cooldown (1 ,3 ,commands .BucketType .user )
    async def users (self ,ctx : commands .Context ):
        users =sum (g .member_count for g in self .bot .guilds
        if g .member_count !=None )
        guilds =len (self .bot .guilds )

        view = discord.ui.LayoutView()
        container = discord.ui.Container(accent_color=None)

        container.add_item(discord.ui.TextDisplay(f"# 🤖 {self.bot.user.name} Statistics"))
        container.add_item(discord.ui.Separator())

        stats_content = f"**Total Users:** {users:,}\n**Total Servers:** {guilds:,}\n**Average Users per Server:** {users//guilds if guilds > 0 else 0:,}"

        if self.bot.user.avatar:
            container.add_item(
                discord.ui.Section(
                    discord.ui.TextDisplay(stats_content),
                    accessory=discord.ui.Thumbnail(self.bot.user.avatar.url)
                )
            )
        else:
            container.add_item(discord.ui.TextDisplay(stats_content))

        container.add_item(discord.ui.Separator())


        view.add_item(container)
        await ctx .send (view=view)

    @commands .command (name ="wizz",usage ="Wizz")
    @blacklist_check ()
    @ignore_check ()
    @commands .cooldown (1 ,3 ,commands .BucketType .user )
    async def wizz (self ,ctx : commands .Context ):
        loading_view = discord.ui.LayoutView()
        loading_container = discord.ui.Container(
            discord.ui.TextDisplay(f"⚡ **Wizzing {ctx.guild.name}**\n\n<a:Yuna_loading:1373173756113195081> Will take 22 seconds to complete..."),
            accent_color=None
        )
        loading_view.add_item(loading_container)

        processing_msg = await ctx.send(view=loading_view)

        steps = [
            "Changing all guild settings...",
            f"Deleting **{len(ctx.guild.roles)}** Roles...",
            f"Deleting **{len(ctx.guild.channels)}** Channels...",
            "Deleting Webhooks...",
            "Deleting emojis...",
            "Installing Ban Wave..."
        ]

        for step in steps:
            await asyncio.sleep(1)
            step_container = discord.ui.Container(
                discord.ui.TextDisplay(f"⚡ **Wizzing {ctx.guild.name}**\n\n<a:Yuna_loading:1373173756113195081> {step}"),
                accent_color=None
            )
            step_view = discord.ui.LayoutView()
            step_view.add_item(step_container)
            await processing_msg.edit(view=step_view)

        await asyncio.sleep(2)

        view = discord.ui.LayoutView()
        container = discord.ui.Container(accent_color=None)

        container.add_item(discord.ui.TextDisplay(f"# ⚡ {self.bot.user.name} Wizz Complete"))
        container.add_item(discord.ui.Separator())

        success_msg = f"<:icon_danger:1373170993236803688> **Successfully Wizzed {ctx.guild.name}**\n\n🔥 Server has been completely wizzed!"

        if ctx.guild.icon:
            container.add_item(
                discord.ui.Section(
                    discord.ui.TextDisplay(success_msg),
                    accessory=discord.ui.Thumbnail(ctx.guild.icon.url)
                )
            )
        else:
            container.add_item(discord.ui.TextDisplay(success_msg))

        container.add_item(discord.ui.Separator())

        footer_info = f"⏰ **Completed:** <t:{int(time.time())}:R>\n\n*Note: This is a simulation command for entertainment purposes.*"
        container.add_item(discord.ui.TextDisplay(footer_info))

        view.add_item(container)
        await processing_msg.edit(view=view)


    @commands .command (name ="rickroll",
    help ="Detects if provided url is a rick-roll",
    usage ="Rickroll <url>")
    @blacklist_check ()
    @ignore_check ()
    @commands .cooldown (1 ,3 ,commands .BucketType .user )
    async def rickroll (self ,ctx : commands .Context ,*,url :str ):
        if not re .match (self ._URL_REGEX ,url ):
            error_view = discord.ui.LayoutView()
            error_container = discord.ui.Container(
                discord.ui.TextDisplay("🚫 **Invalid URL**\n\nPlease provide a valid URL to check for rickrolls.\n\nExample: `rickroll https://example.com`"),
                accent_color=None
            )
            error_view.add_item(error_container)
            await ctx.reply(view=error_view, mention_author=True)
            return

        loading_view = discord.ui.LayoutView()
        loading_container = discord.ui.Container(
            discord.ui.TextDisplay(f"🔍 **Rickroll Detection**\n\nAnalyzing URL...\n\n<a:Yuna_loading:1373173756113195081> Checking for rickroll patterns..."),
            accent_color=None
        )
        loading_view.add_item(loading_container)

        processing_msg = await ctx.send(view=loading_view)

        phrases =[
        "rickroll","rick roll","rick astley","never gonna give you up"
        ]

        try:
            source =str (await (await self .aiohttp .get (
            url ,allow_redirects =True )).content .read ()).lower ()
            rickRoll =bool ((re .findall ('|'.join (phrases ),source ,
            re .MULTILINE |re .IGNORECASE )))

            view = discord.ui.LayoutView()
            container = discord.ui.Container(accent_color=None)

            status_emoji = "🚨" if rickRoll else "✅"
            status_text = "RICKROLL DETECTED!" if rickRoll else "No Rickroll Found"
            container.add_item(discord.ui.TextDisplay(f"# {status_emoji} {status_text}"))
            container.add_item(discord.ui.Separator())

            result_text = f"**URL:** {url}\n**Status:** {'⚠️ **RICKROLL DETECTED**' if rickRoll else '✅ **Safe to click**'}\n**Confidence:** {'High' if rickRoll else 'N/A'}"

            if rickRoll:
                result_text += "\n\n🎵 **Detection Keywords:**\n• Rick Astley references found\n• Never gonna give you up detected\n• Classic rickroll patterns identified"
            else:
                result_text += "\n\n🔍 **Analysis:**\n• No rickroll patterns found\n• URL appears safe\n• No Rick Astley references detected"

            container.add_item(discord.ui.TextDisplay(result_text))
            container.add_item(discord.ui.Separator())

            footer_text = f"🕵️ **Checked by:** {ctx.author.mention}\n\n*Note: This detection is based on content analysis and may not be 100% accurate.*"
            container.add_item(discord.ui.TextDisplay(footer_text))

            view.add_item(container)
            await processing_msg.edit(view=view)

        except Exception as e:
            error_view = discord.ui.LayoutView()
            error_container = discord.ui.Container(
                discord.ui.TextDisplay(f"❌ **Analysis Failed**\n\nCould not analyze the provided URL.\n\n**Error:** Failed to fetch webpage content\n**URL:** {url}"),
                accent_color=None
            )
            error_view.add_item(error_container)
            await processing_msg.edit(view=error_view)

    @commands .command (name ="hash",
    help ="Hashes provided text with provided algorithm")
    @blacklist_check ()
    @ignore_check ()
    @commands .cooldown (1 ,3 ,commands .BucketType .user )
    async def hash (self ,ctx : commands .Context ,algorithm :str ,*,message ):
        algos :dict [str ,str ]={
        "md5":hashlib .md5 (bytes (message .encode ("utf-8"))).hexdigest (),
        "sha1":hashlib .sha1 (bytes (message .encode ("utf-8"))).hexdigest (),
        "sha224":hashlib .sha224 (bytes (message .encode ("utf-8"))).hexdigest (),
        "sha3_224":hashlib .sha3_224 (bytes (message .encode ("utf-8"))).hexdigest (),
        "sha256":hashlib .sha256 (bytes (message .encode ("utf-8"))).hexdigest (),
        "sha3_256":hashlib .sha3_256 (bytes (message .encode ("utf-8"))).hexdigest (),
        "sha384":hashlib .sha384 (bytes (message .encode ("utf-8"))).hexdigest (),
        "sha3_384":hashlib .sha3_384 (bytes (message .encode ("utf-8"))).hexdigest (),
        "sha512":hashlib .sha512 (bytes (message .encode ("utf-8"))).hexdigest (),
        "sha3_512":hashlib .sha3_512 (bytes (message .encode ("utf-8"))).hexdigest (),
        "blake2b":hashlib .blake2b (bytes (message .encode ("utf-8"))).hexdigest (),
        "blake2s":hashlib .blake2s (bytes (message .encode ("utf-8"))).hexdigest ()
        }

        view = discord.ui.LayoutView()
        container = discord.ui.Container(accent_color=None)

        container.add_item(discord.ui.TextDisplay(f"# 🔐 Hash Generator"))
        container.add_item(discord.ui.Separator())

        input_preview = message[:50] + "..." if len(message) > 50 else message
        container.add_item(discord.ui.TextDisplay(f"**Input Text:** {input_preview}\n**Length:** {len(message)} characters"))
        container.add_item(discord.ui.Separator())

        if algorithm .lower () not in list (algos .keys ()):
            container.add_item(discord.ui.TextDisplay(f"**🔍 All Available Hash Algorithms:**"))
            container.add_item(discord.ui.Separator())

            md_hashes = ""
            sha_hashes = ""
            blake_hashes = ""

            for algo, hash_value in algos.items():
                if algo.startswith('md'):
                    md_hashes += f"**{algo.upper()}**\n```{hash_value}```\n"
                elif algo.startswith('sha'):
                    sha_hashes += f"**{algo.upper()}**\n```{hash_value}```\n"
                elif algo.startswith('blake'):
                    blake_hashes += f"**{algo.upper()}**\n```{hash_value}```\n"

            if md_hashes:
                container.add_item(discord.ui.TextDisplay(f"**MD Family:**\n{md_hashes}"))
            if sha_hashes:
                container.add_item(discord.ui.TextDisplay(f"**SHA Family:**\n{sha_hashes}"))
            if blake_hashes:
                container.add_item(discord.ui.TextDisplay(f"**BLAKE Family:**\n{blake_hashes}"))
        else:
            hash_value = algos[algorithm.lower()]
            algorithm_info = f"**Algorithm:** {algorithm.upper()}\n**Hash:**\n```{hash_value}```"
            container.add_item(discord.ui.TextDisplay(algorithm_info))

        container.add_item(discord.ui.Separator())

        footer_text = f"🛡️ **Security Note:** These hashes are for verification and educational purposes\n⏰ **Generated:** <t:{int(time.time())}:R>"
        container.add_item(discord.ui.TextDisplay(footer_text))

        view.add_item(container)
        await ctx .reply (view=view ,mention_author =True )

    

    @commands .command (name ="invite",
    aliases =['invite-bot'],
    description ="Get Support & Bot invite link!")
    @blacklist_check ()
    @ignore_check ()
    @commands .cooldown (1 ,3 ,commands .BucketType .user )
    async def invite (self ,ctx : commands .Context ):
        view = ui.LayoutView()
        container = ui.Container(accent_color=None)

        container.add_item(ui.TextDisplay(f"# ✨ Invite {self.bot.user.name}"))
        container.add_item(ui.Separator())

        main_info = f"**Supercharge your server with elegance!**\n\nModeration • Utility • Fun • Music\n\nJoin thousands of servers already using {self.bot.user.name}"

        if self.bot.user.avatar:
            container.add_item(
                ui.Section(
                    ui.TextDisplay(main_info),
                    accessory=ui.Thumbnail(self.bot.user.avatar.url)
                )
            )
        else:
            container.add_item(ui.TextDisplay(main_info))

        container.add_item(ui.Separator())

        action_row = ui.ActionRow()
        action_row.add_item(ui.Button(
            label="Add to Server",
            style=discord.ButtonStyle.link,
            url="https://discord.com/oauth2/authorize?client_id=1372468860435042344&permissions=8&integration_type=0&scope=bot+applications.commands"
        ))
        action_row.add_item(ui.Button(
            label="Support Server",
            style=discord.ButtonStyle.link,
            url="https://discord.gg/meet"
        ))
        container.add_item(action_row)

        container.add_item(ui.Separator())

        footer_info = f"Developed by **AeroX Development**"
        container.add_item(ui.TextDisplay(footer_info))

        view.add_item(container)
        await ctx .send (view=view)

    @commands.hybrid_command(
        name="tts",
        help="Convert text to speech and send as audio in the channel",
        usage="tts [male/female] <text>"
    )
    @discord.app_commands.describe(
        voice="Choose voice type: male or female (default: male)",
        text="The text you want to convert to speech"
    )
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def tts(self, ctx: commands.Context, voice: Optional[str] = "male", *, text: str):
        if len(text) > 500:
            await ctx.reply("❌ Text is too long. Please keep it under 500 characters.")
            return

        voice_map = {
            "male": "Brian",
            "m": "Brian",
            "female": "Emma",
            "f": "Emma"
        }
        
        selected_voice = voice_map.get(voice.lower(), "Brian")

        try:
            import urllib.parse
            
            encoded_text = urllib.parse.quote(text)
            tts_url = f"https://api.streamelements.com/kappa/v2/speech?voice={selected_voice}&text={encoded_text}"
            
            async with self.aiohttp.get(tts_url) as response:
                if response.status == 200:
                    audio_data = await response.read()
                    
                    audio_file = discord.File(
                        fp=io.BytesIO(audio_data),
                        filename="tts.mp3"
                    )
                    
                    await ctx.send(file=audio_file)
                else:
                    await ctx.reply("❌ Failed to generate speech. Please try again later.")
                    
        except Exception as e:
            await ctx.reply(f"❌ An error occurred: {str(e)}")



async def setup(bot):
    await bot.add_cog(General(bot))