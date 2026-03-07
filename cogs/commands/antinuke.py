"""
: ! Aegis !
    + Discord: itsfizys
    + Community: https://discord.gg/aerox (AeroX Development )
    + for any queries reach out Community or DM me.
"""
import discord 
from discord .ext import commands 
import aiosqlite 
import asyncio 
from utils .Tools import *
from discord import ui


DEFAULT_LIMITS ={
'ban':3 ,
'kick':3 ,
'channel_create':2 ,
'channel_delete':1 ,
'channel_update':5 ,
'role_create':3 ,
'role_delete':2 ,
'role_update':5 ,
'member_update':5 ,
'guild_update':2 ,
'webhook_create':2 ,
'webhook_delete':2 ,
'webhook_update':3 ,
'integration':2 ,
'prune':1 
}

TIME_WINDOW =60 


class Antinuke (commands .Cog ):
  def __init__ (self ,bot ):
    self .bot =bot 
    self .bot .loop .create_task (self .initialize_db ())

  async def initialize_db (self ):
    self .db =await aiosqlite .connect ('db/anti.db')
    await self .db .execute ('''
        CREATE TABLE IF NOT EXISTS antinuke (
            guild_id INTEGER PRIMARY KEY,
            status BOOLEAN
        )
    ''')
    await self .db .execute ('''
        CREATE TABLE IF NOT EXISTS limit_settings (
            guild_id INTEGER,
            action_type TEXT,
            action_limit INTEGER,
            time_window INTEGER,
            PRIMARY KEY (guild_id, action_type)
        )
    ''')
    await self .db .execute ('''
        CREATE TABLE IF NOT EXISTS extraowners (
            guild_id INTEGER,
            owner_id INTEGER,
            PRIMARY KEY (guild_id, owner_id)
        )
    ''')
    await self .db .execute ('''
        CREATE TABLE IF NOT EXISTS whitelisted_users (
            guild_id INTEGER,
            user_id INTEGER,
            ban BOOLEAN DEFAULT 0,
            kick BOOLEAN DEFAULT 0,
            chdl BOOLEAN DEFAULT 0,
            chcr BOOLEAN DEFAULT 0,
            chup BOOLEAN DEFAULT 0,
            meneve BOOLEAN DEFAULT 0,
            rlcr BOOLEAN DEFAULT 0,
            rldl BOOLEAN DEFAULT 0,
            rlup BOOLEAN DEFAULT 0,
            mngweb BOOLEAN DEFAULT 0,
            prune BOOLEAN DEFAULT 0,
            PRIMARY KEY (guild_id, user_id)
        )
    ''')
    await self .db .commit ()


  async def enable_limit_settings (self ,guild_id ):
    default_limits =DEFAULT_LIMITS 
    for action ,limit in default_limits .items ():
      await self .db .execute ('INSERT OR REPLACE INTO limit_settings (guild_id, action_type, action_limit, time_window) VALUES (?, ?, ?, ?)',(guild_id ,action ,limit ,TIME_WINDOW ))
    await self .db .commit ()

  async def disable_limit_settings (self ,guild_id ):
    await self .db .execute ('DELETE FROM limit_settings WHERE guild_id = ?',(guild_id ,))
    await self .db .commit ()


  @commands .hybrid_command (name ='antinuke',aliases =['antiwizz','anti'],help ="Enables/Disables Anti-Nuke Module in the server")

  @blacklist_check ()
  @ignore_check ()
  @commands .cooldown (1 ,4 ,commands .BucketType .user )
  @commands .max_concurrency (1 ,per =commands .BucketType .default ,wait =False )
  @commands .guild_only ()
  @commands .has_permissions (administrator =True )
  async def antinuke (self ,ctx ,option :str =None ):
    guild_id =ctx .guild .id 
    pre =ctx .prefix 

    async with self .db .execute ('SELECT status FROM antinuke WHERE guild_id = ?',(guild_id ,))as cursor :
      row =await cursor .fetchone ()

    async with self .db .execute (
    "SELECT owner_id FROM extraowners WHERE guild_id = ? AND owner_id = ?",
    (ctx .guild .id ,ctx .author .id )
    )as cursor :
            check =await cursor .fetchone ()

    is_owner =ctx .author .id ==ctx .guild .owner_id 
    if not is_owner and not check :
      # Create Components v2 layout
      view = ui.LayoutView()
      container = ui.Container(accent_color=None)

      # Title
      container.add_item(ui.TextDisplay("# <:icon_cross:1372375094336425986> | Access Denied"))
      container.add_item(ui.Separator())

      # Main info
      container.add_item(ui.TextDisplay("Only Server Owner or Extra Owner can Run this Command!"))

      view.add_item(container)
      return await ctx .send (view=view)

    is_activated =row [0 ]if row else False 

    if option is None :
      # Create Components v2 layout
      view = ui.LayoutView()
      container = ui.Container(accent_color=None)

      # Title
      container.add_item(ui.TextDisplay("# Antinuke"))
      container.add_item(ui.Separator())

      # Main info with bot avatar as thumbnail
      main_info = "Boost your server security with Antinuke! It automatically bans any admins involved in suspicious activities, ensuring the safety of your whitelisted members. Strengthen your defenses – activate Antinuke today!"

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

      # Enable/Disable info
      enable_disable_info = f"**Antinuke Enable**\nTo Enable Antinuke, Use - `{pre}antinuke enable`\n\n**Antinuke Disable**\nTo Disable Antinuke, Use - `{pre}antinuke disable`"
      container.add_item(ui.TextDisplay(enable_disable_info))

      view.add_item(container)
      await ctx.send(view=view)

    elif option .lower ()=='enable':
      if is_activated :
        # Create Components v2 layout
        view = ui.LayoutView()
        container = ui.Container(accent_color=None)

        # Title
        container.add_item(ui.TextDisplay(f"# Security Settings For {ctx.guild.name}"))
        container.add_item(ui.Separator())

        # Main info with bot avatar as thumbnail
        main_info = f"Your server __**already has Antinuke enabled.**__\n\nCurrent Status: <:enable_yes:1372375008441143417> Enabled\nTo Disable use `antinuke disable`"

        if self.bot.user.avatar:
          container.add_item(
            ui.Section(
              ui.TextDisplay(main_info),
              accessory=ui.Thumbnail(self.bot.user.avatar.url)
            )
          )
        else:
          container.add_item(ui.TextDisplay(main_info))

        view.add_item(container)
        await ctx.send(view=view)
      else :

        # Create Components v2 layout for setup
        setup_view = ui.LayoutView()
        setup_container = ui.Container(accent_color=None)
        
        setup_container.add_item(ui.TextDisplay("# Antinuke Setup <a:gears_icon:1373946244321378447>"))
        setup_container.add_item(ui.Separator())
        
        setup_text = ui.TextDisplay("<a:Yuna_loading:1372527554761855038> | Initializing Quick Setup!")
        setup_container.add_item(setup_text)
        
        setup_view.add_item(setup_container)
        setup_message = await ctx.send(view=setup_view)


        if not ctx .guild .me .guild_permissions .administrator :
          setup_container.clear_items()
          setup_container.add_item(ui.TextDisplay("# Antinuke Setup <a:gears_icon:1373946244321378447>"))
          setup_container.add_item(ui.Separator())
          setup_container.add_item(ui.TextDisplay("<a:Yuna_loading:1372527554761855038> | Initializing Quick Setup!\n<:icon_danger:1373170993236803688> | Setup failed: Missing **Administrator** permission."))
          await setup_message .edit (view=setup_view)
          return 

        await asyncio .sleep (1 )
        setup_container.clear_items()
        setup_container.add_item(ui.TextDisplay("# Antinuke Setup <a:gears_icon:1373946244321378447>"))
        setup_container.add_item(ui.Separator())
        setup_container.add_item(ui.TextDisplay("<a:Yuna_loading:1372527554761855038> | Initializing Quick Setup!\n<a:Yuna_loading:1372527554761855038> Checking Yuna-bot's role position for optimal configuration..."))
        await setup_message .edit (view=setup_view)

        await asyncio .sleep (1 )
        setup_container.clear_items()
        setup_container.add_item(ui.TextDisplay("# Antinuke Setup <a:gears_icon:1373946244321378447>"))
        setup_container.add_item(ui.Separator())
        setup_container.add_item(ui.TextDisplay("<a:Yuna_loading:1372527554761855038> | Initializing Quick Setup!\n<a:Yuna_loading:1372527554761855038> Checking Yuna-bot's role position for optimal configuration...\n<a:Yuna_loading:1372527554761855038> | Crafting and configuring the Yuna Unstoppable Power role..."))
        await setup_message .edit (view=setup_view)

        try :
          role =await ctx .guild .create_role (
          name ="Yuna Unstoppable Power",
          color =0x0ba7ff ,
          permissions =discord .Permissions (administrator =True ),
          hoist =False ,
          mentionable =False ,
          reason ="Antinuke setup Role Creation"
          )
          await ctx .guild .me .add_roles (role )
        except discord .Forbidden :
          setup_container.clear_items()
          setup_container.add_item(ui.TextDisplay("# Antinuke Setup <a:gears_icon:1373946244321378447>"))
          setup_container.add_item(ui.Separator())
          setup_container.add_item(ui.TextDisplay("<a:Yuna_loading:1372527554761855038> | Initializing Quick Setup!\n<a:Yuna_loading:1372527554761855038> Checking Yuna-bot's role position for optimal configuration...\n<a:Yuna_loading:1372527554761855038> | Crafting and configuring the Yuna Unstoppable Power role...\n<:icon_danger:1373170993236803688> | Setup failed: Insufficient permissions to create role."))
          await setup_message .edit (view=setup_view)
          return 
        except discord .HTTPException as e :
          setup_container.clear_items()
          setup_container.add_item(ui.TextDisplay("# Antinuke Setup <a:gears_icon:1373946244321378447>"))
          setup_container.add_item(ui.Separator())
          setup_container.add_item(ui.TextDisplay(f"<a:Yuna_loading:1372527554761855038> | Initializing Quick Setup!\n<a:Yuna_loading:1372527554761855038> Checking Yuna-bot's role position for optimal configuration...\n<a:Yuna_loading:1372527554761855038> | Crafting and configuring the Yuna Unstoppable Power role...\n<:icon_danger:1373170993236803688> | Setup failed: HTTPException: {e}\nCheck Guild **Audit Logs**."))
          await setup_message .edit (view=setup_view)
          return 

        await asyncio .sleep (1 )
        setup_container.clear_items()
        setup_container.add_item(ui.TextDisplay("# Antinuke Setup <a:gears_icon:1373946244321378447>"))
        setup_container.add_item(ui.Separator())
        setup_container.add_item(ui.TextDisplay("<a:Yuna_loading:1372527554761855038> | Initializing Quick Setup!\n<a:Yuna_loading:1372527554761855038> Checking Yuna-bot's role position for optimal configuration...\n<a:Yuna_loading:1372527554761855038> | Crafting and configuring the Yuna Unstoppable Power role...\n<a:Yuna_loading:1372527554761855038> Ensuring precise placement of the Yuna Unstoppable Power role..."))
        await setup_message .edit (view=setup_view)
        try :
          await ctx .guild .edit_role_positions (positions ={role :1 })
        except discord .Forbidden :
          setup_container.clear_items()
          setup_container.add_item(ui.TextDisplay("# Antinuke Setup <a:gears_icon:1373946244321378447>"))
          setup_container.add_item(ui.Separator())
          setup_container.add_item(ui.TextDisplay("<a:Yuna_loading:1372527554761855038> | Initializing Quick Setup!\n<a:Yuna_loading:1372527554761855038> Checking Yuna-bot's role position for optimal configuration...\n<a:Yuna_loading:1372527554761855038> | Crafting and configuring the Yuna Unstoppable Power role...\n<a:Yuna_loading:1372527554761855038> Ensuring precise placement of the Yuna Unstoppable Power role...\n<:icon_danger:1373170993236803688> | Setup failed: Insufficient permissions to move role."))
          await setup_message .edit (view=setup_view)
          return 
        except discord .HTTPException as e :
          setup_container.clear_items()
          setup_container.add_item(ui.TextDisplay("# Antinuke Setup <a:gears_icon:1373946244321378447>"))
          setup_container.add_item(ui.Separator())
          setup_container.add_item(ui.TextDisplay(f"<a:Yuna_loading:1372527554761855038> | Initializing Quick Setup!\n<a:Yuna_loading:1372527554761855038> Checking Yuna-bot's role position for optimal configuration...\n<a:Yuna_loading:1372527554761855038> | Crafting and configuring the Yuna Unstoppable Power role...\n<a:Yuna_loading:1372527554761855038> Ensuring precise placement of the Yuna Unstoppable Power role...\n<:icon_danger:1373170993236803688> | Setup failed: HTTPException: {e}."))
          await setup_message .edit (view=setup_view)
          return 

        await asyncio .sleep (1 )
        setup_container.clear_items()
        setup_container.add_item(ui.TextDisplay("# Antinuke Setup <a:gears_icon:1373946244321378447>"))
        setup_container.add_item(ui.Separator())
        setup_container.add_item(ui.TextDisplay("<a:Yuna_loading:1372527554761855038> | Initializing Quick Setup!\n<a:Yuna_loading:1372527554761855038> Checking Yuna-bot's role position for optimal configuration...\n<a:Yuna_loading:1372527554761855038> | Crafting and configuring the Yuna Unstoppable Power role...\n<a:Yuna_loading:1372527554761855038> Ensuring precise placement of the Yuna Unstoppable Power role...\n<a:Yuna_loading:1372527554761855038> | Safeguarding your changes..."))
        await setup_message .edit (view=setup_view)

        await asyncio .sleep (1 )
        setup_container.clear_items()
        setup_container.add_item(ui.TextDisplay("# Antinuke Setup <a:gears_icon:1373946244321378447>"))
        setup_container.add_item(ui.Separator())
        setup_container.add_item(ui.TextDisplay("<a:Yuna_loading:1372527554761855038> | Initializing Quick Setup!\n<a:Yuna_loading:1372527554761855038> Checking Yuna-bot's role position for optimal configuration...\n<a:Yuna_loading:1372527554761855038> | Crafting and configuring the Yuna Unstoppable Power role...\n<a:Yuna_loading:1372527554761855038> Ensuring precise placement of the Yuna Unstoppable Power role...\n<a:Yuna_loading:1372527554761855038> | Safeguarding your changes...\n<a:Yuna_loading:1373173756113195081> | Activating the Antinuke Modules for enhanced security...!!"))
        await setup_message .edit (view=setup_view)

        await self .db .execute ('INSERT OR REPLACE INTO antinuke (guild_id, status) VALUES (?, ?)',(guild_id ,True ))
        await self .db .commit ()


        await self .enable_limit_settings (guild_id )


        try :
            from cogs .antinuke .database_migration import migrate_whitelist_table 
            await migrate_whitelist_table ()
        except Exception as e :
            print (f"Database migration warning: {e}")

        await asyncio .sleep (1 )
        await setup_message .delete ()

        # Create Components v2 layout
        view = ui.LayoutView()
        container = ui.Container(accent_color=None)

        # Title
        container.add_item(ui.TextDisplay(f"# Security Settings For {ctx.guild.name}"))
        container.add_item(ui.Separator())

        # Tip section
        tip_info = "Tip: For optimal functionality of the AntiNuke Module, please ensure that my role has **Administration** permissions and is positioned at the **Top** of the roles list"
        container.add_item(ui.TextDisplay(tip_info))

        container.add_item(ui.Separator())

        # Modules enabled section with thumbnail
        modules_info = f"<:icon_settings:1372375191405199480> **Modules Enabled**\n>>> <:disable_no:1372374999310274600><:enable_yes:1372375008441143417> **Anti Ban**\n<:disable_no:1372374999310274600><:enable_yes:1372375008441143417> **Anti Kick**\n<:disable_no:1372374999310274600><:enable_yes:1372375008441143417> **Anti Bot**\n<:disable_no:1372374999310274600><:enable_yes:1372375008441143417> **Anti Channel Create**\n<:disable_no:1372374999310274600><:enable_yes:1372375008441143417> **Anti Channel Delete**\n<:disable_no:1372374999310274600><:enable_yes:1372375008441143417> **Anti Channel Update**\n<:disable_no:1372374999310274600><:enable_yes:1372375008441143417> **Anti Everyone/Here**\n<:disable_no:1372374999310274600><:enable_yes:1372375008441143417> **Anti Role Create**\n<:disable_no:1372374999310274600><:enable_yes:1372375008441143417> **Anti Role Delete**\n<:disable_no:1372374999310274600><:enable_yes:1372375008441143417> **Anti Role Update**\n<:disable_no:1372374999310274600><:enable_yes:1372375008441143417> **Anti Member Update**\n<:disable_no:1372374999310274600><:enable_yes:1372375008441143417> **Anti Guild Update**\n<:disable_no:1372374999310274600><:enable_yes:1372375008441143417> **Anti Integration**\n<:disable_no:1372374999310274600><:enable_yes:1372375008441143417> **Anti Webhook Create**\n<:disable_no:1372374999310274600><:enable_yes:1372375008441143417> **Anti Webhook Delete**\n<:disable_no:1372374999310274600><:enable_yes:1372375008441143417> **Anti Webhook Update**\n<:disable_no:1372374999310274600><:enable_yes:1372375008441143417> **Anti Prune**\n **Auto Recovery**"

        if self.bot.user.avatar:
          container.add_item(
            ui.Section(
              ui.TextDisplay(modules_info),
              accessory=ui.Thumbnail(self.bot.user.avatar.url)
            )
          )
        else:
          container.add_item(ui.TextDisplay(modules_info))

        container.add_item(ui.Separator())

        # Footer
        footer_info = "Successfully Enabled Antinuke for this server | Powered by AeroX Development"
        container.add_item(ui.TextDisplay(footer_info))

        # Add button
        action_row = ui.ActionRow()
        action_row.add_item(ui.Button(
            label="Show Punishment Type",
            style=discord.ButtonStyle.primary,
            custom_id="show_punishment"
        ))
        container.add_item(action_row)

        view.add_item(container)
        await ctx.send(view=view)

    elif option .lower ()=='disable':
      if not is_activated :
        # Create Components v2 layout
        view = ui.LayoutView()
        container = ui.Container(accent_color=None)

        # Title
        container.add_item(ui.TextDisplay(f"# Security Settings For {ctx.guild.name}"))
        container.add_item(ui.Separator())

        # Main info with bot avatar as thumbnail
        main_info = f"Uhh, looks like your server hasn't enabled Antinuke.\n\nCurrent Status: <:disable_no:1372374999310274600><:enable_yes:1372375008441143417> Disabled\n\nTo Enable use `antinuke enable`"

        if self.bot.user.avatar:
          container.add_item(
            ui.Section(
              ui.TextDisplay(main_info),
              accessory=ui.Thumbnail(self.bot.user.avatar.url)
            )
          )
        else:
          container.add_item(ui.TextDisplay(main_info))

        view.add_item(container)
        await ctx.send(view=view)
      else :
        await self .db .execute ('DELETE FROM antinuke WHERE guild_id = ?',(guild_id ,))
        await self .db .commit ()


        await self .disable_limit_settings (guild_id )

        # Create Components v2 layout
        view = ui.LayoutView()
        container = ui.Container(accent_color=None)

        # Title
        container.add_item(ui.TextDisplay(f"# Security Settings For {ctx.guild.name}"))
        container.add_item(ui.Separator())

        # Main info with bot avatar as thumbnail
        main_info = f"Successfully disabled Antinuke for this server.\n\nCurrent Status: <:disable_no:1372374999310274600><:enable_yes:1372375008441143417> Disabled\n\nTo Enable use `antinuke enable`"

        if self.bot.user.avatar:
          container.add_item(
            ui.Section(
              ui.TextDisplay(main_info),
              accessory=ui.Thumbnail(self.bot.user.avatar.url)
            )
          )
        else:
          container.add_item(ui.TextDisplay(main_info))

        view.add_item(container)
        await ctx.send(view=view)
    else :
      # Create Components v2 layout
      view = ui.LayoutView()
      container = ui.Container(accent_color=None)

      # Title
      container.add_item(ui.TextDisplay("# Invalid Option"))
      container.add_item(ui.Separator())

      # Main info
      container.add_item(ui.TextDisplay("Invalid option. Please use `enable` or `disable`."))

      view.add_item(container)
      await ctx.send(view=view)


  @commands .Cog .listener ()
  async def on_interaction (self ,interaction :discord .Interaction ):
    if interaction .data .get ('custom_id')=='show_punishment':

      # Create Components v2 layout
      view = ui.LayoutView()
      container = ui.Container(accent_color=None)

      # Title
      container.add_item(ui.TextDisplay("# Punishment Types for Changes Made by Unwhitelisted Admins/Mods"))
      container.add_item(ui.Separator())

      # Punishment types info
      punishment_info = (
      "**Anti Ban:** Ban\n"
      "**Anti Kick:** Ban\n"
      "**Anti Bot:** Ban the bot Inviter\n"
      "**Anti Channel Create/Delete/Update:** Ban\n"
      "**Anti Everyone/Here:** Remove the message & 1 hour timeout\n"
      "**Anti Role Create/Delete/Update:** Ban\n"
      "**Anti Member Update:** Ban\n"
      "**Anti Guild Update:** Ban\n"
      "**Anti Integration:** Ban\n"
      "**Anti Webhook Create/Delete/Update:** Ban\n"
      "**Anti Prune:** Ban\n"
      "**Auto Recovery:** Automatically recover damaged channels, roles, and settings\n\n"
      "Note: In the case of member updates, action will be taken only if the role contains dangerous permissions such as Ban Members, Administrator, Manage Guild, Manage Channels, Manage Roles, Manage Webhooks, or Mention Everyone"
      )
      container.add_item(ui.TextDisplay(punishment_info))

      container.add_item(ui.Separator())

      # Footer
      footer_info = "These punishment types are fixed and assigned as required to ensure guild security/protection"
      container.add_item(ui.TextDisplay(footer_info))

      view.add_item(container)
      await interaction .response .send_message (view=view ,ephemeral =True )

async def setup (bot ):
  await bot .add_cog (Antinuke (bot ))


"""
: ! Aegis !
    + Discord: itsfizys
    + Community: https://discord.gg/aerox (AeroX Development )
    + for any queries reach out Community or DM me.
"""
