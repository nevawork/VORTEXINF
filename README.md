<div align="center">

# 🤖 VORTEX|INF Discord Bot — Component V2

*A premium multipurpose Discord bot featuring high-end Antinuke, Automod, and next-gen UI.*

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Discord.py](https://img.shields.io/badge/discord.py-2.0+-green.svg)
![License](https://img.shields.io/badge/License-Proprietary-red.svg)

</div>

---

## ✨ What is VORTEX|INF?

**VORTEX|INF** is a state-of-the-art multipurpose Discord bot designed for performance and security. Powered by the **Component V2** architecture, VORTEX|INF delivers a premium user experience with sleek layouts and advanced functionality.

**Current Stats:**
- 🛠️ **99 Cogs** loaded with specialized logic.
- ⚡ **79 Commands** synchronized and ready for action.
- 🎨 **Component V2 UI**: Modern, interactive layouts using high-end Discord UI components.

## 🛡️ Key Features

- **Advanced Antinuke**: Protect your server from malicious actions (Channel/Role creation/deletion, kicks, bans, etc.).
- **Powerful Automod**: Keep your community safe with advanced filters for caps, links, invites, and spam.
- **Robust Moderation**: A full suite of moderation tools including ban, kick, warn, mute, and more.
- **Utility & Fun**: Feature-rich utility commands (Avatar, Userinfo, Membercount) and engaging fun features.
- **Auto-Initializing**: Seamless setup with automatic database and configuration generation.

## Quick Setup

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure your bot**
   - Create a `.env` file in the root directory.
   - Add your Discord bot token: `TOKEN=your_token_here`

3. **Owner Identification**
   - Edit `utils/config.py` to add your ID to `OWNER_IDS` for access to no-prefix and owner-only commands.

4. **Run the bot**
   ```bash
   python main.py
   ```

## ⚙️ Configuration Guide

### ⚡ Bot Prefix 
Edit `BOT_PREFIX` in your `.env` file and restart the bot:
```env
BOT_PREFIX=!
```

### 📁 File Organization
- **Database files (.db)**: Automatically generated and located in the `db/` folder.
- **JSON Data**: Configuration and persistence data in `jsondb/`.

---

## 🏆 Credits

<div align="center">

### 👨‍💻 Development Team

**Developer:** NEVA 3pa8
**Discord:** Watch https://discord.gg/98qaRWnKuH

---

**Made with ❤️ by NEVA 3pa8**

*Powered by Python & Discord.py • Component V2 Interface*

</div>