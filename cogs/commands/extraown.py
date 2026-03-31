"""
: ! Aegis !
    + Discord: itsfizys
    + Community: https://discord.gg/aerox (AeroX Development )
    + for any queries reach out Community or DM me.
"""
import discord 
from discord .ext import commands 
from discord import ui
import aiosqlite 
from utils .Tools import *

class ConfirmView(ui.LayoutView):
    def __init__(self, ctx, action_type, user=None):
        super().__init__(timeout=60.0)
        self.ctx = ctx
        self.value = None
        self.action_type = action_type
        self.user = user

        self.container = ui.Container(accent_color=None)
        
        if action_type == "set":
            title = "# Confirm Extra Owner Assignment"
            description = f"Are you sure you want to set {user.mention} as the Extra Owner?\n\n**This will grant them access to:**\n<:enable_yes:1372375008441143417> Antinuke settings management\n<:enable_yes:1372375008441143417> Whitelist event configuration\n<:enable_yes:1372375008441143417> Security controls"
        else:  # reset
            title = "# Confirm Extra Owner Removal"
            description = "Are you sure you want to remove the current Extra Owner?\n\n**This will revoke their access to:**\n<:disable_no:1372374999310274600> Antinuke settings management\n<:disable_no:1372374999310274600> Whitelist event configuration\n<:disable_no:1372374999310274600> Security controls"
        
        self.container.add_item(ui.TextDisplay(title))
        self.container.add_item(ui.Separator())
        
        if ctx.bot.user.avatar:
            self.container.add_item(ui.Section(ui.TextDisplay(description), accessory=ui.Thumbnail(ctx.bot.user.avatar.url)))
        else:
            self.container.add_item(ui.TextDisplay(description))
        
        self.container.add_item(ui.Separator())
        self.container.add_item(ui.TextDisplay(f"**Executor:** {ctx.author.mention}"))
        self.container.add_item(ui.Separator())
        
        button_row = ui.ActionRow(
            ui.Button(label="Confirm", style=discord.ButtonStyle.success, custom_id="confirm"),
            ui.Button(label="Cancel", style=discord.ButtonStyle.danger, custom_id="cancel")
        )
        button_row.children[0].callback = self.confirm
        button_row.children[1].callback = self.cancel
        self.container.add_item(button_row)
        
        self.add_item(self.container)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user != self.ctx.author:
            await interaction.response.send_message("You cannot interact with this confirmation.", ephemeral=True)
            return False
        return True

    async def confirm(self, interaction: discord.Interaction):
        await interaction.response.defer()
        self.value = True
        self.stop()
        
    async def cancel(self, interaction: discord.Interaction):
        await interaction.response.defer()
        self.value = False
        self.stop()


class Extraowner (commands .Cog ):
    def __init__ (self ,bot ):
        self .bot =bot 
        self .bot .loop .create_task (self .initialize_db ())

    async def initialize_db (self ):
        from db._db import Database
        self .db = Database('db/anti.db')
        db_conn = await self .db .connect()
        
        async def create_table():
            await db_conn.execute('''
                CREATE TABLE IF NOT EXISTS extraowners (
                    guild_id INTEGER PRIMARY KEY,
                    owner_id INTEGER
                )
            ''')
            await db_conn.commit()
        
        await self.db.execute_with_retries(create_table)

    @commands .hybrid_command (name ='extraowner',aliases =["owner"],help ="Adds Extraowner to the server")
    @blacklist_check ()
    @ignore_check ()
    @commands .cooldown (1 ,10 ,commands .BucketType .user )
    @commands .max_concurrency (1 ,per =commands .BucketType .default ,wait =False )
    @commands .guild_only ()
    async def extraowner (self ,ctx ,option :str =None ,user :discord .Member =None ):
        guild_id =ctx .guild .id 

        if ctx .guild .member_count <2 :
            view = ui.LayoutView()
            container = ui.Container(accent_color=None)
            container.add_item(ui.TextDisplay("# Error"))
            container.add_item(ui.Separator())
            container.add_item(ui.TextDisplay("<:icon_cross:1372375094336425986> | Your Server Doesn't Meet My 30 Member Criteria"))
            view.add_item(container)
            return await ctx .send (view=view)

        if ctx .author .id !=ctx .guild .owner_id :
            view = ui.LayoutView()
            container = ui.Container(accent_color=None)
            container.add_item(ui.TextDisplay("# <:icon_cross:1372375094336425986> Access Denied"))
            container.add_item(ui.Separator())
            container.add_item(ui.TextDisplay("Only Server Owner Can Run This Command"))
            view.add_item(container)
            return await ctx .send (view=view)

        if option is None :
            pre =ctx .prefix 
            view = ui.LayoutView()
            container = ui.Container(accent_color=None)
            
            container.add_item(ui.TextDisplay(f"# {ctx.guild.name} Extra Owner Management"))
            container.add_item(ui.Separator())
            
            main_info = (
                "Extraowners can adjust server antinuke settings & manage whitelist events, "
                "so careful consideration is essential before assigning it to someone.\n\n"
                f"**Available Commands:**\n"
                f"<a:Arrowright:1376605813820489820> `{pre}extraowner set @user` - Set Extra Owner\n"
                f"<a:Arrowright:1376605813820489820> `{pre}extraowner reset` - Remove Extra Owner\n"
                f"<a:Arrowright:1376605813820489820> `{pre}extraowner view` - View Current Extra Owner"
            )
            
            if ctx.bot.user.avatar:
                container.add_item(ui.Section(ui.TextDisplay(main_info), accessory=ui.Thumbnail(ctx.bot.user.avatar.url)))
            else:
                container.add_item(ui.TextDisplay(main_info))
            
            container.add_item(ui.Separator())
            container.add_item(ui.TextDisplay(f"**Executor:** {ctx.author.mention}"))
            view.add_item(container)
            return await ctx .reply (view=view)


        if option .lower ()=='set':
            if user is None or user .bot :
                view = ui.LayoutView()
                container = ui.Container(accent_color=None)
                container.add_item(ui.TextDisplay("# Invalid User"))
                container.add_item(ui.Separator())
                container.add_item(ui.TextDisplay("Please Provide a Valid User Mention or ID to Set as Extra Owner!"))
                view.add_item(container)
                return await ctx .reply (view=view)

            view = ConfirmView(ctx, "set", user)
            message = await ctx.reply(view=view)
            await view.wait()

            if view.value is None:
                timeout_view = ui.LayoutView()
                container = ui.Container(accent_color=None)
                container.add_item(ui.TextDisplay("# ⏱️ Timeout"))
                container.add_item(ui.Separator())
                container.add_item(ui.TextDisplay("Confirmation timed out."))
                timeout_view.add_item(container)
                await message.edit(view=timeout_view)
            elif view.value:
                db_conn = await self.db.ensure_connection()
                
                async def set_owner():
                    await db_conn.execute(
                        'INSERT OR REPLACE INTO extraowners (guild_id, owner_id) VALUES (?, ?)',
                        (guild_id, user.id)
                    )
                    await db_conn.commit()
                
                await self.db.execute_with_retries(set_owner)
                
                success_view = ui.LayoutView()
                container = ui.Container(accent_color=None)
                container.add_item(ui.TextDisplay("# <:icon_tick:1372375089668161597> Success"))
                container.add_item(ui.Separator())
                container.add_item(ui.TextDisplay(f"Successfully added {user.mention} as Extra Owner!"))
                container.add_item(ui.Separator())
                container.add_item(ui.TextDisplay(f"**Executor:** {ctx.author.mention}\n**Target:** {user.mention}"))
                success_view.add_item(container)
                await message.edit(view=success_view)
            else:
                cancel_view = ui.LayoutView()
                container = ui.Container(accent_color=None)
                container.add_item(ui.TextDisplay("# <:icon_cross:1372375094336425986> Cancelled"))
                container.add_item(ui.Separator())
                container.add_item(ui.TextDisplay("Action cancelled."))
                cancel_view.add_item(container)
                await message.edit(view=cancel_view)


        elif option .lower ()=='reset':
            db_conn = await self.db.ensure_connection()
            
            async with db_conn.execute(
                'SELECT owner_id FROM extraowners WHERE guild_id = ?',
                (guild_id,)
            ) as cursor:
                row = await cursor.fetchone()

            if not row :
                view = ui.LayoutView()
                container = ui.Container(accent_color=None)
                container.add_item(ui.TextDisplay("# No Extra Owner"))
                container.add_item(ui.Separator())
                container.add_item(ui.TextDisplay("No extra owner has been designated for this guild."))
                view.add_item(container)
                return await ctx .reply (view=view)
            else :
                view = ConfirmView(ctx, "reset")
                message = await ctx.reply(view=view)
                await view.wait()

                if view.value is None:
                    timeout_view = ui.LayoutView()
                    container = ui.Container(accent_color=None)
                    container.add_item(ui.TextDisplay("# ⏱️ Timeout"))
                    container.add_item(ui.Separator())
                    container.add_item(ui.TextDisplay("Confirmation timed out."))
                    timeout_view.add_item(container)
                    await message.edit(view=timeout_view)
                elif view.value:
                    async def reset_owner():
                        await db_conn.execute(
                            'DELETE FROM extraowners WHERE guild_id = ?',
                            (guild_id,)
                        )
                        await db_conn.commit()
                    
                    await self.db.execute_with_retries(reset_owner)
                    
                    success_view = ui.LayoutView()
                    container = ui.Container(accent_color=None)
                    container.add_item(ui.TextDisplay("# <:icon_tick:1372375089668161597> Success"))
                    container.add_item(ui.Separator())
                    container.add_item(ui.TextDisplay("Successfully disabled Extra Owner configuration!"))
                    container.add_item(ui.Separator())
                    container.add_item(ui.TextDisplay(f"**Executor:** {ctx.author.mention}"))
                    success_view.add_item(container)
                    await message.edit(view=success_view)
                else:
                    cancel_view = ui.LayoutView()
                    container = ui.Container(accent_color=None)
                    container.add_item(ui.TextDisplay("# <:icon_cross:1372375094336425986> Cancelled"))
                    container.add_item(ui.Separator())
                    container.add_item(ui.TextDisplay("Action cancelled."))
                    cancel_view.add_item(container)
                    await message.edit(view=cancel_view)

        elif option .lower ()=='view':
            db_conn = await self.db.ensure_connection()
            
            async with db_conn.execute(
                'SELECT owner_id FROM extraowners WHERE guild_id = ?',
                (guild_id,)
            ) as cursor:
                row = await cursor.fetchone()

            if not row :
                view = ui.LayoutView()
                container = ui.Container(accent_color=None)
                container.add_item(ui.TextDisplay("# No Extra Owner"))
                container.add_item(ui.Separator())
                container.add_item(ui.TextDisplay("No extra owner is currently assigned."))
                view.add_item(container)
                return await ctx .reply (view=view)
            else :
                view = ui.LayoutView()
                container = ui.Container(accent_color=None)
                container.add_item(ui.TextDisplay(f"# {ctx.guild.name} Extra Owner"))
                container.add_item(ui.Separator())
                container.add_item(ui.TextDisplay(f"Current Extra Owner: <@{row[0]}>"))
                container.add_item(ui.Separator())
                container.add_item(ui.TextDisplay(f"**Requested by:** {ctx.author.mention}"))
                view.add_item(container)
                return await ctx .reply (view=view)


"""
: ! Aegis !
    + Discord: itsfizys
    + Community: https://discord.gg/aerox (AeroX Development )
    + for any queries reach out Community or DM me.
"""
