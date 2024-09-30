# Maltriel D&D Discord Bot

A powerful Discord bot designed to facilitate Dungeons & Dragons gameplay for both Dungeon Masters and players. The bot manages player characters, rolls dice, checks passive stats, tracks equipment and modifiers, and more. It is highly customizable and easy to use after initial setup.

## Features
- Create and manage D&D characters
- Automated dice rolls for stats, skills, and saving throws
- Passive checks and modifiers management
- Level-based proficiency and automatic updates as characters level up
- Equipment tracking with optional descriptions, quantities, and modifiers (stats and skills)
- HP and Armor Class tracking with customizable equipment modifiers
- Saving throw management and automatic roll generation

## Commands

### Character Management
- **`!create_character [name] [class] [level] [stats]`**: Creates a new character.
- **`!update_character [name] [level/stat/skill/equipment] [new_value]`**: Updates an existing character with new values (for level-ups, stat changes, etc.).
- **`!add_equipment [character_name] [equipment_name] [optional: description] [optional: quantity]`**: Adds equipment to the character's inventory.
- **`!equip [character_name] [equipment_name]`**: Equips an item and applies any stat or skill modifiers.
- **`!unequip [character_name] [equipment_name]`**: Unequips an item and removes its modifiers.

### Rolling Dice
- **`!roll [dice]`**: Rolls a dice (e.g., `!roll d20`, `!roll 2d6`).
- **`!roll_stat [character_name] [stat]`**: Rolls for a character's stat (e.g., `!roll_stat John Strength`).
- **`!roll_skill [character_name] [skill]`**: Rolls for a character’s skill (e.g., `!roll_skill John Acrobatics`).
- **`!roll_save [character_name] [saving_throw]`**: Rolls a saving throw for a character (e.g., `!roll_save John Constitution`).

### HP and Armor Class Management
- **`!set_hp [character_name] [max_hp]`**: Sets the maximum HP for a character based on their class and Constitution modifier.
- **`!damage [character_name] [amount]`**: Deducts HP based on damage taken.
- **`!heal [character_name] [amount]`**: Heals HP based on amount healed.
- **`!set_ac [character_name] [armor_class]`**: Sets the Armor Class (AC) for the character. By default, AC is 10 without modifiers.

### Help and Info
- **`!help`**: Displays detailed instructions on how to use each command.

## How to Use

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/dnd-discord-bot.git
   ```
2. **Install dependencies**:
   Navigate to the bot directory and install the required Python libraries.
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your Discord bot**:
   - Create a new bot on the [Discord Developer Portal](https://discord.com/developers/applications).
   - Enable the necessary intents for the bot (privileged intents like member presence and message content).
   - Get the bot token and add it to your environment variables or a `.env` file.

4. **Run the bot**:
   ```bash
   python main.py
   ```

## Hosting

To keep the bot running 24/7, deploy it to a cloud service like:
- **Heroku**: [Heroku Deployment Guide](https://devcenter.heroku.com/articles/getting-started-with-python)
- **Replit**: [Replit Guide](https://replit.com)

Make sure to set your environment variables (e.g., `DISCORD_TOKEN`) in the hosting service’s settings.

## Contributing

Contributions are welcome! Feel free to submit a pull request or open an issue if you have suggestions or bug reports.

## License

This project is licensed under the GNL v3 License.
