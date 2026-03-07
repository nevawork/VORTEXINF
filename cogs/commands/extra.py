"""
: ! Aegis !
    + Discord: itsfizys
    + Community: https://discord.gg/aerox (AeroX Development )
    + for any queries reach out Community or DM me.
"""
import os
import discord
from discord .ext import commands
import datetime
import sys
from discord .ui import Button ,View
from discord import ui
import psutil
import time
from utils .Tools import*
from discord .ext import commands ,menus
from discord .ext .commands import BucketType ,cooldown
import requests
from typing import *
from utils import*
from utils .config import BotName ,serverLink
from utils import Paginator ,DescriptionEmbedPaginator ,FieldPagePaginator ,TextPaginator
from core import Cog ,Yuna ,Context
from typing import Optional
import aiosqlite
import asyncio
import aiohttp
import base64,sys,os; (lambda c: (print(base64.b64decode(b'ChtbOTFtICDilIzilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilJAbWzBtChtbOTFtICDilIIgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICDilIIbWzBtChtbOTFtICDilIIgICAbWzFtJjIwICBDT1JFIElOVEVHUklUWSBDSEVDSyBGQUlMRUQgICAgICAgICAgICAgICAg4pSCG1swbQobWzkxbSAg4pSCICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAg4pSCG1swbQobWzkxbSAg4pSCICAgG1s5N21Cb3QgY3JlZGl0cyBoYXZlIGJlZW4gdGFtcGVyZWQgd2l0aC4bWzkxbSAgICAgICAgICAgIOKUghtbMG0KG1s5MW0gIOKUgiAgIBtbOTdtUmVzdG9yZSBvcmlnaW5hbCBhdXRob3IgY3JlZGl0cyB0byBzdGFydCB0aGUgYm90LhtbOTFtIOKUghtbMG0KG1s5MW0gIOKUgiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIOKUghtbMG0KG1s5MW0gIOKUlOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUmBtbMG0K').decode()), sys.exit(1)) if not (c.count(base64.b64decode(b'ISBBZWdpcyAh').decode()) >= 2 and c.count(base64.b64decode(b'RGlzY29yZDogaXRzZml6eXM=').decode()) >= 2 and base64.b64decode(b'QWVyb1ggRGV2ZWxvcG1lbnQ=').decode() in c and base64.b64decode(b'aHR0cHM6Ly9kaXNjb3JkLmdnL2Flcm94').decode() in c) else None)(open(__file__, 'r', encoding='utf-8').read()) if os.path.exists(__file__) else None


start_time =time .time ()


def datetime_to_seconds (thing :datetime .datetime ):
  current_time =datetime .datetime .fromtimestamp (time .time ())
  return round (
  round (time .time ())+
  (current_time -thing .replace (tzinfo =None )).total_seconds ())

tick ="<:icon_tick:1372375089668161597>"
cross ="<:icon_cross:1372375094336425986>"






class UserinfoLayout(ui.LayoutView):
    def __init__(self, ctx, member):
        super().__init__()
        self.ctx = ctx
        self.member = member
        self.guild = ctx.guild
        self.bot = ctx.bot

        self.container = ui.Container(accent_color=None)

        self.container.add_item(ui.TextDisplay(f"# General Information"))
        self.container.add_item(ui.Separator())
        self.container.add_item(ui.TextDisplay("Loading user information..."))

        self.add_item(self.container)

    async def _setup_general_page(self):
        """Set up the general user info content"""
        self.container.clear_items()

        self.container.add_item(ui.TextDisplay(f"# General Information"))
        self.container.add_item(ui.Separator())

        banner_user = await self.bot.fetch_user(self.member.id)

        nickk = f"{self.member.nick if self.member.nick else 'None'}" if self.member in self.guild.members else "None"
        joinedat = f"<t:{round(self.member.joined_at.timestamp())}:R>" if self.member in self.guild.members else "None"

        badges = self._get_badges()

        user_info = f"**Name:** {self.member.display_name}\n**ID:** {self.member.id}\n**Nickname:** {nickk}\n**Bot:** {'Yes' if self.member.bot else 'No'}\n**Badges:** {badges}\n**Account Created:** <t:{round(self.member.created_at.timestamp())}:R>\n**Server Joined:** {joinedat}"

        if self.member.avatar:
            self.container.add_item(
                ui.Section(
                    ui.TextDisplay(f"**User Information**\n{user_info}"),
                    accessory=ui.Thumbnail(self.member.avatar.url)
                )
            )
        else:
            self.container.add_item(ui.TextDisplay(f"**User Information**\n{user_info}"))

        if banner_user.banner:
            self.container.add_item(ui.Separator())
            banner_gallery = ui.MediaGallery()
            banner_gallery.add_item(media=banner_user.banner.url)
            self.container.add_item(banner_gallery)

        self.container.add_item(ui.Separator())
        self.container.add_item(self._create_select_menu())

    async def _setup_roles_page(self):
        """Set up the roles and permissions content"""
        self.container.clear_items()

        self.container.add_item(ui.TextDisplay(f"# Roles & Permissions"))
        self.container.add_item(ui.Separator())

        if self.member in self.guild.members:
            roles_list = [role.name for role in self.member.roles[1:][::-1]] if len(self.member.roles) > 1 else []
            roles_display = ", ".join(roles_list[:15]) if roles_list else "None"
            if len(roles_list) > 15:
                roles_display += f"\n...and {len(roles_list) - 15} more roles"

            highest_role = self.member.top_role.name if len(self.member.roles) > 1 else "None"
            role_count = len(self.member.roles) - 1

            role_info = f"**Highest Role:** {highest_role}\n**Roles [{role_count}]:** {roles_display}\n**Color:** {self.member.color if self.member.color else '#99aab5'}"
            self.container.add_item(ui.TextDisplay(f"**Role Information**\n{role_info}"))

            kp = self._get_key_permissions()
            self.container.add_item(ui.TextDisplay(f"**Key Permissions**\n{kp}"))

            acknowledgement = self._get_acknowledgement()
            self.container.add_item(ui.TextDisplay(f"**Server Role**\n{acknowledgement}"))
        else:
            self.container.add_item(ui.TextDisplay(f"**Role Information**\nUser is not in this server."))

        self.container.add_item(ui.Separator())
        self.container.add_item(self._create_select_menu())

    async def _setup_activity_page(self):
        """Set up the activity and status content"""
        self.container.clear_items()

        self.container.add_item(ui.TextDisplay(f"# Activity & Status"))
        self.container.add_item(ui.Separator())

        if self.member in self.guild.members:
            boosting_status = f"<t:{round(self.member.premium_since.timestamp())}:R>" if self.member in self.guild.premium_subscribers else "Not boosting"

            voice_status = self.member.voice.channel.name if self.member.voice else "Not in voice"

            activity_info = f"**Boosting Since:** {boosting_status}\n**Voice Channel:** {voice_status}"
            self.container.add_item(ui.TextDisplay(f"**Activity Status**\n{activity_info}"))

            status_info = f"**Status:** {self.member.status}\n**Mobile:** {'Yes' if self.member.is_on_mobile() else 'No'}"
            self.container.add_item(ui.TextDisplay(f"**Presence**\n{status_info}"))
        else:
            self.container.add_item(ui.TextDisplay(f"**Activity Status**\nUser is not in this server."))

        self.container.add_item(ui.Separator())
        self.container.add_item(self._create_select_menu())

    def _get_badges(self):
        """Get user badges"""
        badges = []
        if self.member.public_flags.hypesquad:
            badges.append("HypeSquad Events")
        if self.member.public_flags.hypesquad_balance:
            badges.append("HypeSquad Balance")
        if self.member.public_flags.hypesquad_bravery:
            badges.append("HypeSquad Bravery")
        if self.member.public_flags.hypesquad_brilliance:
            badges.append("HypeSquad Brilliance")
        if self.member.public_flags.early_supporter:
            badges.append("Early Supporter")
        if self.member.public_flags.active_developer:
            badges.append("Active Developer")
        if self.member.public_flags.verified_bot_developer:
            badges.append("Early Verified Bot Developer")
        if self.member.public_flags.discord_certified_moderator:
            badges.append("Moderators Program Alumni")
        if self.member.public_flags.staff:
            badges.append("Discord Staff")
        if self.member.public_flags.partner:
            badges.append("Partnered Server Owner")

        return ", ".join(badges) if badges else "None"

    def _get_key_permissions(self):
        """Get key permissions for the user"""
        if self.member not in self.guild.members:
            return "None"

        perms = []
        if self.member.guild_permissions.administrator:
            perms.append("Administrator")
        if self.member.guild_permissions.kick_members:
            perms.append("Kick Members")
        if self.member.guild_permissions.ban_members:
            perms.append("Ban Members")
        if self.member.guild_permissions.manage_channels:
            perms.append("Manage Channels")
        if self.member.guild_permissions.manage_guild:
            perms.append("Manage Server")
        if self.member.guild_permissions.manage_messages:
            perms.append("Manage Messages")
        if self.member.guild_permissions.mention_everyone:
            perms.append("Mention Everyone")
        if self.member.guild_permissions.manage_nicknames:
            perms.append("Manage Nicknames")
        if self.member.guild_permissions.manage_roles:
            perms.append("Manage Roles")
        if self.member.guild_permissions.manage_webhooks:
            perms.append("Manage Webhooks")
        if self.member.guild_permissions.manage_emojis:
            perms.append("Manage Emojis")

        return ", ".join(perms) if perms else "None"

    def _get_acknowledgement(self):
        """Get user's server role/acknowledgement"""
        if self.member not in self.guild.members:
            return "Not in server"

        if self.member == self.guild.owner:
            return "Server Owner"
        elif self.member.guild_permissions.administrator:
            return "Server Admin"
        elif self.member.guild_permissions.ban_members or self.member.guild_permissions.kick_members:
            return "Server Moderator"
        else:
            return "Server Member"

    def _create_select_menu(self):
        """Create the select menu for navigation"""
        select = ui.Select(
            placeholder="Choose a page...",
            options=[
                discord.SelectOption(label="General Info", value="general", description="Basic user information"),
                discord.SelectOption(label="Roles & Perms", value="roles", description="Role and permission details"),
                discord.SelectOption(label="Activity", value="activity", description="Activity and presence status")
            ]
        )

        async def select_callback(interaction):
            await interaction.response.defer()

            if interaction.data['values'][0] == "general":
                await self._setup_general_page()
            elif interaction.data['values'][0] == "roles":
                await self._setup_roles_page()
            elif interaction.data['values'][0] == "activity":
                await self._setup_activity_page()

            await interaction.edit_original_response(view=self)

        select.callback = select_callback
        return ui.ActionRow(select)

class ServerinfoLayout(ui.LayoutView):
    def __init__(self, ctx):
        super().__init__(timeout=300.0)
        self.ctx = ctx
        self.guild = ctx.guild
        self.current_page = "general"

        self.container = ui.Container(accent_color=None)

        self.select_menu = ui.ActionRow(
            ui.Select(
                placeholder="Choose section...",
                options=[
                    discord.SelectOption(
                        label="General Information",
                        value="general",
                        description="Basic server info, owner, and description"
                    ),
                    discord.SelectOption(
                        label="Server Statistics",
                        value="statistics",
                        description="Channels, roles, emojis, and features"
                    ),
                    discord.SelectOption(
                        label="Boost & Roles",
                        value="boosts",
                        description="Boost status and server roles"
                    )
                ]
            )
        )
        self.select_menu.children[0].callback = self.select_callback

        self.setup_general_content()

        self.add_item(self.container)

    def setup_general_content(self):
        """Set up the general server info content"""
        self.container.clear_items()

        self.container.add_item(ui.TextDisplay(f"# General Information"))
        self.container.add_item(ui.Separator())

        c_at = self.guild.created_at.strftime("%Y-%m-%d %H:%M:%S")
        owner_display = self.guild.owner.display_name if self.guild.owner else "Unknown"
        owner_link = f"[{owner_display}](https://discord.com/users/{self.guild.owner.id})" if self.guild.owner else "Unknown"

        about_info = f"**Name:** {self.guild.name}\n**ID:** {self.guild.id}\n**Owner:** {owner_link}\n**Created At:** {c_at}\n**Members:** {len(self.guild.members):,}"

        if self.guild.icon:
            self.container.add_item(
                ui.Section(
                    ui.TextDisplay(f"📋 **About Server**\n{about_info}"),
                    accessory=ui.Thumbnail(self.guild.icon.url)
                )
            )
        else:
            self.container.add_item(ui.TextDisplay(f"**About Server**\n{about_info}"))

        if self.guild.description:
            self.container.add_item(ui.TextDisplay(f"**Description**\n{self.guild.description}"))

        basic_stats = f"**Verification Level:** {self.guild.verification_level}\n**Total Channels:** {len(self.guild.channels)}\n**Total Roles:** {len(self.guild.roles)}\n**Total Emojis:** {len(self.guild.emojis)}"
        self.container.add_item(ui.TextDisplay(f"**Quick Stats**\n{basic_stats}"))

        self.container.add_item(ui.Separator())
        self.container.add_item(self.select_menu)

        if self.guild.banner:
            self.container.add_item(ui.Separator())
            banner_gallery = ui.MediaGallery()
            banner_gallery.add_item(media=self.guild.banner.url)
            self.container.add_item(banner_gallery)

    def setup_statistics_content(self):
        """Set up the server statistics content"""
        self.container.clear_items()

        self.container.add_item(ui.TextDisplay(f"# Server Statistics"))
        self.container.add_item(ui.Separator())

        categories = len([c for c in self.guild.channels if isinstance(c, discord.CategoryChannel)])
        channels_info = f"**Total:** {len(self.guild.channels)}\n**Text:** {len(self.guild.text_channels)} | **Voice:** {len(self.guild.voice_channels)} | **Categories:** {categories}"
        self.container.add_item(ui.TextDisplay(f"**Channels**\n{channels_info}"))

        regular_emojis = [emoji for emoji in self.guild.emojis if not emoji.animated]
        animated_emojis = [emoji for emoji in self.guild.emojis if emoji.animated]
        emoji_info = f"**Regular:** {len(regular_emojis)}/100\n**Animated:** {len(animated_emojis)}/100\n**Total:** {len(self.guild.emojis)}/200"
        self.container.add_item(ui.TextDisplay(f"**Emojis**\n{emoji_info}"))

        if self.guild.features:
            features = "\n".join([f"<:icon_tick:1372375089668161597> {feature[:1].upper() + feature[1:].lower().replace('_', ' ')}" for feature in self.guild.features[:10]])
            if len(self.guild.features) > 10:
                features += f"\n...and {len(self.guild.features) - 10} more"
            self.container.add_item(ui.TextDisplay(f"**Server Features**\n{features}"))

        security_info = f"**Verification Level:** {self.guild.verification_level}\n**Content Filter:** {self.guild.explicit_content_filter}\n**MFA Requirement:** {'Yes' if self.guild.mfa_level > 0 else 'No'}"
        self.container.add_item(ui.TextDisplay(f"**Security Settings**\n{security_info}"))

        self.container.add_item(ui.Separator())
        self.container.add_item(self.select_menu)

    def setup_boosts_content(self):
        """Set up the boost and roles content"""
        self.container.clear_items()

        self.container.add_item(ui.TextDisplay(f"# Boost & Roles"))
        self.container.add_item(ui.Separator())

        boost_info = f"**Level:** {self.guild.premium_tier}\n**Boosts:** {self.guild.premium_subscription_count}\n**Boosters:** {len(self.guild.premium_subscribers)}"
        self.container.add_item(ui.TextDisplay(f"**Boost Status**\n{boost_info}"))

        roles = self.guild.roles[1:]  # Skip @everyone
        if roles:
            roles_list = [role.name for role in roles]
            roles_count = len(roles_list)
            roles_display = ", ".join(roles_list[:15])

            if roles_count > 15:
                roles_display += f"\n...and {roles_count - 15} more roles"

            self.container.add_item(ui.TextDisplay(f"**Server Roles [{roles_count}]**\n{roles_display}"))
        else:
            self.container.add_item(ui.TextDisplay(f"**Server Roles [0]**\nNo custom roles found."))

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
        elif choice == "statistics":
            self.setup_statistics_content()
        elif choice == "boosts":
            self.setup_boosts_content()

        await interaction.response.edit_message(view=self)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return interaction.user == self.ctx.author


class Extra (commands .Cog ):

  def __init__ (self ,bot ):
    self .bot =bot
    self .color =0x000000
    self .start_time =datetime .datetime .now ()

  @commands .hybrid_group (name ="banner")
  @blacklist_check ()
  @ignore_check ()
  @commands .cooldown (1 ,3 ,commands .BucketType .user )
  async def banner (self ,ctx ):
    if ctx .invoked_subcommand is None :
      await ctx .send_help (ctx .command )

  @banner .command (name ="server")
  @blacklist_check ()
  @ignore_check ()
  @commands .cooldown (1 ,3 ,commands .BucketType .user )
  @commands .max_concurrency (1 ,per =commands .BucketType .default ,wait =False )
  async def server (self ,ctx ):
    if not ctx .guild .banner :
        error_view = discord.ui.LayoutView()
        error_container = discord.ui.Container(
            discord.ui.TextDisplay("❌ **Server Banner**\n\nThis server does not have a banner set."),
            accent_color=None
        )
        error_view.add_item(error_container)
        await ctx.reply(view=error_view)
        return

    view = discord.ui.LayoutView()
    container = discord.ui.Container(accent_color=None)

    container.add_item(discord.ui.TextDisplay(f"# 🖼️ {ctx.guild.name}'s Banner"))
    container.add_item(discord.ui.Separator())

    banner_info = f"**Server:** {ctx.guild.name}\n**Members:** {ctx.guild.member_count:,}"

    if ctx.guild.icon:
        container.add_item(
            discord.ui.Section(
                discord.ui.TextDisplay(banner_info),
                accessory=discord.ui.Thumbnail(ctx.guild.icon.url)
            )
        )
    else:
        container.add_item(discord.ui.TextDisplay(banner_info))

    container.add_item(discord.ui.Separator())

    banner_gallery = discord.ui.MediaGallery()
    banner_gallery.add_item(media=ctx.guild.banner.url)
    container.add_item(banner_gallery)

    view.add_item(container)
    await ctx.reply(view=view)


  @banner .command (name ="user")
  @blacklist_check ()
  @ignore_check ()
  @commands .cooldown (1 ,3 ,commands .BucketType .user )
  @commands .max_concurrency (1 ,per =commands .BucketType .default ,wait =False )
  @commands .guild_only ()
  async def _user (self ,
  ctx ,
  member :Optional [Union [discord .Member ,
  discord .User ]]=None ):
    if member ==None or member =="":
      member =ctx .author
    bannerUser =await self .bot .fetch_user (member .id )

    if not bannerUser .banner :
        error_view = discord.ui.LayoutView()
        error_container = discord.ui.Container(
            discord.ui.TextDisplay(f"❌ **User Banner**\n\n{member.display_name} doesn't have a banner set."),
            accent_color=None
        )
        error_view.add_item(error_container)
        await ctx.reply(view=error_view)
        return

    view = discord.ui.LayoutView()
    container = discord.ui.Container(accent_color=None)

    container.add_item(discord.ui.TextDisplay(f"# 🎨 {member.display_name}'s Banner"))
    container.add_item(discord.ui.Separator())

    user_info = f"**Username:** {bannerUser.name}\n**Display Name:** {member.display_name if hasattr(member, 'display_name') else bannerUser.display_name}"

    if member.avatar:
        container.add_item(
            discord.ui.Section(
                discord.ui.TextDisplay(user_info),
                accessory=discord.ui.Thumbnail(member.avatar.url)
            )
        )
    else:
        container.add_item(discord.ui.TextDisplay(user_info))

    container.add_item(discord.ui.Separator())

    banner_gallery = discord.ui.MediaGallery()
    banner_gallery.add_item(media=bannerUser.banner.url)
    container.add_item(banner_gallery)

    view.add_item(container)
    await ctx.send(view=view)





  @commands .command (name ="uptime",description ="Shows the Bot's Uptime.")
  @blacklist_check ()
  @ignore_check ()
  @commands .cooldown (1 ,3 ,commands .BucketType .user )
  async def uptime (self ,ctx ):
      uptime_seconds =int (round (time .time ()-start_time ))
      uptime_timedelta =datetime .timedelta (seconds =uptime_seconds )

      uptime_string =f"Up since {datetime.datetime.utcfromtimestamp(start_time).strftime('%Y-%m-%d %H:%M:%S')} UTC"
      uptime_duration_string =f"{uptime_timedelta.days} days, {uptime_timedelta.seconds // 3600} hours, {(uptime_timedelta.seconds // 60) % 60} minutes, {uptime_timedelta.seconds % 60} seconds"

      view = ui.LayoutView()
      container = ui.Container(accent_color=None)

      container.add_item(ui.TextDisplay("# ⏰ Yuna-bot Uptime"))
      container.add_item(ui.Separator())

      uptime_info = f"<:icon_danger:1373170993236803688> **UTC:** {uptime_string}\n\n<:icon_ping:1373948868114513972> **Online Duration:** {uptime_duration_string}"

      if ctx.author.display_avatar:
          container.add_item(
              ui.Section(
                  ui.TextDisplay(uptime_info),
                  accessory=ui.Thumbnail(ctx.author.display_avatar.url)
              )
          )
      else:
          container.add_item(ui.TextDisplay(uptime_info))

      view.add_item(container)
      await ctx.reply(view=view)

  @commands.hybrid_command(name="serverinfo",
  aliases=["sinfo","si"],
  with_app_command=True)
  @blacklist_check()
  @ignore_check()
  @commands.cooldown(1, 3, commands.BucketType.user)
  async def serverinfo(self, ctx):
    view = ServerinfoLayout(ctx)

    await ctx.reply(view=view)






  @commands .hybrid_command (name ="userinfo",
  aliases =["whois","ui"],
  usage ="Userinfo [user]",
  with_app_command =True )
  @blacklist_check ()
  @ignore_check ()
  @commands .cooldown (1 ,3 ,commands .BucketType .user )
  @commands .max_concurrency (1 ,per =commands .BucketType .default ,wait =False )
  @commands .guild_only ()
  async def _userinfo (self ,
  ctx ,
  member :Optional [Union [discord .Member ,
  discord .User ]]=None ):
    if member ==None or member =="":
      member =ctx .author
    elif member not in ctx .guild .members :
      member =await self .bot .fetch_user (member .id )

    view = UserinfoLayout(ctx, member)

    await view._setup_general_page()

    await ctx.reply(view=view)



  @commands .hybrid_command (name ='roleinfo',aliases =["ri"],help ="Displays information about a specified role.")
  @blacklist_check ()
  @ignore_check ()
  @commands .cooldown (1 ,3 ,commands .BucketType .user )
  async def roleinfo (self ,ctx ,role :discord .Role ):
    members =role .members
    created_at =role .created_at .strftime ("%Y-%m-%d %H:%M:%S")

    view = ui.LayoutView()
    container = ui.Container(accent_color=None)

    container.add_item(ui.TextDisplay(f"# 🎭 Role Information - {role.name}"))
    container.add_item(ui.Separator())

    total_roles =len (ctx .guild .roles )-0
    role_position =total_roles -role .position
    general_info = f"**ID:** {role.id}\n**Name:** {role.name}\n**Mention:** <@&{role.id}>\n**Color:** {str(role.color)}\n**Total Members:** {len(role.members)}"
    container.add_item(ui.TextDisplay(f"**General Information**\n{general_info}"))

    properties_info = f"**Position:** {role_position}\n**Mentionable:** {role.mentionable}\n**Hoisted:** {role.hoist}\n**Managed:** {role.managed}\n**Created At:** {created_at}"
    container.add_item(ui.TextDisplay(f"**Properties**\n{properties_info}"))

    container.add_item(ui.Separator())

    perms_row = ui.ActionRow()
    perms_btn = ui.Button(
        label="Show Permissions",
        emoji="<:admin:1373949463814738002>",
        style=discord.ButtonStyle.secondary,
        custom_id="show_perms"
    )

    async def perms_callback(interaction):
        if interaction.user.id != ctx.author.id:
            await interaction.response.send_message("You cannot interact with this button.", ephemeral=True)
            return

        permissions = [perm.replace("_", " ").title() for perm, value in role.permissions if value]
        permission_text = ", ".join(permissions) if permissions else "None"

        perm_view = ui.LayoutView()
        perm_container = ui.Container(
            ui.TextDisplay(f"# Permissions for {role.name}"),
            ui.Separator(),
            ui.TextDisplay(permission_text or "No permissions."),
            accent_color=None
        )
        perm_view.add_item(perm_container)
        await interaction.response.send_message(view=perm_view, ephemeral=True)

    perms_btn.callback = perms_callback
    perms_row.add_item(perms_btn)
    container.add_item(perms_row)

    view.add_item(container)
    await ctx.reply(view=view)





  @commands .command (name ="boostcount",
  help ="Shows boosts count",
  usage ="boosts",
  aliases =["bco"],
  with_app_command =True )
  @blacklist_check ()
  @ignore_check ()
  @commands .cooldown (1 ,3 ,commands .BucketType .user )
  async def boosts (self ,ctx ):
    view = ui.LayoutView()
    container = ui.Container(accent_color=None)

    container.add_item(ui.TextDisplay(f"# <:booste:1373949048758997034> Boosts Count Of {ctx.guild.name}"))
    container.add_item(ui.Separator())
    container.add_item(ui.TextDisplay(f"**Total `{ctx.guild.premium_subscription_count}` boosts**"))

    boost_info = f"**Boost Level:** {ctx.guild.premium_tier}\n**Boosters:** {len(ctx.guild.premium_subscribers)}"
    container.add_item(ui.TextDisplay(boost_info))

    view.add_item(container)
    await ctx.reply(view=view)

  @commands .hybrid_group (name ="list",
  invoke_without_command =True ,
  with_app_command =True )
  @blacklist_check ()
  @ignore_check ()
  @commands .cooldown (1 ,3 ,commands .BucketType .user )
  async def __list_ (self ,ctx :commands .Context ):
    if ctx .subcommand_passed is None :
      await ctx .send_help (ctx .command )
      ctx .command .reset_cooldown (ctx )

  @__list_ .command (name ="boosters",
  aliases =["boost","booster"],
  usage ="List boosters",
  help ="List of boosters in the Guild",
  with_app_command =True )
  @blacklist_check ()
  @ignore_check ()
  @commands .cooldown (1 ,3 ,commands .BucketType .user )
  async def list_boost (self ,ctx ):
    guild =ctx .guild
    boosters = guild.premium_subscribers

    if not boosters:
        empty_container = discord.ui.Container(
            discord.ui.TextDisplay(f"# Boosters in {guild.name}"),
            discord.ui.Separator(),
            discord.ui.TextDisplay("No boosters found in this server."),
            accent_color=None
        )
        empty_view = discord.ui.LayoutView()
        empty_view.add_item(empty_container)
        await ctx.reply(view=empty_view)
        return

    view = discord.ui.LayoutView()
    container = discord.ui.Container(accent_color=None)

    container.add_item(discord.ui.TextDisplay(f"# 💎 Server Boosters [{len(boosters)}]"))
    container.add_item(discord.ui.Separator())

    booster_list = "\n".join([
        f"`#{no}.` [{mem}](https://discord.com/users/{mem.id}) - <t:{round(mem.premium_since.timestamp())}:R>"
        for no, mem in enumerate(boosters[:15], start=1)
    ])

    container.add_item(discord.ui.TextDisplay(booster_list))

    if len(boosters) > 15:
        container.add_item(discord.ui.Separator())
        container.add_item(discord.ui.TextDisplay(f"**And {len(boosters) - 15} more boosters...**"))

    container.add_item(discord.ui.Separator())

    server_info = f"**Server:** {guild.name}\n**Boost Level:** {guild.premium_tier}\n**Total Boosts:** {guild.premium_subscription_count}"
    container.add_item(discord.ui.TextDisplay(server_info))

    view.add_item(container)
    await ctx.reply(view=view)

  @__list_ .command (name ="bans",help ="List of all banned members in Guild",aliases =["ban"],with_app_command =True )
  @blacklist_check ()
  @ignore_check ()
  @commands .cooldown (1 ,3 ,commands .BucketType .user )
  @commands .has_permissions (view_audit_log =True )
  @commands .bot_has_permissions (view_audit_log =True )
  async def list_ban (self ,ctx ):
    bans =[member async for member in ctx .guild .bans ()]
    guild = ctx.guild

    if len(bans) == 0:
        empty_container = discord.ui.Container(
            discord.ui.TextDisplay(f"# Banned Users in {guild.name}"),
            discord.ui.Separator(),
            discord.ui.TextDisplay("No banned users found in this server."),
            accent_color=None
        )
        empty_view = discord.ui.LayoutView()
        empty_view.add_item(empty_container)
        await ctx.reply(view=empty_view)
        return

    view = discord.ui.LayoutView()
    container = discord.ui.Container(accent_color=None)

    container.add_item(discord.ui.TextDisplay(f"# 🔨 Banned Users [{len(bans)}]"))
    container.add_item(discord.ui.Separator())

    ban_list = "\n".join([
        f"`#{no}.` {ban_entry.user}"
        for no, ban_entry in enumerate(bans[:15], start=1)
    ])

    container.add_item(discord.ui.TextDisplay(ban_list))

    if len(bans) > 15:
        container.add_item(discord.ui.Separator())
        container.add_item(discord.ui.TextDisplay(f"**And {len(bans) - 15} more banned users...**"))

    container.add_item(discord.ui.Separator())

    server_info = f"**Server:** {guild.name}\n**Total Bans:** {len(bans)}"
    container.add_item(discord.ui.TextDisplay(server_info))

    view.add_item(container)
    await ctx.reply(view=view)

  @__list_ .command (name ="inrole",
  aliases =["inside-role"],
  help ="List of members that are in the specified role",
  with_app_command =True )
  @blacklist_check ()
  @ignore_check ()
  @commands .cooldown (1 ,3 ,commands .BucketType .user )
  async def list_inrole (self ,ctx ,role :discord .Role ):
    guild = ctx.guild
    members = role.members

    if not members:
        empty_container = discord.ui.Container(
            discord.ui.TextDisplay(f"# Members in {role.name}"),
            discord.ui.Separator(),
            discord.ui.TextDisplay(f"No members found with the {role.mention} role."),
            accent_color=None
        )
        empty_view = discord.ui.LayoutView()
        empty_view.add_item(empty_container)
        await ctx.reply(view=empty_view)
        return

    view = discord.ui.LayoutView()
    container = discord.ui.Container(accent_color=None)

    container.add_item(discord.ui.TextDisplay(f"# 👥 Members in {role.name} [{len(members)}]"))
    container.add_item(discord.ui.Separator())

    role_info = f"**Role:** {role.mention}\n**Color:** {role.color}\n**Members:** {len(members)}"
    container.add_item(discord.ui.TextDisplay(role_info))

    container.add_item(discord.ui.Separator())

    member_list = "\n".join([
        f"`#{no}.` [{mem}](https://discord.com/users/{mem.id}) - <t:{int(mem.created_at.timestamp())}:D>"
        for no, mem in enumerate(members[:15], start=1)
    ])

    container.add_item(discord.ui.TextDisplay(member_list))

    if len(members) > 15:
        container.add_item(discord.ui.Separator())
        container.add_item(discord.ui.TextDisplay(f"**And {len(members) - 15} more members...**"))

    view.add_item(container)
    await ctx.reply(view=view)

  @__list_ .command (name ="emojis",
  aliases =["emoji"],
  help ="List of emojis in the Guild with ids",
  with_app_command =True )
  @blacklist_check ()
  @ignore_check ()
  @commands .cooldown (1 ,3 ,commands .BucketType .user )
  async def list_emojis (self ,ctx ):
    guild =ctx .guild
    emojis = ctx.guild.emojis

    if not emojis:
        empty_container = ui.Container(
            ui.TextDisplay(f"# Emojis in {guild.name}"),
            ui.Separator(),
            ui.TextDisplay("No custom emojis found in this server."),
            accent_color=None
        )
        empty_view = ui.LayoutView()
        empty_view.add_item(empty_container)
        await ctx.reply(view=empty_view)
        return

    view = discord.ui.LayoutView()
    container = discord.ui.Container(accent_color=None)

    container.add_item(discord.ui.TextDisplay(f"# 😄 Emojis in {guild.name} [{len(emojis)}]"))
    container.add_item(discord.ui.Separator())

    emoji_list = "\n".join([
        f"`#{no}.` {e} - `{e}`"
        for no, e in enumerate(emojis[:10], start=1)
    ])

    container.add_item(discord.ui.TextDisplay(emoji_list))

    if len(emojis) > 10:
        container.add_item(discord.ui.Separator())
        container.add_item(discord.ui.TextDisplay(f"**And {len(emojis) - 10} more emojis...**"))

    container.add_item(discord.ui.Separator())

    server_info = f"**Server:** {guild.name}\n**Total Emojis:** {len(emojis)}"
    container.add_item(discord.ui.TextDisplay(server_info))

    if len(emojis) > 10:
        nav_row = ui.ActionRow()
        prev_btn = ui.Button(
            label="Previous",
            style=discord.ButtonStyle.secondary,
            disabled=True,
            custom_id="prev_emojis"
        )
        page_btn = ui.Button(
            label=f"Page 1/{(len(emojis) + 9) // 10}",
            style=discord.ButtonStyle.primary,
            disabled=True,
            custom_id="page_info_emojis"
        )
        next_btn = ui.Button(
            label="Next",
            style=discord.ButtonStyle.secondary,
            disabled=(len(emojis) <= 10),
            custom_id="next_emojis"
        )
        nav_row.add_item(prev_btn)
        nav_row.add_item(page_btn)
        nav_row.add_item(next_btn)

        current_page = 0

        async def nav_callback(interaction: discord.Interaction):
            nonlocal current_page

            if interaction.user != ctx.author:
                return await interaction.response.send_message("You can't use these buttons.", ephemeral=True)

            if interaction.data['custom_id'] == 'next_emojis' and current_page < (len(emojis) + 9) // 10 - 1:
                current_page += 1
            elif interaction.data['custom_id'] == 'prev_emojis' and current_page > 0:
                current_page -= 1

            start_idx = current_page * 10
            end_idx = min(start_idx + 10, len(emojis))
            page_emojis = emojis[start_idx:end_idx]
            new_emoji_list = "\n".join([
                f"`#{start_idx + no + 1}.` {e} - `{e}`"
                for no, e in enumerate(page_emojis)
            ])

            new_container = discord.ui.Container(
                discord.ui.TextDisplay(f"# 😄 Emojis in {guild.name} [{len(emojis)}]"),
                discord.ui.Separator(),
                discord.ui.TextDisplay(new_emoji_list),
                discord.ui.Separator(),
                discord.ui.TextDisplay(server_info),
                accent_color=None
            )

            prev_btn.disabled = (current_page == 0)
            next_btn.disabled = (current_page == (len(emojis) + 9) // 10 - 1)
            page_btn.label = f"Page {current_page + 1}/{ (len(emojis) + 9) // 10}"

            new_container.add_item(nav_row)
            new_view = discord.ui.LayoutView()
            new_view.add_item(new_container)

            await interaction.response.edit_message(view=new_view)

        prev_btn.callback = nav_callback
        next_btn.callback = nav_callback
        container.add_item(nav_row)

    view.add_item(container)
    await ctx.reply(view=view)

  @__list_ .command (name ="roles",
  aliases =["role"],
  help ="List of all roles in the server with ids",
  with_app_command =True )
  @blacklist_check ()
  @ignore_check ()
  @commands .cooldown (1 ,3 ,commands .BucketType .user )
  @commands .has_permissions (manage_roles =True )
  async def list_roles (self ,ctx ):
    guild =ctx .guild
    roles = list(reversed(ctx.guild.roles))  # Show highest roles first

    if not roles:
        empty_container = ui.Container(
            ui.TextDisplay(f"# Roles in {guild.name}"),
            ui.Separator(),
            ui.TextDisplay("No roles found in this server."),
            accent_color=None
        )
        empty_view = ui.LayoutView()
        empty_view.add_item(empty_container)
        await ctx.reply(view=empty_view)
        return

    per_page = 10
    total_pages = (len(roles) + per_page - 1) // per_page
    current_page = 0

    def get_page_content(page):
        start_idx = page * per_page
        end_idx = min(start_idx + per_page, len(roles))
        page_roles = roles[start_idx:end_idx]

        role_list = "\n".join([
            f"`#{start_idx + no + 1}.` {role.mention} - `[{role.id}]`"
            for no, role in enumerate(page_roles)
        ])

        return role_list

    container = ui.Container(
        ui.TextDisplay(f"# Roles in {guild.name} [{len(roles)}]"),
        ui.Separator(),
        ui.TextDisplay(get_page_content(current_page)),
        accent_color=None
    )

    if total_pages > 1:
        nav_row = ui.ActionRow()

        prev_btn = ui.Button(
            label="Previous",
            style=discord.ButtonStyle.secondary,
            disabled=True,
            custom_id="prev_roles"
        )

        page_btn = ui.Button(
            label=f"Page {current_page + 1}/{total_pages}",
            style=discord.ButtonStyle.primary,
            disabled=True,
            custom_id="page_info_roles"
        )

        next_btn = ui.Button(
            label="Next",
            style=discord.ButtonStyle.secondary,
            disabled=(total_pages <= 1),
            custom_id="next_roles"
        )

        nav_row.add_item(prev_btn)
        nav_row.add_item(page_btn)
        nav_row.add_item(next_btn)

        async def nav_callback(interaction: discord.Interaction):
            nonlocal current_page

            if interaction.user != ctx.author:
                return await interaction.response.send_message("You can't use these buttons.", ephemeral=True)

            if interaction.data['custom_id'] == 'next_roles' and current_page < total_pages - 1:
                current_page += 1
            elif interaction.data['custom_id'] == 'prev_roles' and current_page > 0:
                current_page -= 1

            new_container = ui.Container(
                ui.TextDisplay(f"# Roles in {guild.name} [{len(roles)}]"),
                ui.Separator(),
                ui.TextDisplay(get_page_content(current_page)),
                accent_color=None
            )

            prev_btn.disabled = (current_page == 0)
            next_btn.disabled = (current_page == total_pages - 1)
            page_btn.label = f"Page {current_page + 1}/{total_pages}"

            new_container.add_item(nav_row)
            new_view = ui.LayoutView()
            new_view.add_item(new_container)

            await interaction.response.edit_message(view=new_view)

        prev_btn.callback = nav_callback
        next_btn.callback = nav_callback

        container.add_item(nav_row)

    view = ui.LayoutView()
    view.add_item(container)
    await ctx.reply(view=view)

  @__list_ .command (name ="bots",
  aliases =["bot"],
  help ="List of All Bots in a server",
  with_app_command =True )
  @blacklist_check ()
  @ignore_check ()
  @commands .cooldown (1 ,3 ,commands .BucketType .user )
  async def list_bots (self ,ctx ):
    guild =ctx .guild
    people =filter (lambda member :member .bot ,ctx .guild .members )
    bots =sorted (people ,key =lambda member :member .joined_at )

    if not bots:
        empty_container = ui.Container(
            ui.TextDisplay(f"# Bots in {guild.name}"),
            ui.Separator(),
            ui.TextDisplay("No bots found in this server."),
            accent_color=None
        )
        empty_view = ui.LayoutView()
        empty_view.add_item(empty_container)
        await ctx.reply(view=empty_view)
        return

    per_page = 10
    total_pages = (len(bots) + per_page - 1) // per_page
    current_page = 0

    def get_page_content(page):
        start_idx = page * per_page
        end_idx = min(start_idx + per_page, len(bots))
        page_bots = bots[start_idx:end_idx]

        bot_list = "\n".join([
            f"`#{start_idx + no + 1}.` [{bot}](https://discord.com/users/{bot.id}) [{bot.mention}]"
            for no, bot in enumerate(page_bots)
        ])

        return bot_list

    container = ui.Container(
        ui.TextDisplay(f"# Bots in {guild.name} [{len(bots)}]"),
        ui.Separator(),
        ui.TextDisplay(get_page_content(current_page)),
        accent_color=None
    )

    if total_pages > 1:
        nav_row = ui.ActionRow()

        prev_btn = ui.Button(
            label="Previous",
            style=discord.ButtonStyle.secondary,
            disabled=True,
            custom_id="prev_bots"
        )

        page_btn = ui.Button(
            label=f"Page {current_page + 1}/{total_pages}",
            style=discord.ButtonStyle.primary,
            disabled=True,
            custom_id="page_info_bots"
        )

        next_btn = ui.Button(
            label="Next",
            style=discord.ButtonStyle.secondary,
            disabled=(total_pages <= 1),
            custom_id="next_bots"
        )

        nav_row.add_item(prev_btn)
        nav_row.add_item(page_btn)
        nav_row.add_item(next_btn)

        async def nav_callback(interaction: discord.Interaction):
            nonlocal current_page

            if interaction.user != ctx.author:
                return await interaction.response.send_message("You can't use these buttons.", ephemeral=True)

            if interaction.data['custom_id'] == 'next_bots' and current_page < total_pages - 1:
                current_page += 1
            elif interaction.data['custom_id'] == 'prev_bots' and current_page > 0:
                current_page -= 1

            new_container = ui.Container(
                ui.TextDisplay(f"# Bots in {guild.name} [{len(bots)}]"),
                ui.Separator(),
                ui.TextDisplay(get_page_content(current_page)),
                accent_color=None
            )

            prev_btn.disabled = (current_page == 0)
            next_btn.disabled = (current_page == total_pages - 1)
            page_btn.label = f"Page {current_page + 1}/{total_pages}"

            new_container.add_item(nav_row)
            new_view = ui.LayoutView()
            new_view.add_item(new_container)

            await interaction.response.edit_message(view=new_view)

        prev_btn.callback = nav_callback
        next_btn.callback = nav_callback

        container.add_item(nav_row)

    view = ui.LayoutView()
    view.add_item(container)
    await ctx.reply(view=view)

  @__list_ .command (name ="admins",
  aliases =["admin"],
  help ="List of all Admins of the Guild",
  with_app_command =True )
  @blacklist_check ()
  @ignore_check ()
  @commands .cooldown (1 ,3 ,commands .BucketType .user )
  async def list_admin (self ,ctx ):
    mems =([
    mem for mem in ctx .guild .members
    if mem .guild_permissions .administrator
    ])
    admins =sorted (mems ,key =lambda mem :not mem .bot )
    guild =ctx .guild

    if not admins:
        empty_container = ui.Container(
            ui.TextDisplay(f"# Admins in {guild.name}"),
            ui.Separator(),
            ui.TextDisplay("No administrators found in this server."),
            accent_color=None
        )
        empty_view = ui.LayoutView()
        empty_view.add_item(empty_container)
        await ctx.reply(view=empty_view)
        return

    per_page = 10
    total_pages = (len(admins) + per_page - 1) // per_page
    current_page = 0

    def get_page_content(page):
        start_idx = page * per_page
        end_idx = min(start_idx + per_page, len(admins))
        page_admins = admins[start_idx:end_idx]

        admin_list = "\n".join([
            f"`#{start_idx + no + 1}.` [{admin}](https://discord.com/users/{admin.id}) [{admin.mention}] - <t:{int(admin.created_at.timestamp())}:D>"
            for no, admin in enumerate(page_admins)
        ])

        return admin_list

    container = ui.Container(
        ui.TextDisplay(f"# Admins in {guild.name} [{len(admins)}]"),
        ui.Separator(),
        ui.TextDisplay(get_page_content(current_page)),
        accent_color=None
    )

    if total_pages > 1:
        nav_row = ui.ActionRow()

        prev_btn = ui.Button(
            label="Previous",
            style=discord.ButtonStyle.secondary,
            disabled=True,
            custom_id="prev_admins"
        )

        page_btn = ui.Button(
            label=f"Page {current_page + 1}/{total_pages}",
            style=discord.ButtonStyle.primary,
            disabled=True,
            custom_id="page_info_admins"
        )

        next_btn = ui.Button(
            label="Next",
            style=discord.ButtonStyle.secondary,
            disabled=(total_pages <= 1),
            custom_id="next_admins"
        )

        nav_row.add_item(prev_btn)
        nav_row.add_item(page_btn)
        nav_row.add_item(next_btn)

        async def nav_callback(interaction: discord.Interaction):
            nonlocal current_page

            if interaction.user != ctx.author:
                return await interaction.response.send_message("You can't use these buttons.", ephemeral=True)

            if interaction.data['custom_id'] == 'next_admins' and current_page < total_pages - 1:
                current_page += 1
            elif interaction.data['custom_id'] == 'prev_admins' and current_page > 0:
                current_page -= 1

            new_container = ui.Container(
                ui.TextDisplay(f"# Admins in {guild.name} [{len(admins)}]"),
                ui.Separator(),
                ui.TextDisplay(get_page_content(current_page)),
                accent_color=None
            )

            prev_btn.disabled = (current_page == 0)
            next_btn.disabled = (current_page == total_pages - 1)
            page_btn.label = f"Page {current_page + 1}/{total_pages}"

            new_container.add_item(nav_row)
            new_view = ui.LayoutView()
            new_view.add_item(new_container)

            await interaction.response.edit_message(view=new_view)

        prev_btn.callback = nav_callback
        next_btn.callback = nav_callback

        container.add_item(nav_row)

    view = ui.LayoutView()
    view.add_item(container)
    await ctx.reply(view=view)

  @__list_ .command (name ="invoice",help ="List of all users in a voice channel",aliases =["invc"],with_app_command =True )
  @blacklist_check ()
  @ignore_check ()
  @commands .cooldown (1 ,3 ,commands .BucketType .user )
  async def listusers (self ,ctx ):
    if not ctx .author .voice :
        error_container = ui.Container(
            ui.TextDisplay("# Voice Channel Users"),
            ui.Separator(),
            ui.TextDisplay("You are not connected to a voice channel."),
            accent_color=None
        )
        error_view = ui.LayoutView()
        error_view.add_item(error_container)
        return await ctx.reply(view=error_view)

    members =ctx .author .voice .channel .members
    channel_name = ctx.author.voice.channel.name

    if not members:
        empty_container = ui.Container(
            ui.TextDisplay(f"# Voice List of {channel_name}"),
            ui.Separator(),
            ui.TextDisplay("No members found in this voice channel."),
            accent_color=None
        )
        empty_view = ui.LayoutView()
        empty_view.add_item(empty_container)
        await ctx.reply(view=empty_view)
        return

    per_page = 10
    total_pages = (len(members) + per_page - 1) // per_page
    current_page = 0

    def get_page_content(page):
        start_idx = page * per_page
        end_idx = min(start_idx + per_page, len(members))
        page_members = members[start_idx:end_idx]

        member_list = "\n".join([
            f"`[{start_idx + no + 1}]` | {member} [{member.mention}]"
            for no, member in enumerate(page_members)
        ])

        return member_list

    container = ui.Container(
        ui.TextDisplay(f"# Voice List of {channel_name} [{len(members)}]"),
        ui.Separator(),
        ui.TextDisplay(get_page_content(current_page)),
        accent_color=None
    )

    if total_pages > 1:
        nav_row = ui.ActionRow()

        prev_btn = ui.Button(
            label="Previous",
            style=discord.ButtonStyle.secondary,
            disabled=True,
            custom_id="prev_voice_users"
        )

        page_btn = ui.Button(
            label=f"Page {current_page + 1}/{total_pages}",
            style=discord.ButtonStyle.primary,
            disabled=True,
            custom_id="page_info_voice_users"
        )

        next_btn = ui.Button(
            label="Next",
            style=discord.ButtonStyle.secondary,
            disabled=(total_pages <= 1),
            custom_id="next_voice_users"
        )

        nav_row.add_item(prev_btn)
        nav_row.add_item(page_btn)
        nav_row.add_item(next_btn)

        async def nav_callback(interaction: discord.Interaction):
            nonlocal current_page

            if interaction.user != ctx.author:
                return await interaction.response.send_message("You can't use these buttons.", ephemeral=True)

            if interaction.data['custom_id'] == 'next_voice_users' and current_page < total_pages - 1:
                current_page += 1
            elif interaction.data['custom_id'] == 'prev_voice_users' and current_page > 0:
                current_page -= 1

            new_container = ui.Container(
                ui.TextDisplay(f"# Voice List of {channel_name} [{len(members)}]"),
                ui.Separator(),
                ui.TextDisplay(get_page_content(current_page)),
                accent_color=None
            )

            prev_btn.disabled = (current_page == 0)
            next_btn.disabled = (current_page == total_pages - 1)
            page_btn.label = f"Page {current_page + 1}/{total_pages}"

            new_container.add_item(nav_row)
            new_view = ui.LayoutView()
            new_view.add_item(new_container)

            await interaction.response.edit_message(view=new_view)

        prev_btn.callback = nav_callback
        next_btn.callback = nav_callback

        container.add_item(nav_row)

    view = ui.LayoutView()
    view.add_item(container)
    await ctx.reply(view=view)

  @__list_ .command (name ="moderators",help ="List of All Admins of a server",aliases =["mods"],with_app_command =True )
  @blacklist_check ()
  @ignore_check ()
  @commands .cooldown (1 ,3 ,commands .BucketType .user )
  async def list_mod (self ,ctx ):
    guild = ctx.guild
    moderators = [
        mem for mem in guild.members
        if mem.guild_permissions.ban_members
        or mem.guild_permissions.kick_members
    ]
    moderators = sorted(moderators, key=lambda mem: mem.joined_at)

    if not moderators:
        empty_container = discord.ui.Container(
            discord.ui.TextDisplay(f"# Moderators in {guild.name}"),
            discord.ui.Separator(),
            discord.ui.TextDisplay("No moderators found in this server."),
            accent_color=None
        )
        empty_view = discord.ui.LayoutView()
        empty_view.add_item(empty_container)
        await ctx.reply(view=empty_view)
        return

    view = discord.ui.LayoutView()
    container = discord.ui.Container(accent_color=None)

    container.add_item(discord.ui.TextDisplay(f"# ⚔️ Moderators [{len(moderators)}]"))
    container.add_item(discord.ui.Separator())

    mod_list = "\n".join([
        f"`#{no}.` [{mem}](https://discord.com/users/{mem.id}) - <t:{int(mem.created_at.timestamp())}:D>"
        for no, mem in enumerate(moderators[:15], start=1)
    ])

    container.add_item(discord.ui.TextDisplay(mod_list))

    if len(moderators) > 15:
        container.add_item(discord.ui.Separator())
        container.add_item(discord.ui.TextDisplay(f"**And {len(moderators) - 15} more moderators...**"))

    container.add_item(discord.ui.Separator())

    server_info = f"**Server:** {guild.name}\n**Total Moderators:** {len(moderators)}"
    container.add_item(discord.ui.TextDisplay(server_info))

    view.add_item(container)
    await ctx.reply(view=view)

  @__list_ .command (name ="early",aliases =["sup"],help ="List of members that have Early Supporter badge.",with_app_command =True )
  @blacklist_check ()
  @ignore_check ()
  @commands .cooldown (1 ,3 ,commands .BucketType .user )
  async def list_early (self ,ctx ):
    guild = ctx.guild
    early_supporters = [
        memb for memb in guild.members
        if memb.public_flags.early_supporter
    ]
    early_supporters = sorted(early_supporters, key=lambda memb: memb.created_at)

    if not early_supporters:
        empty_container = discord.ui.Container(
            discord.ui.TextDisplay(f"# Early Supporters in {guild.name}"),
            discord.ui.Separator(),
            discord.ui.TextDisplay("No early supporters found in this server."),
            accent_color=None
        )
        empty_view = discord.ui.LayoutView()
        empty_view.add_item(empty_container)
        await ctx.reply(view=empty_view)
        return

    view = discord.ui.LayoutView()
    container = discord.ui.Container(accent_color=None)

    container.add_item(discord.ui.TextDisplay(f"# 🌟 Early Supporters [{len(early_supporters)}]"))
    container.add_item(discord.ui.Separator())

    supporter_list = "\n".join([
        f"`#{no}.` [{mem}](https://discord.com/users/{mem.id}) - <t:{int(mem.created_at.timestamp())}:D>"
        for no, mem in enumerate(early_supporters[:15], start=1)
    ])

    container.add_item(discord.ui.TextDisplay(supporter_list))

    if len(early_supporters) > 15:
        container.add_item(discord.ui.Separator())
        container.add_item(discord.ui.TextDisplay(f"**And {len(early_supporters) - 15} more early supporters...**"))

    container.add_item(discord.ui.Separator())

    server_info = f"**Server:** {guild.name}\n**Early Supporters:** {len(early_supporters)}"
    container.add_item(discord.ui.TextDisplay(server_info))

    view.add_item(container)
    await ctx.reply(view=view)

  @__list_ .command (name ="activedeveloper",help ="List of members that have Active Developer badge.",
  aliases =["activedev"],
  with_app_command =True )
  @blacklist_check ()
  @ignore_check ()
  @commands .cooldown (1 ,3 ,commands .BucketType .user )
  async def list_activedeveloper (self ,ctx ):
    guild = ctx.guild
    active_developers = [
        memb for memb in guild.members
        if memb.public_flags.active_developer
    ]
    active_developers = sorted(active_developers, key=lambda memb: memb.created_at)

    if not active_developers:
        empty_container = discord.ui.Container(
            discord.ui.TextDisplay(f"# Active Developers in {guild.name}"),
            discord.ui.Separator(),
            discord.ui.TextDisplay("No active developers found in this server."),
            accent_color=None
        )
        empty_view = discord.ui.LayoutView()
        empty_view.add_item(empty_container)
        await ctx.reply(view=empty_view)
        return

    view = discord.ui.LayoutView()
    container = discord.ui.Container(accent_color=None)

    container.add_item(discord.ui.TextDisplay(f"# 🛠️ Active Developers [{len(active_developers)}]"))
    container.add_item(discord.ui.Separator())

    dev_list = "\n".join([
        f"`#{no}.` [{mem}](https://discord.com/users/{mem.id}) - <t:{int(mem.created_at.timestamp())}:D>"
        for no, mem in enumerate(active_developers[:15], start=1)
    ])

    container.add_item(discord.ui.TextDisplay(dev_list))

    if len(active_developers) > 15:
        container.add_item(discord.ui.Separator())
        container.add_item(discord.ui.TextDisplay(f"**And {len(active_developers) - 15} more active developers...**"))

    container.add_item(discord.ui.Separator())

    server_info = f"**Server:** {guild.name}\n**Active Developers:** {len(active_developers)}"
    container.add_item(discord.ui.TextDisplay(server_info))

    view.add_item(container)
    await ctx.reply(view=view)

  @__list_ .command (name ="createdat",help ="List of Account Creation Date of all Users",with_app_command =True )
  @blacklist_check ()
  @ignore_check ()
  @commands .cooldown (1 ,3 ,commands .BucketType .user )
  async def list_cpos (self ,ctx ):
    guild = ctx.guild
    members = sorted(guild.members, key=lambda memb: memb.created_at)

    if not members:
        empty_container = discord.ui.Container(
            discord.ui.TextDisplay(f"# Account Creation Dates in {guild.name}"),
            discord.ui.Separator(),
            discord.ui.TextDisplay("No members found in this server."),
            accent_color=None
        )
        empty_view = discord.ui.LayoutView()
        empty_view.add_item(empty_container)
        await ctx.reply(view=empty_view)
        return

    view = discord.ui.LayoutView()
    container = discord.ui.Container(accent_color=None)

    container.add_item(discord.ui.TextDisplay(f"# 📅 Account Creation Dates [{len(members)}]"))
    container.add_item(discord.ui.Separator())

    member_list = "\n".join([
        f"`[{no}]` | [{mem}](https://discord.com/users/{mem.id}) - <t:{int(mem.created_at.timestamp())}:D>"
        for no, mem in enumerate(members[:15], start=1)
    ])

    container.add_item(discord.ui.TextDisplay(member_list))

    if len(members) > 15:
        container.add_item(discord.ui.Separator())
        container.add_item(discord.ui.TextDisplay(f"**And {len(members) - 15} more members...**"))

    container.add_item(discord.ui.Separator())

    server_info = f"**Server:** {guild.name}\n**Total Members:** {len(members)}\n**Sorted by:** Account Creation Date"
    container.add_item(discord.ui.TextDisplay(server_info))

    view.add_item(container)
    await ctx.reply(view=view)

  @__list_ .command (name ="joinedat",help ="List of Guild Joined date of all Users",with_app_command =True )
  @blacklist_check ()
  @ignore_check ()
  @commands .cooldown (1 ,3 ,commands .BucketType .user )
  async def list_joinpos (self ,ctx ):
    guild = ctx.guild
    members = sorted(guild.members, key=lambda memb: memb.joined_at)

    if not members:
        empty_container = discord.ui.Container(
            discord.ui.TextDisplay(f"# Join Positions in {guild.name}"),
            discord.ui.Separator(),
            discord.ui.TextDisplay("No members found in this server."),
            accent_color=None
        )
        empty_view = discord.ui.LayoutView()
        empty_view.add_item(empty_container)
        await ctx.reply(view=empty_view)
        return

    view = discord.ui.LayoutView()
    container = discord.ui.Container(accent_color=None)

    container.add_item(discord.ui.TextDisplay(f"# 📈 Join Positions [{len(members)}]"))
    container.add_item(discord.ui.Separator())

    member_list = "\n".join([
        f"`#{no}.` [{mem}](https://discord.com/users/{mem.id}) - <t:{int(mem.joined_at.timestamp())}:D>"
        for no, mem in enumerate(members[:15], start=1)
    ])

    container.add_item(discord.ui.TextDisplay(member_list))

    if len(members) > 15:
        container.add_item(discord.ui.Separator())
        container.add_item(discord.ui.TextDisplay(f"**And {len(members) - 15} more members...**"))

    container.add_item(discord.ui.Separator())

    server_info = f"**Server:** {guild.name}\n**Total Members:** {len(members)}\n**Sorted by:** Join Date"
    container.add_item(discord.ui.TextDisplay(server_info))

    view.add_item(container)
    await ctx.reply(view=view)




  @commands .command (name ="joined-at",
  help ="Shows when a user joined",
  usage ="joined-at [user]",
  with_app_command =True )
  @blacklist_check ()
  @ignore_check ()
  @commands .cooldown (1 ,3 ,commands .BucketType .user )
  async def joined_at (self ,ctx ):
    joined =ctx .author .joined_at .strftime ("%a, %d %b %Y %I:%M %p")

    view = ui.LayoutView()
    container = ui.Container(accent_color=None)

    container.add_item(ui.TextDisplay("# 📅 Join Date"))
    container.add_item(ui.Separator())

    if ctx.author.avatar:
        container.add_item(
            ui.Section(
                ui.TextDisplay(f"**{ctx.author.display_name}** joined:\n**`{joined}`**"),
                accessory=ui.Thumbnail(ctx.author.avatar.url)
            )
        )
    else:
        container.add_item(ui.TextDisplay(f"**{ctx.author.display_name}** joined:\n**`{joined}`**"))

    view.add_item(container)
    await ctx.reply(view=view)

  @commands .command (name ="github",usage ="github [search]")
  @blacklist_check ()
  @ignore_check ()
  @commands .cooldown (1 ,3 ,commands .BucketType .user )
  async def github (self ,ctx ,*,search_query ):
    try:
      json =requests .get (
      f"https://api.github.com/search/repositories?q={search_query}").json ()

      view = ui.LayoutView()
      container = ui.Container(accent_color=None)

      container.add_item(ui.TextDisplay(f"# 🔍 GitHub Search"))
      container.add_item(ui.Separator())

      if json ["total_count"]==0 :
        container.add_item(ui.TextDisplay(f"❌ **No Results**\n\nNo repositories found for: **{search_query}**"))
      else :
        repo = json['items'][0]

        repo_info = f"**Repository:** {repo.get('name', 'Unknown')}\n**Owner:** {repo.get('owner', {}).get('login', 'Unknown')}\n**Description:** {repo.get('description', 'No description available')[:150]}{'...' if len(repo.get('description', '')) > 150 else ''}"

        avatar_url = repo.get('owner', {}).get('avatar_url')
        if avatar_url:
            try:
                container.add_item(
                    ui.Section(
                        ui.TextDisplay(repo_info),
                        accessory=ui.Thumbnail(avatar_url)
                    )
                )
            except:
                container.add_item(ui.TextDisplay(repo_info))
        else:
            container.add_item(ui.TextDisplay(repo_info))

        container.add_item(ui.Separator())

        stats = f"⭐ **Stars:** {repo.get('stargazers_count', 0):,}\n🍴 **Forks:** {repo.get('forks_count', 0):,}\n📝 **Language:** {repo.get('language', 'Not specified')}\n🕒 **Updated:** <t:{int(datetime.datetime.fromisoformat(repo.get('updated_at', '').replace('Z', '+00:00')).timestamp())}:R>" if repo.get('updated_at') else f"⭐ **Stars:** {repo.get('stargazers_count', 0):,}\n🍴 **Forks:** {repo.get('forks_count', 0):,}\n📝 **Language:** {repo.get('language', 'Not specified')}"
        container.add_item(ui.TextDisplay(stats))

        if repo.get("html_url"):
          container.add_item(ui.Separator())

          action_row = ui.ActionRow()
          action_row.add_item(ui.Button(
            label="View on GitHub",
            style=discord.ButtonStyle.link,
            url=repo['html_url'],
            emoji="🔗"
          ))

          container.add_item(action_row)

      view.add_item(container)
      await ctx.reply(view=view)

    except Exception as e:
      error_view = ui.LayoutView()
      error_container = ui.Container(
          ui.TextDisplay("❌ **GitHub Search Failed**\n\nUnable to search GitHub repositories. Please try again later."),
          accent_color=None
      )
      error_view.add_item(error_container)
      await ctx.reply(view=error_view)

  @commands .hybrid_command (name ="vcinfo",
  description ="View information about a voice channel.",
  help ="View information about a voice channel.",
  usage ="<VoiceChannel>",
  with_app_command =True )
  @blacklist_check ()
  @ignore_check ()
  @commands .cooldown (1 ,3 ,commands .BucketType .user )
  async def vcinfo (self ,ctx ,channel :discord .VoiceChannel =None ):
    if channel is None :
      error_view = ui.LayoutView()
      error_container = ui.Container(
          ui.TextDisplay(f"❌ **Voice Channel Info**\n\nPlease provide a valid voice channel."),
          accent_color=None
      )
      error_view.add_item(error_container)
      await ctx.reply(view=error_view)
      return

    view = ui.LayoutView()
    container = ui.Container(accent_color=None)

    container.add_item(ui.TextDisplay(f"# 🎙️ Voice Channel Info for: {channel.name}"))
    container.add_item(ui.Separator())

    basic_info = f"**ID:** {channel.id}\n**Members:** {len(channel.members)}\n**Bitrate:** {channel.bitrate/1000} kbps\n**Created At:** {channel.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
    container.add_item(ui.TextDisplay(f"**Basic Information**\n{basic_info}"))

    additional_info = f"**Category:** {channel.category.name if channel.category else 'None'}\n**Region:** {channel.rtc_region or 'Auto'}"
    if channel.user_limit:
        additional_info += f"\n**User Limit:** {channel.user_limit}"
    container.add_item(ui.TextDisplay(f"**Additional Details**\n{additional_info}"))

    container.add_item(ui.Separator())

    action_row = ui.ActionRow()
    action_row.add_item(ui.Button(label="Join Channel", style=discord.ButtonStyle.green, url=f"https://discord.com/channels/{ctx.guild.id}/{channel.id}"))
    action_row.add_item(ui.Button(label="Create Invite", style=discord.ButtonStyle.link, url=f"https://discord.com/channels/{ctx.guild.id}/{channel.id}/invite"))
    container.add_item(action_row)

    view.add_item(container)
    await ctx.reply(view=view)


  @commands .hybrid_command (name ="channelinfo",
  aliases =['cinfo','ci'],
  description ='Get information about a channel.',
  help ='Get information about a channel.',
  usage ="<Channel>",
  with_app_command =True )
  @blacklist_check ()
  @ignore_check ()
  @commands .cooldown (1 ,3 ,commands .BucketType .user )
  async def channelinfo (self ,ctx ,channel :discord .TextChannel =None ):
    if channel is None :
      channel =ctx .channel

    view = ui.LayoutView()
    container = ui.Container(accent_color=None)

    container.add_item(ui.TextDisplay(f"# 💬 Channel Info - {channel.name}"))
    container.add_item(ui.Separator())

    basic_info = f"**ID:** {channel.id}\n**Created At:** {channel.created_at.strftime('%Y-%m-%d %H:%M:%S')}\n**Category:** {channel.category.name if channel.category else 'None'}"
    container.add_item(ui.TextDisplay(f"**Basic Information**\n{basic_info}"))

    properties_info = f"**Topic:** {channel.topic if channel.topic else 'None'}\n**Slowmode:** {f'{channel.slowmode_delay} seconds' if channel.slowmode_delay else 'None'}\n**NSFW:** {channel.is_nsfw()}"
    container.add_item(ui.TextDisplay(f"**Properties**\n{properties_info}"))

    container.add_item(ui.Separator())

    action_row = ui.ActionRow()

    overwrites_btn = ui.Button(
        label="Show Overwrites",
        style=discord.ButtonStyle.primary,
        custom_id="show_overwrites"
    )

    async def overwrites_callback(interaction):
        if interaction.user.id != ctx.author.id:
            await interaction.response.send_message("You cannot interact with this button.", ephemeral=True)
            return

        overwrites = []
        for target, perms in channel.overwrites:
            permissions = {
                "View Channel": perms.view_channel,
                "Send Messages": perms.send_messages,
                "Read Message History": perms.read_message_history,
                "Manage Messages": perms.manage_messages,
                "Embed Links": perms.embed_links,
                "Attach Files": perms.attach_files,
                "Manage Channels": perms.manage_channels,
                "Manage Permissions": perms.manage_permissions,
                "Manage Webhooks": perms.manage_webhooks,
                "Create Instant Invite": perms.create_instant_invite,
                "Add Reactions": perms.add_reactions,
                "Mention Everyone": perms.mention_everyone
            }

            overwrites.append(f"**For {target.name}**\n" +
                "\n".join(f"  * **{perm}:** {'<:icon_tick:1372375089668161597>' if value else '<:icon_cross:1372375094336425986>' if value is False else '⛔'}"
                         for perm, value in permissions.items()))

        overwrites_view = ui.LayoutView()
        overwrites_container = ui.Container(
            ui.TextDisplay(f"# Overwrites for {channel.name}"),
            ui.Separator(),
            ui.TextDisplay("\n".join(overwrites) if overwrites else "No overwrites for this channel."),
            ui.Separator(),
            ui.TextDisplay("<:icon_tick:1372375089668161597>= Allowed, <:icon_cross:1372375094336425986> = Denied, ⛔ = None"),
            accent_color=None
        )
        overwrites_view.add_item(overwrites_container)
        await interaction.response.send_message(view=overwrites_view, ephemeral=True)

    overwrites_btn.callback = overwrites_callback
    action_row.add_item(overwrites_btn)
    action_row.add_item(ui.Button(label="Go to Channel", style=discord.ButtonStyle.green, url=f"https://discord.com/channels/{ctx.guild.id}/{channel.id}"))
    container.add_item(action_row)

    view.add_item(container)
    await ctx.reply(view=view)


  @commands .command (name ="ping",aliases =['latency'],
  help ="Checks the bot latency.",
  with_app_command =True )
  @ignore_check ()
  @blacklist_check ()
  @commands .cooldown (1 ,2 ,commands .BucketType .user )
  async def ping (self ,ctx ):
    start_time = time.perf_counter()

    websocket_ping = round(self.bot.latency * 1000, 2)
    message_latency = 0  # Will be updated after sending
    total_response = websocket_ping  # Will be updated after sending


    view = discord.ui.LayoutView()

    ping_container = discord.ui.Container(
        discord.ui.TextDisplay("**Pong!**"),
        discord.ui.Separator(),
        accent_color=None
    )

    if self.bot.user.avatar:
        ping_container.add_item(
            discord.ui.Section(
                discord.ui.TextDisplay(f"**Latency Information:**\n<:dot:1479361908766281812>  **WebSocket Ping:** {websocket_ping}ms\n<:dot:1479361908766281812>  **Message Latency:** {message_latency}ms\n<:dot:1479361908766281812>  **Total Response:** {total_response}ms"),
                accessory=discord.ui.Thumbnail(self.bot.user.avatar.url)
            )
        )
    else:
        ping_container.add_item(
            discord.ui.TextDisplay(f"**Latency Information:**\n<:dot:1479361908766281812>  **WebSocket Ping:** {websocket_ping}ms\n<:dot:1479361908766281812>  **Message Latency:** {message_latency}ms\n<:dot:1479361908766281812>  **Total Response:** {total_response}ms")
        )

    view.add_item(ping_container)

    await ctx.send(view=view)
    end_time = time.perf_counter()
    message_latency = round((end_time - start_time) * 1000, 2)
    total_response = round(websocket_ping + message_latency, 2)

    updated_view = discord.ui.LayoutView()
    updated_ping_container = discord.ui.Container(
        discord.ui.TextDisplay("**Pong!**"),
        discord.ui.Separator(),
        accent_color=None
    )

    if self.bot.user.avatar:
        updated_ping_container.add_item(
            discord.ui.Section(
                discord.ui.TextDisplay(f"**Latency Information:**\n<:dot:1479361908766281812>  **WebSocket Ping:** {websocket_ping}ms\n<:dot:1479361908766281812>  **Message Latency:** {message_latency}ms\n<:dot:1479361908766281812>  **Total Response:** {total_response}ms"),
                accessory=discord.ui.Thumbnail(self.bot.user.avatar.url)
            )
        )
    else:
        updated_ping_container.add_item(
            discord.ui.TextDisplay(f"**Latency Information:**\n<:dot:1479361908766281812>  **WebSocket Ping:** {websocket_ping}ms\n<:dot:1479361908766281812>  **Message Latency:** {message_latency}ms\n<:dot:1479361908766281812>  **Total Response:** {total_response}ms")
        )

    updated_view.add_item(updated_ping_container)

    async for message in ctx.history(limit=1):
        if message.author == ctx.bot.user:
            await message.edit(view=updated_view)
            break




  @commands .command (name ="permissions",aliases =["perms"],
  help ="Check and list the key permissions of a specific user",
  usage ="perms <user>",
  with_app_command =True )
  @blacklist_check ()
  @ignore_check ()
  @commands .cooldown (1 ,3 ,commands .BucketType .user )
  async def keyperms (self ,ctx ,member :discord .Member ):
    key_permissions =[]

    if member .guild_permissions .create_instant_invite :
      key_permissions .append ("Create Instant Invite")
    if member .guild_permissions .kick_members :
      key_permissions .append ("Kick Members")
    if member .guild_permissions .ban_members :
      key_permissions .append ("Ban Members")
    if member .guild_permissions .administrator :
      key_permissions .append ("Administrator")
    if member .guild_permissions .manage_channels :
      key_permissions .append ("Manage Channels")
    if member .guild_permissions .manage_messages :
      key_permissions .append ("Manage Messages")
    if member .guild_permissions .mention_everyone :
      key_permissions .append ("Mention Everyone")
    if member .guild_permissions .manage_nicknames :
      key_permissions .append ("Manage Nicknames")
    if member .guild_permissions .manage_roles :
      key_permissions .append ("Manage Roles")
    if member .guild_permissions .manage_webhooks :
      key_permissions .append ("Manage Webhooks")
    if member .guild_permissions .manage_emojis :
      key_permissions .append ("Manage Emojis")
    if member .guild_permissions .manage_guild :
      key_permissions .append ("Manage Server")
    if member .guild_permissions .manage_permissions :
      key_permissions .append ("Manage Permissions")
    if member .guild_permissions .manage_threads :
      key_permissions .append ("Manage Threads")
    if member .guild_permissions .moderate_members :
      key_permissions .append ("Moderate Members")
    if member .guild_permissions .move_members :
      key_permissions .append ("Move Members")
    if member .guild_permissions .mute_members :
      key_permissions .append ("Mute Members (VC)")
    if member .guild_permissions .deafen_members :
      key_permissions .append ("Deafen Members")
    if member .guild_permissions .priority_speaker :
      key_permissions .append ("Priority Speaker")
    if member .guild_permissions .stream :
      key_permissions .append ("Stream")

    permissions_list =", ".join (key_permissions )if key_permissions else "None"

    view = ui.LayoutView()
    container = ui.Container(accent_color=None)

    container.add_item(ui.TextDisplay(f"# 🔑 Key Permissions of {member}"))
    container.add_item(ui.Separator())

    if member.avatar:
        container.add_item(
            ui.Section(
                ui.TextDisplay(f"**Key Permissions:**\n{permissions_list}"),
                accessory=ui.Thumbnail(member.avatar.url)
            )
        )
    else:
        container.add_item(ui.TextDisplay(f"**Key Permissions:**\n{permissions_list}"))

    view.add_item(container)
    await ctx.reply(view=view)






  @commands .hybrid_command (name ="report",
  aliases =["bug"],
  usage ='Report <bug>',
  description ='Report a bug to the Development team.',
  help ='Report a bug to the Development team.',
  with_app_command =True )
  @blacklist_check ()
  @ignore_check ()
  @commands .cooldown (1 ,30 ,commands .BucketType .channel )
  async def report (self ,ctx ,*,bug ):
    channel =self .bot .get_channel (1377940648493322240 )

    report_view = ui.LayoutView()
    report_container = ui.Container(
        ui.TextDisplay("# Bug Reported"),
        ui.Separator(),
        ui.TextDisplay(f"**Description:** {bug}"),
        ui.TextDisplay(f"**Reported By:** {ctx.author.name}"),
        ui.TextDisplay(f"**Server:** {ctx.guild.name}"),
        ui.TextDisplay(f"**Channel:** {ctx.channel.name}"),
        accent_color=None
    )
    report_view.add_item(report_container)
    await channel .send (view=report_view)

    confirm_view = ui.LayoutView()
    confirm_container = ui.Container(
        ui.TextDisplay("# <:icon_tick:1372375089668161597> Bug Reported"),
        ui.Separator(),
        ui.TextDisplay("Thank you for reporting the bug. We will look into it."),
        accent_color=None
    )
    confirm_view.add_item(confirm_container)
    await ctx .reply (view=confirm_view)


async def setup(bot):
    await bot.add_cog(Extra(bot))

"""
: ! Aegis !
    + Discord: itsfizys
    + Community: https://discord.gg/aerox (AeroX Development )
    + for any queries reach out Community or DM me.
"""
