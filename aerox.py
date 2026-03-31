"""
: ! Aegis !
    + Discord: itsfizys
    + Community: https://discord.gg/aerox (AeroX Development )
    + for any queries reach out Community or DM me.
"""
import os 
import sys 
import asyncio 
import traceback 
import signal 
from threading import Thread 
from datetime import datetime ,timezone ,timedelta 
import base64,sys,os; (lambda c: (print(base64.b64decode(b'ChtbOTFtICDilIzilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilJAbWzBtChtbOTFtICDilIIgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICDilIIbWzBtChtbOTFtICDilIIgICAbWzFtJjIwICBDT1JFIElOVEVHUklUWSBDSEVDSyBGQUlMRUQgICAgICAgICAgICAgICAg4pSCG1swbQobWzkxbSAg4pSCICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAg4pSCG1swbQobWzkxbSAg4pSCICAgG1s5N21Cb3QgY3JlZGl0cyBoYXZlIGJlZW4gdGFtcGVyZWQgd2l0aC4bWzkxbSAgICAgICAgICAgIOKUghtbMG0KG1s5MW0gIOKUgiAgIBtbOTdtUmVzdG9yZSBvcmlnaW5hbCBhdXRob3IgY3JlZGl0cyB0byBzdGFydCB0aGUgYm90LhtbOTFtIOKUghtbMG0KG1s5MW0gIOKUgiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIOKUghtbMG0KG1s5MW0gIOKUlOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUmBtbMG0K').decode()), sys.exit(1)) if not (c.count(base64.b64decode(b'ISBBZWdpcyAh').decode()) >= 2 and c.count(base64.b64decode(b'RGlzY29yZDogaXRzZml6eXM=').decode()) >= 2 and base64.b64decode(b'QWVyb1ggRGV2ZWxvcG1lbnQ=').decode() in c and base64.b64decode(b'aHR0cHM6Ly9kaXNjb3JkLmdnL2Flcm94').decode() in c) else None)(open(__file__, 'r', encoding='utf-8').read()) if os.path.exists(__file__) else None


if sys .version_info <(3 ,11 ):
    import typing 
    if not hasattr (typing ,'Self'):
        try :
            from typing_extensions import Self 
            typing .Self =Self 
        except ImportError :

            typing .Self =type ('Self',(),{})

import aiohttp 
import discord 
from discord .ext import commands 
from core import Context 
from core .Yuna import Yuna 
from utils .Tools import *
from utils .config import *
from utils .logger import logger
import jishaku 
import cogs 




async def load_reactionrole ():
    await bot .add_cog (cogs .ReactionRole (bot ))
import aiosqlite 
import logging 
from dotenv import load_dotenv 


def print_startup_banner ():
    """Print the AeroX startup banner"""
    banner = [
        "AeroX Multipurpose Bot",
        "──────────────────────────────────────",
        "System: Operational",
        "Developer: itsfizys (AeroX Development)",
        "Community: https://discord.gg/aerox",
        "──────────────────────────────────────"
    ]
    for line in banner:
        logger.info("CORE", line)

def print_system_ready ():
    """Print the final system ready message"""
    logger.success("SYSTEM", "AeroX is now online and ready to serve!")




load_dotenv ()
_log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
os.makedirs(_log_dir, exist_ok=True)

logging .basicConfig (
level =logging .ERROR ,
format ='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
handlers =[
    logging .FileHandler (os.path.join(_log_dir, 'discord.log'))
]
)


logging .getLogger ('discord').setLevel (logging .ERROR )
logging .getLogger ('discord.http').setLevel (logging .ERROR )
logging .getLogger ('discord.gateway').setLevel (logging .ERROR )
logging .getLogger ('discord.client').setLevel (logging .ERROR )


class DatabaseTestFilter (logging .Filter ):
    def filter (self ,record ):
        message =record .getMessage ().lower ()

        if 'database connection test successful'in message :
            return False 
        return True 


for logger_name in ['discord','discord.http','discord.gateway','discord.client']:
    std_logger =logging .getLogger (logger_name )
    std_logger .propagate = True
    std_logger .handlers = [] # Clear any existing handlers
    std_logger .addFilter (DatabaseTestFilter ())


logging .getLogger ().addFilter (DatabaseTestFilter ())



os .environ ["JISHAKU_NO_DM_TRACEBACK"]="False"
os .environ ["JISHAKU_HIDE"]="True"
os .environ ["JISHAKU_NO_UNDERSCORE"]="True"
os .environ ["JISHAKU_FORCE_PAGINATOR"]="True"


def utc_to_ist (dt ):
    ist_offset =timedelta (hours =5 ,minutes =30 )
    return dt .replace (tzinfo =timezone .utc ).astimezone (timezone (ist_offset ))

class TicketBot (Yuna ):
    def __init__ (self ):
        super ().__init__ ()
        self .db =None 

    async def setup_hook (self ):
        print_startup_banner ()
        logger.info("INIT", "Initializing database connection")
        try :
            self .db =await aiosqlite .connect ("db/bot_database.db")
            if self .db is None :
                raise Exception ("Failed to connect to database")

            logger.success("DB", "Database connection established")
            
            from utils.Tools import updateAllGuildsPrefixFromEnv
            await updateAllGuildsPrefixFromEnv()
            
            logger.success("DB", "Database schema initialized")


            await self .db .execute ("""
                CREATE TABLE IF NOT EXISTS tickets (
                    guild_id INTEGER PRIMARY KEY,
                    channel_id INTEGER,
                    role_id INTEGER,
                    category_id INTEGER,
                    log_channel_id INTEGER,
                    ping_role_id INTEGER,
                    embed_title TEXT DEFAULT 'Create a Ticket',
                    embed_description TEXT DEFAULT 'Need assistance? Select a category below to create a ticket, and our support team will assist you shortly! 📩',
                    embed_footer TEXT DEFAULT 'Powered by AeroX Development',
                    embed_image_url TEXT,
                    embed_color INTEGER DEFAULT 16711680,
                    panel_type TEXT DEFAULT 'dropdown'
                )
            """)


            async with self .db .cursor ()as cur :
                await cur .execute ("PRAGMA table_info(tickets)")
                columns =[col [1 ]for col in await cur .fetchall ()]
                if "panel_type"not in columns :
                    await cur .execute ("ALTER TABLE tickets ADD COLUMN panel_type TEXT DEFAULT 'dropdown'")
                if "ping_role_id"not in columns :
                    await cur .execute ("ALTER TABLE tickets ADD COLUMN ping_role_id INTEGER")
                if "embed_color"in columns :
                    await cur .execute ("PRAGMA table_info(tickets)")
                    col_info =[col for col in await cur .fetchall ()if col [1 ]=="embed_color"]
                    if col_info and col_info [0 ][2 ]=="TEXT":
                        await cur .execute ("ALTER TABLE tickets RENAME TO old_tickets")
                        await self .db .execute ("""
                            CREATE TABLE tickets (
                                guild_id INTEGER PRIMARY KEY,
                                channel_id INTEGER,
                                role_id INTEGER,
                                category_id INTEGER,
                                log_channel_id INTEGER,
                                ping_role_id INTEGER,
                                embed_title TEXT DEFAULT 'Create a Ticket',
                                embed_description TEXT DEFAULT 'Need assistance? Select a category below to create a ticket, and our support team will assist you shortly! 📩',
                                embed_footer TEXT DEFAULT 'Powered by AeroX Development',
                                embed_image_url TEXT,
                                embed_color INTEGER DEFAULT 16711680,
                                panel_type TEXT DEFAULT 'dropdown'
                            )
                        """)
                        await cur .execute ("""
                            INSERT INTO tickets (
                                guild_id, channel_id, role_id, category_id, log_channel_id, ping_role_id,
                                embed_title, embed_description, embed_footer, embed_image_url, embed_color, panel_type
                            )
                            SELECT guild_id, channel_id, role_id, category_id, log_channel_id, ping_role_id,
                                   embed_title, embed_description, embed_footer, embed_image_url,
                                   CAST(embed_color AS INTEGER), panel_type
                            FROM old_tickets
                        """)
                        await cur .execute ("DROP TABLE old_tickets")
                        await self .db .commit ()


            await self .db .execute ("""
                CREATE TABLE IF NOT EXISTS ticket_categories (
                    guild_id INTEGER,
                    category_name TEXT,
                    PRIMARY KEY (guild_id, category_name)
                )
            """)


            await self .db .execute ("""
                CREATE TABLE IF NOT EXISTS ticket_panels (
                    guild_id INTEGER,
                    channel_id INTEGER,
                    message_id INTEGER,
                    PRIMARY KEY (guild_id, message_id)
                )
            """)


            await self .db .execute ("""
                CREATE TABLE IF NOT EXISTS guild_blacklist (
                    guild_id INTEGER PRIMARY KEY,
                    reason TEXT,
                    blacklisted_at TEXT
                )
            """)

            await self .db .execute ("""
                CREATE TABLE IF NOT EXISTS user_blacklist (
                    user_id INTEGER PRIMARY KEY,
                    reason TEXT,
                    blacklisted_at TEXT
                )
            """)

            await self .db .commit ()
            logger.success("DB", "Database schema initialized")
        except Exception as e :
            logger.error("DB", f"Database setup failed: {e}")
            raise 

        logger.info("INIT", "Loading core modules")
        try :
            await self .load_extension ("jishaku")
            logger.success("INIT", "Core utilities loaded")
            await self .load_extension ("cogs")
            logger.success("INIT", "Command modules loaded")
            logger.info("INIT", "All modules loaded successfully")
        except Exception as e :
            logger.error("INIT", f"Failed to load extensions: {e}")
            raise 

        logger.info("INIT", "Synchronizing command tree")
        try :
            synced =await self .tree .sync ()
            logger.success("INIT", f"Command synchronization complete ({len(synced)} commands)")
        except Exception as e :
            logger.error("INIT", f"Failed to sync commands: {e}")
            raise

        logger.info("INIT", "Setting up component interactions")
        try:
            
            self.setup_component_interactions()
            logger.success("INIT", "Component interaction handlers configured")
        except Exception as e:
            logger.error("INIT", f"Failed to setup component interactions: {e}")

    def setup_component_interactions(self):
        """Setup component interaction handlers for Components v2"""
        pass 

    async def close (self ):
        try :
            if hasattr (self ,'status_rotation'):
                self .status_rotation .cancel ()

            if self .db :
                await self .db .close ()
                logger.info("DB", "Database connection gracefully closed")

            import gc 
            for obj in gc .get_objects ():
                try:
                    if hasattr (obj ,'close')and 'aiosqlite'in str (type (obj )):
                        try :
                            await obj .close ()
                        except :
                            pass 
                except:
                    pass

        except Exception as e :
            logger.error("SHUTDOWN", f"Failed to close resources: {e}")
        finally :
            await super ().close ()

client =TicketBot ()
tree =client .tree 


@client .event 
async def on_ready ():
    await client .wait_until_ready ()

    logger.success("READY", f"Logged in as {client.user.name}")



    print_system_ready ()

@client .event 
async def on_interaction (interaction :discord .Interaction ):
    if interaction .type !=discord .InteractionType .component :
        return 
    try :
        custom_id =interaction .data .get ("custom_id")
        if not custom_id :
            logger.error("INTERACTION", f"Received interaction without custom_id from user {interaction.user.id}")
            logger .warn ("Received interaction without custom_id")
            return 


        
        if custom_id.startswith("giveaway_"):
            from cogs.commands.giveaway import giveaway_button_callback
            giveaway_id = int(custom_id.split("_")[1])
            await giveaway_button_callback(interaction, giveaway_id)
            return

        if hasattr(interaction.message, 'view') and interaction.message.view:
            view = interaction.message.view
            if hasattr(view, 'interaction_handler'):
                await view.interaction_handler(interaction)
                return

        if custom_id in ["ban_user", "unban_user", "delete_message", "confirm_unbanall", "cancel_unbanall"]:
            from cogs.moderation.ban import BanLayoutView
            from cogs.moderation.unban import UnbanLayoutView
            from cogs.moderation.unbanall import UnbanAllView
            
            message = interaction.message
            if message and hasattr(message, 'components'):
                logger.debug("INTERACTION", f"Handling {custom_id} interaction")
                
                if not interaction.response.is_done():
                    await interaction.response.defer()
            return

    except Exception as e :
        logger.error("INTERACTION", f"Critical error in interaction handler: {str(e)}")
        logger.error("INTERACTION", f"User: {interaction.user.id}, Guild: {interaction.guild.id if interaction.guild else 'None'}")
        logger.error("INTERACTION", f"Custom ID: {custom_id if 'custom_id' in locals() else 'Unknown'}")
        logger.debug("INTERACTION", f"Traceback: {traceback.format_exc()}")
        logger .error (f"Interaction failed: {str(e)}")
        try :
            if not interaction .response .is_done ():
                await interaction .response .send_message ("An error occurred while handling this interaction.",ephemeral =True )
        except Exception as followup_error :
            logger.error("INTERACTION", f"Failed to send error message: {followup_error}")

@client .event 
async def on_command_completion (context :commands .Context )->None :
    full_command_name =context .command .qualified_name 
    split =full_command_name .split ("\n")
    executed_command =str (split [0 ])
    webhook_url =WEBHOOK_URL 
    
    if context .guild is not None :
        try :
            async with aiohttp .ClientSession ()as session :
                webhook =discord .Webhook .from_url (webhook_url ,session =session )
                
                avatar_url =context .author .avatar .url if context .author .avatar else context .author .default_avatar .url 
                current_time =utc_to_ist (discord .utils .utcnow ())
                
                container =discord .ui .Container (accent_color =None )
                
                container .add_item (
                    discord .ui .TextDisplay (f"# Command Executed: {executed_command}")
                )
                
                container .add_item (discord .ui .Separator ())
                
                command_details =f"<:arrow:1479361920254345391> **Command Name:** {executed_command}\n<:arrow:1479361920254345391> **Guild Name:** {context.guild.name} ({context.guild.id})\n<:arrow:1479361920254345391> **Channel Name:** {context.channel.name} ({context.channel.id})\n<:arrow:1479361920254345391> **User:** [{context.author}](https://discord.com/users/{context.author.id}) ({context.author.id})"
                
                container .add_item (
                    discord .ui .Section (
                        discord .ui .TextDisplay (command_details ),
                        accessory =discord .ui .Thumbnail (avatar_url )
                    )
                )
                
                container .add_item (discord .ui .Separator ())
                
                container .add_item (
                    discord .ui .TextDisplay (f"**Command Executed at {current_time.strftime('%I:%M %p IST')}**")
                )
                
                view =discord .ui .LayoutView ()
                view .add_item (container )
                
                await webhook .send (view =view )
        except Exception as e :
            pass  





TOKEN =os .getenv ("TOKEN")
WEBHOOK_URL =os .getenv ("WEBHOOK_URL")
PREFIX =os .getenv ("BOT_PREFIX")

if TOKEN is None :
    logger .error ("TOKEN environment variable not set in .env file. Please ensure your .env file contains the TOKEN.")
    raise ValueError ("TOKEN environment variable not set in .env file. Cannot start the bot.")

if WEBHOOK_URL is None :
    logger .error ("WEBHOOK_URL environment variable not set in .env file. Please ensure your .env file contains the WEBHOOK_URL.")
    raise ValueError ("WEBHOOK_URL environment variable not set in .env file.")

if PREFIX is None :
    logger .error ("PREFIX environment variable not set in .env file. Please ensure your .env file contains the PREFIX.")
    raise ValueError ("PREFIX environment variable not set in .env file.")

async def run_bot ():
    """Run the bot with graceful shutdown handling"""
    try:
        logger.info("INIT", "Establishing connection to Discord")
        await client.start(TOKEN)
    except discord.LoginFailure:
        logger.error("INIT", "Authentication failed - Invalid token configuration")
    except KeyboardInterrupt:
        logger.info("INIT", "Keyboard interrupt received, shutting down...")
    except Exception as e:
        logger.error("INIT", f"Startup failed: {e}")
    finally:
        if not client.is_closed():
            logger.info("INIT", "Shutdown signal received, stopping bot gracefully...")
            await client.close()
        logger.success("INIT", "Bot shutdown completed gracefully")

if __name__ =='__main__':
    try :
        asyncio .run (run_bot ())
    except KeyboardInterrupt:
        logger.info("INIT", "Received keyboard interrupt, shutdown complete.")
    except Exception as e :
        logger.error ("INIT", f"Critical error: {e}")
        sys .exit (1 )
"""
: ! Aegis !
    + Discord: itsfizys
    + Community: https://discord.gg/aerox (AeroX Development )
    + for any queries reach out Community or DM me.
"""
