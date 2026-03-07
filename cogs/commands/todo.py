"""
: ! Aegis !
    + Discord: itsfizys
    + Community: https://discord.gg/aerox (AeroX Development )
    + for any queries reach out Community or DM me.
"""
import discord
from discord.ext import commands
from discord import ui
import aiosqlite
from typing import Optional
from utils.logger import logger

DATABASE_PATH = 'db/todos.db'

class TodoList(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_initialized = False
        
    async def cog_load(self):
        await self.init_database()
        
    async def init_database(self):
        try:
            async with aiosqlite.connect(DATABASE_PATH) as db:
                await db.execute("""
                    CREATE TABLE IF NOT EXISTS todos (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        userId INTEGER NOT NULL,
                        guildId INTEGER NOT NULL,
                        task TEXT NOT NULL,
                        completed INTEGER DEFAULT 0,
                        created_at TEXT DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                await db.commit()
                self.db_initialized = True
                logger.success("DATABASE", "Todo database initialized successfully")
        except Exception as e:
            logger.error(f"Todo database initialization error: {e}")
            
    @commands.group(name="todo", aliases=["task", "tasks"], invoke_without_command=True)
    async def todo(self, ctx):
        pass
            
    @todo.command(name="add")
    async def todo_add(self, ctx, *, task: Optional[str] = None):
        if not task or task.strip() == "":
            error_view = ui.LayoutView()
            error_container = ui.Container(accent_color=None)
            error_container.add_item(ui.TextDisplay("# Missing Task"))
            error_container.add_item(ui.Separator())
            error_container.add_item(ui.TextDisplay(
                "Please provide a task to add to your todo list.\n\n"
                "**Usage:** `todo add <task>`\n"
                "**Example:** `todo add Complete project documentation`"
            ))
            error_view.add_item(error_container)
            await ctx.send(view=error_view)
            return
            
        if len(task) > 500:
            error_view = ui.LayoutView()
            error_container = ui.Container(accent_color=None)
            error_container.add_item(ui.TextDisplay("# Task Too Long"))
            error_container.add_item(ui.Separator())
            error_container.add_item(ui.TextDisplay(
                f"Your task is too long. Please keep it under 500 characters.\n\n"
                f"**Current length:** {len(task)} characters"
            ))
            error_view.add_item(error_container)
            await ctx.send(view=error_view)
            return
            
        try:
            async with aiosqlite.connect(DATABASE_PATH) as db:
                await db.execute(
                    "INSERT INTO todos (userId, guildId, task) VALUES (?, ?, ?)",
                    (ctx.author.id, ctx.guild.id, task.strip())
                )
                await db.commit()
                
            success_view = ui.LayoutView()
            success_container = ui.Container(accent_color=None)
            success_container.add_item(ui.TextDisplay("✅ Your task has been added to your todo list."))
            success_view.add_item(success_container)
            await ctx.send(view=success_view)
        except Exception as e:
            logger.error(f"Todo add error: {e}")
            error_view = ui.LayoutView()
            error_container = ui.Container(accent_color=None)
            error_container.add_item(ui.TextDisplay("# Database Error"))
            error_container.add_item(ui.Separator())
            error_container.add_item(ui.TextDisplay(
                "Failed to add task to your todo list. Please try again later."
            ))
            error_view.add_item(error_container)
            await ctx.send(view=error_view)
            
    @todo.command(name="list")
    async def todo_list(self, ctx):
        try:
            async with aiosqlite.connect(DATABASE_PATH) as db:
                cursor = await db.execute(
                    "SELECT COUNT(*) FROM todos WHERE userId = ? AND guildId = ? AND completed = 0",
                    (ctx.author.id, ctx.guild.id)
                )
                result = await cursor.fetchone()
                total_todos = result[0] if result else 0
                
                if total_todos == 0:
                    empty_view = ui.LayoutView()
                    empty_container = ui.Container(accent_color=None)
                    empty_container.add_item(ui.TextDisplay("# Your Todo List"))
                    empty_container.add_item(ui.Separator())
                    empty_container.add_item(ui.TextDisplay("Your todo list is empty!"))
                    empty_view.add_item(empty_container)
                    await ctx.send(view=empty_view)
                    return
                    
                items_per_page = 6
                total_pages = (total_todos + items_per_page - 1) // items_per_page
                current_page = 0
                
                async def create_todo_list_view(page: int):
                    offset = page * items_per_page
                    async with aiosqlite.connect(DATABASE_PATH) as db:
                        cursor = await db.execute(
                            "SELECT id, task FROM todos WHERE userId = ? AND guildId = ? AND completed = 0 LIMIT ? OFFSET ?",
                            (ctx.author.id, ctx.guild.id, items_per_page, offset)
                        )
                        todos = await cursor.fetchall()
                        
                    layout_view = ui.LayoutView(timeout=300.0)
                    container = ui.Container(accent_color=None)
                    container.add_item(ui.TextDisplay("# Your Todo List"))
                    container.add_item(ui.Separator())
                    
                    if todos:
                        todo_text = ""
                        for todo_id, task in todos:
                            todo_text += f"<:dot:1479361908766281812>  {task} [{todo_id}]\n"
                        container.add_item(ui.TextDisplay(todo_text.strip()))
                        
                    if total_pages > 1:
                        container.add_item(ui.Separator())
                        button_row = ui.ActionRow(
                            ui.Button(
                                label="",
                                emoji="<:SageDoubleArrowLeft:1385846432535412758>",
                                custom_id="todo_home",
                                style=discord.ButtonStyle.secondary,
                                disabled=(page == 0)
                            ),
                            ui.Button(
                                label="",
                                emoji="<:arrow_left:1385846548625363117>",
                                custom_id="todo_back",
                                style=discord.ButtonStyle.secondary,
                                disabled=(page == 0)
                            ),
                            ui.Button(
                                label="",
                                emoji="<:arrow_right:1385846525204103252>",
                                custom_id="todo_next",
                                style=discord.ButtonStyle.secondary,
                                disabled=(page >= total_pages - 1)
                            ),
                            ui.Button(
                                label="",
                                emoji="<:SageDoubleArrowRight:1385846409902948362>",
                                custom_id="todo_last",
                                style=discord.ButtonStyle.secondary,
                                disabled=(page >= total_pages - 1)
                            )
                        )
                        container.add_item(button_row)
                        
                    layout_view.add_item(container)
                    return layout_view
                    
                initial_view = await create_todo_list_view(current_page)
                result_message = await ctx.send(view=initial_view)
                
                if total_pages > 1:
                    def check(interaction: discord.Interaction):
                        return (interaction.user.id == ctx.author.id and 
                                interaction.message and 
                                interaction.message.id == result_message.id)
                        
                    while True:
                        try:
                            interaction = await self.bot.wait_for('interaction', timeout=300.0, check=check)
                            
                            if interaction.data['custom_id'] == 'todo_home':
                                current_page = 0
                            elif interaction.data['custom_id'] == 'todo_back':
                                if current_page > 0:
                                    current_page -= 1
                            elif interaction.data['custom_id'] == 'todo_next':
                                if current_page < total_pages - 1:
                                    current_page += 1
                            elif interaction.data['custom_id'] == 'todo_last':
                                current_page = total_pages - 1
                                
                            updated_view = await create_todo_list_view(current_page)
                            await interaction.response.edit_message(view=updated_view)
                            
                        except Exception:
                            break
                            
        except Exception as e:
            logger.error(f"Todo list error: {e}")
            error_view = ui.LayoutView()
            error_container = ui.Container(accent_color=None)
            error_container.add_item(ui.TextDisplay("# Command Error"))
            error_container.add_item(ui.Separator())
            error_container.add_item(ui.TextDisplay(
                "An unexpected error occurred while processing your todo list. Please try again later."
            ))
            error_view.add_item(error_container)
            await ctx.send(view=error_view)
            
    @todo.command(name="remove", aliases=["delete", "rm"])
    async def todo_remove(self, ctx, todo_id: Optional[int] = None):
        if todo_id is None:
            error_view = ui.LayoutView()
            error_container = ui.Container(accent_color=None)
            error_container.add_item(ui.TextDisplay("# Missing Todo ID"))
            error_container.add_item(ui.Separator())
            error_container.add_item(ui.TextDisplay(
                "Please provide a todo ID to remove.\n\n"
                "**Usage:** `todo remove <id>`\n"
                "**Example:** `todo remove 5`\n\n"
                "Use `todo list` to see your available todos and their IDs."
            ))
            error_view.add_item(error_container)
            await ctx.send(view=error_view)
            return
            
        try:
            async with aiosqlite.connect(DATABASE_PATH) as db:
                cursor = await db.execute(
                    "SELECT id FROM todos WHERE id = ? AND userId = ? AND guildId = ?",
                    (todo_id, ctx.author.id, ctx.guild.id)
                )
                existing_todo = await cursor.fetchone()
                
                if not existing_todo:
                    error_view = ui.LayoutView()
                    error_container = ui.Container(accent_color=None)
                    error_container.add_item(ui.TextDisplay("# Todo Not Found"))
                    error_container.add_item(ui.Separator())
                    error_container.add_item(ui.TextDisplay(
                        f"Todo with ID **{todo_id}** was not found in your todo list.\n\n"
                        f"Use `todo list` to see your available todos and their IDs."
                    ))
                    error_view.add_item(error_container)
                    await ctx.send(view=error_view)
                    return
                    
                cursor = await db.execute(
                    "DELETE FROM todos WHERE id = ? AND userId = ? AND guildId = ?",
                    (todo_id, ctx.author.id, ctx.guild.id)
                )
                await db.commit()
                
                rowcount = cursor.rowcount or 0
                if rowcount > 0:
                    success_view = ui.LayoutView()
                    success_container = ui.Container(accent_color=None)
                    success_container.add_item(ui.TextDisplay("✅ Task successfully removed from your todo list."))
                    success_view.add_item(success_container)
                    await ctx.send(view=success_view)
                else:
                    error_view = ui.LayoutView()
                    error_container = ui.Container(accent_color=None)
                    error_container.add_item(ui.TextDisplay("# Remove Failed"))
                    error_container.add_item(ui.Separator())
                    error_container.add_item(ui.TextDisplay(
                        "Failed to remove the task. It may have already been deleted."
                    ))
                    error_view.add_item(error_container)
                    await ctx.send(view=error_view)
                    
        except Exception as e:
            logger.error(f"Todo remove error: {e}")
            error_view = ui.LayoutView()
            error_container = ui.Container(accent_color=None)
            error_container.add_item(ui.TextDisplay("# Database Error"))
            error_container.add_item(ui.Separator())
            error_container.add_item(ui.TextDisplay(
                "Failed to remove task from your todo list. Please try again later."
            ))
            error_view.add_item(error_container)
            await ctx.send(view=error_view)
            
    @todo.command(name="clear")
    async def todo_clear(self, ctx):
        try:
            async with aiosqlite.connect(DATABASE_PATH) as db:
                cursor = await db.execute(
                    "SELECT COUNT(*) FROM todos WHERE userId = ? AND guildId = ? AND completed = 0",
                    (ctx.author.id, ctx.guild.id)
                )
                result = await cursor.fetchone()
                total_todos = result[0] if result else 0
                
                if total_todos == 0:
                    error_view = ui.LayoutView()
                    error_container = ui.Container(accent_color=None)
                    error_container.add_item(ui.TextDisplay("# No Todos Found"))
                    error_container.add_item(ui.Separator())
                    error_container.add_item(ui.TextDisplay(
                        "Your todo list is already empty! There are no todos to clear."
                    ))
                    error_view.add_item(error_container)
                    await ctx.send(view=error_view)
                    return
                    
                cursor = await db.execute(
                    "DELETE FROM todos WHERE userId = ? AND guildId = ? AND completed = 0",
                    (ctx.author.id, ctx.guild.id)
                )
                await db.commit()
                
                rowcount = cursor.rowcount or 0
                if rowcount > 0:
                    success_view = ui.LayoutView()
                    success_container = ui.Container(accent_color=None)
                    todo_word = "todo" if rowcount == 1 else "todos"
                    success_container.add_item(ui.TextDisplay(
                        f"✅ Successfully cleared **{rowcount}** {todo_word} from your list."
                    ))
                    success_view.add_item(success_container)
                    await ctx.send(view=success_view)
                else:
                    error_view = ui.LayoutView()
                    error_container = ui.Container(accent_color=None)
                    error_container.add_item(ui.TextDisplay("# Clear Failed"))
                    error_container.add_item(ui.Separator())
                    error_container.add_item(ui.TextDisplay(
                        "Failed to clear todos. Your list may already be empty."
                    ))
                    error_view.add_item(error_container)
                    await ctx.send(view=error_view)
                    
        except Exception as e:
            logger.error(f"Todo clear error: {e}")
            error_view = ui.LayoutView()
            error_container = ui.Container(accent_color=None)
            error_container.add_item(ui.TextDisplay("# Database Error"))
            error_container.add_item(ui.Separator())
            error_container.add_item(ui.TextDisplay(
                "Failed to clear your todo list. Please try again later."
            ))
            error_view.add_item(error_container)
            await ctx.send(view=error_view)

async def setup(bot):
    await bot.add_cog(TodoList(bot))

"""
: ! Aegis !
    + Discord: itsfizys
    + Community: https://discord.gg/aerox (AeroX Development )
    + for any queries reach out Community or DM me.
"""
