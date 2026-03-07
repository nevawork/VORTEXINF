"""
: ! Aegis !
    + Discord: itsfizys
    + Community: https://discord.gg/aerox (AeroX Development )
    + for any queries reach out Community or DM me.
"""
import discord 
from discord .ext import commands ,tasks 
from discord import ui
import asyncio 
import datetime 
import re 
from typing import *
from utils .Tools import *
from discord .ui import Button ,View 
from typing import Union ,Optional 
from typing import Union ,Optional 
from io import BytesIO 
import requests 
import aiohttp 
import time 
from datetime import datetime ,timezone ,timedelta 
from collections import Counter


time_regex =re .compile (r"(?:(\d{1,5})(h|s|m|d))+?")
time_dict ={"h":3600 ,"s":1 ,"m":60 ,"d":86400 }


def convert (argument ):
  args =argument .lower ()
  matches =re .findall (time_regex ,args )
  time =0 
  for key ,value in matches :
    try :
      time +=time_dict [value ]*float (key )
    except KeyError :
      raise commands .BadArgument (
      f"{value} is an invalid time key! h|m|s|d are valid arguments")
    except ValueError :
      raise commands .BadArgument (f"{key} is not a number!")
  return round (time )

async def do_removal (ctx ,limit ,predicate ,*,before =None ,after =None ):
  if limit >2000 :
      return await ctx .send (f"Too many messages to search given ({limit}/2000)")

  if before is None :
      before =ctx .message 
  else :
      before =discord .Object (id =before )

  if after is not None :
      after =discord .Object (id =after )

  try :
      deleted =await ctx .channel .purge (limit =limit ,before =before ,after =after ,check =predicate )
  except discord .Forbidden as e :
      return await ctx .send ("I do not have permissions to delete messages.")
  except discord .HTTPException as e :
      return await ctx .send (f"Error: {e} (try a smaller search?)")

  spammers =Counter (m .author .display_name for m in deleted )
  deleted_count =len (deleted )
  
  temp_container = ui.Container(accent_color=None)
  
  temp_container.add_item(
      ui.TextDisplay(f"<:icon_tick:1372375089668161597> | {deleted_count} message{' was' if deleted_count == 1 else 's were'} removed.")
  )
  
  if deleted_count > 0:
      temp_container.add_item(ui.Separator())
      spammers = sorted(spammers.items(), key=lambda t: t[1], reverse=True)
      
      user_breakdown = []
      for name, count in spammers:
          user_breakdown.append(f"**{name}**: {count}")
      
      if user_breakdown:
          breakdown_text = "\n".join(user_breakdown)
          if len(breakdown_text) <= 1000:  # Discord limit for text display
              temp_container.add_item(ui.TextDisplay(breakdown_text))
          else:
              temp_container.add_item(ui.TextDisplay("Multiple users affected - check audit log for details"))
  
  temp_view = ui.LayoutView()
  temp_view.add_item(temp_container)
  
  temp_msg = await ctx.send(view=temp_view)
  
  async def auto_delete():
      await asyncio.sleep(7)
      try:
          await temp_msg.delete()
      except (discord.NotFound, discord.Forbidden, discord.HTTPException):
          pass
  
  asyncio.create_task(auto_delete())


class PurgeAmountModal(ui.Modal, title="Purge Amount"):
    def __init__(self, view, purge_type, operation_title):
        super().__init__()
        self.view = view
        self.purge_type = purge_type
        self.operation_title = operation_title
        
        self.amount_input = ui.TextInput(
            label="Number of messages to purge",
            placeholder="Enter amount (1-2000, default: 100)",
            default="100",
            required=True,
            max_length=4
        )
        self.add_item(self.amount_input)
        
        if purge_type == "user":
            self.user_input = ui.TextInput(
                label="User ID or mention",
                placeholder="Enter user ID or @mention",
                required=True,
                max_length=50
            )
            self.add_item(self.user_input)
        elif purge_type == "contains":
            self.text_input = ui.TextInput(
                label="Text to search for",
                placeholder="Enter text to search for in messages (min 3 chars)",
                required=True,
                max_length=100
            )
            self.add_item(self.text_input)
    
    async def on_submit(self, interaction: discord.Interaction):
        try:
            amount = int(self.amount_input.value)
            if amount < 1 or amount > 2000:
                await interaction.response.send_message(
                    "<:dot:1479361908766281812>  Amount must be between 1 and 2000.", 
                    ephemeral=True
                )
                return
        except ValueError:
            await interaction.response.send_message(
                "<:dot:1479361908766281812>  Please enter a valid number.", 
                ephemeral=True
            )
            return
        
        if self.purge_type == "user":
            user_input = self.user_input.value.strip()
            if not user_input:
                await interaction.response.send_message(
                    "<:dot:1479361908766281812>  Please enter a user ID or mention.", 
                    ephemeral=True
                )
                return
            
            user = None
            if user_input.startswith('<@') and user_input.endswith('>'):
                user_id = user_input[2:-1].replace('!', '')
                try:
                    user = self.view.ctx.guild.get_member(int(user_id))
                except ValueError:
                    pass
            else:
                try:
                    user = self.view.ctx.guild.get_member(int(user_input))
                except ValueError:
                    pass
            
            if not user:
                await interaction.response.send_message(
                    "<:dot:1479361908766281812>  User not found. Please enter a valid user ID or mention.", 
                    ephemeral=True
                )
                return
        
        elif self.purge_type == "contains":
            search_text = self.text_input.value.strip()
            if len(search_text) < 3:
                await interaction.response.send_message(
                    "<:dot:1479361908766281812>  Search text must be at least 3 characters long.", 
                    ephemeral=True
                )
                return
        
        await interaction.response.defer()
        
        self.view.purged_amount = amount
        self.view.purged_operation = self.operation_title
        
        if self.purge_type == "all":
            await do_removal(self.view.ctx, amount, lambda e: True)
        elif self.purge_type == "user":
            await do_removal(self.view.ctx, amount, lambda e: e.author == user)
        elif self.purge_type == "contains":
            await do_removal(self.view.ctx, amount, lambda e: search_text in e.content)
        elif self.purge_type == "bots":
            def predicate(m):
                return m.webhook_id is None and m.author.bot
            await do_removal(self.view.ctx, amount, predicate)
        elif self.purge_type == "files":
            await do_removal(self.view.ctx, amount, lambda e: len(e.attachments) or len(e.embeds))
        elif self.purge_type == "embeds":
            await do_removal(self.view.ctx, amount, lambda e: len(e.embeds))
        elif self.purge_type == "emojis":
            custom_emoji = re.compile(r"<a?:[a-zA-Z0-9\_]+:([0-9]+)>")
            def predicate(m):
                return custom_emoji.search(m.content)
            await do_removal(self.view.ctx, amount, predicate)
        elif self.purge_type == "reactions":
            if amount > 2000:
                return await self.view.ctx.send(f"Too many messages to search for ({amount}/2000)")

            total_reactions = 0
            async for message in self.view.ctx.history(limit=amount, before=self.view.ctx.message):
                if len(message.reactions):
                    total_reactions += sum(r.count for r in message.reactions)
                    await message.clear_reactions()

            await self.view.ctx.send(f"<:icon_tick:1372375089668161597> | Successfully removed {total_reactions} reactions.", delete_after=7)
        
        self.view.setup_completion_content()
        await interaction.edit_original_response(view=self.view)


class PurgeView(ui.LayoutView):
    def __init__(self, ctx, bot):
        super().__init__(timeout=300.0)
        self.ctx = ctx
        self.bot = bot
        self.current_page = "main"
        self.purged_amount = 0
        self.purged_operation = ""
        
        self.container = ui.Container(accent_color=None)
        
        self.purge_select = ui.ActionRow(
            ui.Select(
                placeholder="Select purge operation type",
                options=[
                    discord.SelectOption(
                        label="All Messages",
                        description="Clear all messages in channel",
                        value="all"
                    ),
                    discord.SelectOption(
                        label="User Messages", 
                        description="Clear messages from specific user",
                        value="user"
                    ),
                    discord.SelectOption(
                        label="Bot Messages",
                        description="Clear bot messages only", 
                        value="bots"
                    ),
                    discord.SelectOption(
                        label="Files & Images",
                        description="Clear messages with attachments",
                        value="files"
                    ),
                    discord.SelectOption(
                        label="Embeds",
                        description="Clear messages with embeds",
                        value="embeds"
                    ),
                    discord.SelectOption(
                        label="Custom Emojis",
                        description="Clear messages with custom emojis",
                        value="emojis"
                    ),
                    discord.SelectOption(
                        label="Contains Text",
                        description="Clear messages containing specific text",
                        value="contains"
                    ),
                    discord.SelectOption(
                        label="Reactions Only",
                        description="Clear all reactions from messages",
                        value="reactions"
                    )
                ]
            )
        )
        self.purge_select.children[0].callback = self.select_callback
        
        self.setup_main_content()
        
        self.add_item(self.container)
    
    def setup_main_content(self):
        """Set up the main purge interface"""
        self.container.clear_items()
        
        self.container.add_item(ui.TextDisplay("# Message Purge System"))
        self.container.add_item(ui.Separator())
        
        if self.bot.user.avatar:
            self.container.add_item(
                ui.Section(
                    ui.TextDisplay("<:dot:1479361908766281812>  **Advanced message management system**\n<:dot:1479361908766281812>  **Supports up to 2000 messages per operation**\n<:dot:1479361908766281812>  **Multiple filtering options available**\n<:dot:1479361908766281812>  **Safe and logged operations**"),
                    accessory=ui.Thumbnail(self.bot.user.avatar.url)
                )
            )
        else:
            self.container.add_item(
                ui.TextDisplay("<:dot:1479361908766281812>  **Advanced message management system**\n<:dot:1479361908766281812>  **Supports up to 2000 messages per operation**\n<:dot:1479361908766281812>  **Multiple filtering options available**\n<:dot:1479361908766281812>  **Safe and logged operations**")
            )
        
        self.container.add_item(ui.Separator())
        
        self.container.add_item(self.purge_select)
        
        self.container.add_item(ui.Separator())
        
        gif_gallery = ui.MediaGallery()
        gif_gallery.add_item(media="https://cdn.discordapp.com/attachments/1414256332592254986/1427906981506715729/standard_1.gif")
        self.container.add_item(gif_gallery)
    
    def setup_completion_content(self):
        """Show completion screen with formatted results"""
        self.container.clear_items()
        
        self.container.add_item(ui.TextDisplay("# Purge Operation Completed"))
        self.container.add_item(ui.Separator())
        
        operation_details = f"<:dot:1479361908766281812>  **Operation Type:** {self.purged_operation}\n<:dot:1479361908766281812>  **Messages Processed:** {self.purged_amount}\n<:dot:1479361908766281812>  **Channel:** {self.ctx.channel.mention}\n<:dot:1479361908766281812>  **Executed:** <t:{int(time.time())}:R>"
        
        if self.bot.user.avatar:
            self.container.add_item(
                ui.Section(
                    ui.TextDisplay(operation_details),
                    accessory=ui.Thumbnail(self.bot.user.avatar.url)
                )
            )
        else:
            self.container.add_item(ui.TextDisplay(operation_details))
        
        self.container.add_item(ui.Separator())
        
        back_row = ui.ActionRow()
        back_btn = ui.Button(
            label="Back to Main Menu",
            style=discord.ButtonStyle.primary,
            custom_id="back_main"
        )
        
        async def back_callback(interaction):
            if interaction.user != self.ctx.author:
                return await interaction.response.send_message("Only the command author can use this!", ephemeral=True)
            
            self.setup_main_content()
            await interaction.response.edit_message(view=self)
        
        back_btn.callback = back_callback
        back_row.add_item(back_btn)
        self.container.add_item(back_row)
        
        self.container.add_item(ui.Separator())
        
        gif_gallery = ui.MediaGallery()
        gif_gallery.add_item(media="https://cdn.discordapp.com/attachments/1414256332592254986/1427906981506715729/standard_1.gif")
        self.container.add_item(gif_gallery)
    
    async def select_callback(self, interaction: discord.Interaction):
        """Handle purge option selection"""
        if interaction.user != self.ctx.author:
            await interaction.response.send_message("Only the command author can use this!", ephemeral=True)
            return
        
        values = getattr(interaction, 'data', {}).get('values', []) if hasattr(interaction, 'data') and interaction.data else []
        choice = values[0] if values else 'all'
        
        choice_map = {
            "all": "All Messages",
            "user": "User Messages",
            "bots": "Bot Messages",
            "files": "Files & Images",
            "embeds": "Embeds",
            "emojis": "Custom Emojis",
            "contains": "Contains Text",
            "reactions": "Reactions Only"
        }
        
        operation_title = choice_map.get(choice, "Unknown")
        
        modal = PurgeAmountModal(self, choice, operation_title)
        await interaction.response.send_modal(modal)
    
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return interaction.user == self.ctx.author


class Message (commands .Cog ):

  def __init__ (self ,bot ):
    self .bot =bot 
    self .color =0x000000 


  @commands .group (invoke_without_command =True ,aliases =["purge"],help ="Clears the messages")
  @blacklist_check ()
  @ignore_check ()
  @commands .cooldown (1 ,3 ,commands .BucketType .user )
  @commands .has_permissions (manage_messages =True )
  @commands .bot_has_permissions (manage_messages =True )
  async def clear (self ,ctx ,choice :Union [discord .Member ,int ]=None ,amount :int =None ):
        if choice is None:
            loading_container = ui.Container(
                ui.TextDisplay("<a:Yuna_loading:1373173756113195081> Loading purge interface..."),
                accent_color=None
            )
            loading_view = ui.LayoutView()
            loading_view.add_item(loading_container)
            
            processing_message = await ctx.send(view=loading_view)
            
            view = PurgeView(ctx, self.bot)
            
            await ctx.reply(view=view)
            await processing_message.delete()
            return

        await ctx .message .delete ()

        if isinstance(choice, discord.Member):
            limit = amount or 5  # default to 5 messages if no amount specified
            if limit > 2000:
                return await ctx.send(f"Too many messages to search given ({limit}/2000)")
            if limit < 1:
                return await ctx.send("Message limit must be at least 1")
            return await do_removal(ctx, limit, lambda e: e.author == choice)
            
        elif isinstance(choice, int):
            if choice > 2000:
                return await ctx.send(f"Too many messages to search given ({choice}/2000)")
            if choice < 1:
                return await ctx.send("Message limit must be at least 1")
            return await do_removal(ctx, choice, lambda e: True)



  @clear .command (help ="Clears the messages having embeds")
  @blacklist_check ()
  @ignore_check ()
  @commands .cooldown (1 ,3 ,commands .BucketType .user )
  @commands .has_permissions (manage_messages =True )
  @commands .bot_has_permissions (manage_messages =True )
  async def embeds (self ,ctx ,search =100 ):
        await ctx .message .delete ()
        await do_removal (ctx ,search ,lambda e :len (e .embeds ))


  @clear .command (help ="Clears the messages having files")
  @blacklist_check ()
  @ignore_check ()
  @commands .cooldown (1 ,3 ,commands .BucketType .user )
  @commands .has_permissions (manage_messages =True )
  @commands .bot_has_permissions (manage_messages =True )
  async def files (self ,ctx ,search =100 ):

        await ctx .message .delete ()
        await do_removal (ctx ,search ,lambda e :len (e .attachments ))

  @clear .command (help ="Clears the messages having images")
  @blacklist_check ()
  @ignore_check ()
  @commands .cooldown (1 ,3 ,commands .BucketType .user )
  @commands .has_permissions (manage_messages =True )
  @commands .bot_has_permissions (manage_messages =True )
  async def images (self ,ctx ,search =100 ):

        await ctx .message .delete ()
        await do_removal (ctx ,search ,lambda e :len (e .embeds )or len (e .attachments ))


  @clear .command (name ="all",help ="Clears all messages")
  @blacklist_check ()
  @ignore_check ()
  @commands .cooldown (1 ,3 ,commands .BucketType .user )
  @commands .has_permissions (manage_messages =True )
  @commands .bot_has_permissions (manage_messages =True )
  async def _remove_all (self ,ctx ,search =100 ):

        await ctx .message .delete ()
        await do_removal (ctx ,search ,lambda e :True )

  @clear .command (help ="Clears the messages of a specific user")
  @commands .has_permissions (manage_messages =True )
  @commands .bot_has_permissions (manage_messages =True )
  async def user (self ,ctx ,member :discord .Member ,search =100 ):

        await ctx .message .delete ()
        await do_removal (ctx ,search ,lambda e :e .author ==member )



  @clear .command (help ="Clears the messages containing a specifix string")
  @blacklist_check ()
  @ignore_check ()
  @commands .cooldown (1 ,3 ,commands .BucketType .user )
  @commands .has_permissions (manage_messages =True )
  @commands .bot_has_permissions (manage_messages =True )
  async def contains (self ,ctx ,*,string :str ):

        await ctx .message .delete ()
        if len (string )<3 :
            await ctx .send ("The substring length must be at least 3 characters.")
        else :
            await do_removal (ctx ,100 ,lambda e :string in e .content )

  @clear .command (name ="bot",aliases =["bots","b"],help ="Clears the messages sent by bot")
  @blacklist_check ()
  @ignore_check ()
  @commands .cooldown (1 ,3 ,commands .BucketType .user )
  @commands .has_permissions (manage_messages =True )
  @commands .bot_has_permissions (manage_messages =True )
  async def _bot (self ,ctx ,prefix =None ,search =100 ):

        await ctx .message .delete ()

        def predicate (m ):
            return (m .webhook_id is None and m .author .bot )or (prefix and m .content .startswith (prefix ))

        await do_removal (ctx ,search ,predicate )

  @clear .command (name ="emoji",aliases =["emojis"],help ="Clears the messages having emojis")
  @blacklist_check ()
  @ignore_check ()
  @commands .cooldown (1 ,3 ,commands .BucketType .user )
  @commands .has_permissions (manage_messages =True )
  @commands .bot_has_permissions (manage_messages =True )

  async def _emoji (self ,ctx ,search =100 ):

        await ctx .message .delete ()
        custom_emoji =re .compile (r"<a?:[a-zA-Z0-9\_]+:([0-9]+)>")

        def predicate (m ):
            return custom_emoji .search (m .content )

        await do_removal (ctx ,search ,predicate )

  @clear .command (name ="reactions",help ="Clears the reaction from the messages")
  @blacklist_check ()
  @ignore_check ()
  @commands .cooldown (1 ,3 ,commands .BucketType .user )
  @commands .has_permissions (manage_messages =True )
  @commands .bot_has_permissions (manage_messages =True )
  async def _reactions (self ,ctx ,search =100 ):

        await ctx .message .delete ()

        if search >2000 :
            return await ctx .send (f"Too many messages to search for ({search}/2000)")

        total_reactions =0 
        async for message in ctx .history (limit =search ,before =ctx .message ):
            if len (message .reactions ):
                total_reactions +=sum (r .count for r in message .reactions )
                await message .clear_reactions ()

        await ctx .send (f"<:icon_tick:1372375089668161597> | Successfully removed {total_reactions} reactions.")




  @commands .command (name ="purgebots",
  aliases =["cleanup","pb","clearbot","clearbots"],
  help ="Clear recently bot messages in channel")
  @blacklist_check ()
  @ignore_check ()
  @commands .cooldown (1 ,3 ,commands .BucketType .user )
  @commands .has_permissions (manage_messages =True )
  @commands .bot_has_permissions (manage_messages =True )
  async def _purgebot (self ,ctx ,prefix =None ,search =100 ):

    await ctx .message .delete ()

    def predicate (m ):
        return (m .webhook_id is None and m .author .bot )or (prefix and m .content .startswith (prefix ))

    await do_removal (ctx ,search ,predicate )


  @commands .command (name ="purgeuser",
  aliases =["pu","cu","clearuser"],
  help ="Clear recent messages of a user in channel")
  @blacklist_check ()
  @ignore_check ()
  @commands .cooldown (1 ,3 ,commands .BucketType .user )
  @commands .has_permissions (manage_messages =True )
  @commands .bot_has_permissions (manage_messages =True )
  async def purguser (self ,ctx ,member :discord .Member ,search =100 ):

      await ctx .message .delete ()
      await do_removal (ctx ,search ,lambda e :e .author ==member )


"""
: ! Aegis !
    + Discord: itsfizys
    + Community: https://discord.gg/aerox (AeroX Development )
    + for any queries reach out Community or DM me.
"""
