import discord
from discord.ext import commands
import random


token = 'token filler'

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True  # Important for handling message content
intents.guilds = True  # Enable guild-related events

bot = commands.Bot(command_prefix="!", intents=intents)

def calculate_proficiency_bonus(level):
    if level >= 17:
        return 6
    elif level >= 13:
        return 5
    elif level >= 9:
        return 4
    elif level >= 5:
        return 3
    else:
        return 2

class_hit_dice = {
    "Artificer": 8,
    "Barbarian": 12,
    "Bard": 8,
    "Cleric": 8,
    "Druid": 8,
    "Fighter": 10,
    "Monk": 8,
    "Paladin": 10,
    "Ranger": 10,
    "Rogue": 8,
    "Sorcerer": 6,
    "Warlock": 8,
    "Wizard": 6
}

@bot.command()
async def command_help(ctx, page=1):
    help_message = ''

    if page == 1:
        help_message = """
**D&D Bot Command Guide:**

1. **!create_character <name> [level]**
   - Creates a new character with a given name and optional level (default is 1).
   - Example: `!create_character Cocyutis barbarian 3`

2. **!add_proficiency <name> <skill/stat> <full/half>**
    - Adds proficiency to a skill or stat. Specify if it’s full or half proficiency.
    - Example: `!add_proficiency Cocyutis acrobatics full`

3. **!add_equipment <name> <item> [description] [quantity] [modifier]**
    - Adds equipment to the character. You can optionally provide a description, quantity, and modifier.
    - Example: `!add_equipment Cocyutis Sword "A fine steel sword" 1 +2 strength`
        """
    elif page == 2:
        help_message = """
**D&D Bot Command Guide:**

4. **!equip_item <name> <item>**
    - Equips an item for the character and applies any relevant stat or skill modifiers.
    - Example: `!equip_item Cocyutis Sword`

5. **!unequip_item <name> <item>**
    - Unequips an item for the character and removes its stat or skill modifiers.
    - Example: `!unequip_item Cocyutis Sword`

6. **!roll <name> [stat/skill]**
    - Rolls a d20 for the character. You can optionally specify a stat (e.g., strength, dexterity) or a skill (e.g., acrobatics, arcana).
    - Rolls include proficiency bonuses and modifiers from equipped items.
    - Example: `!roll Cocyutis` or `!roll Cocyutis strength` or `!roll Cocyutis acrobatics`

7. **!saving_throw <name> <stat>**
    - Rolls a saving throw for the specified stat.
    - Example: `!saving_throw Cocyutis strength`
        """
    elif page == 3:
        help_message = """
**D&D Bot Command Guide:**

8. **!view_stats <name>**
    - Displays the character's current stats, including any active modifiers and proficiencies.
    - Example: `!view_stats Cocyutis`

9. **!view_equipment <name>**
    - Displays the character’s currently equipped items and inventory.
    - Example: `!view_equipment Cocyutis`

**Additional Notes:**
    - Proficiencies can be full or half, and will affect skill/stat rolls accordingly.
    - Equipment can include optional stat and skill modifiers, which will be applied when items are equipped.
        """

    await ctx.send(help_message)


# Roll a die, e.g., 1d20 or 2d6+3
@bot.command()
async def roll(ctx, name: str, stat_or_skill: str = None):
    character = characters.get(ctx.author.id)

    if not character:
        await ctx.send("No character found for you.")
        return

    if name != character['name']:
        await ctx.send(f"You don't have a character named {name}.")
        return

    if stat_or_skill:
        # Roll for a stat or skill
        if stat_or_skill in character['stats']:
            # Roll for a stat (e.g., strength, dexterity)
            stat_value = character['stats'][stat_or_skill]
            roll_result = random.randint(1, 20)
            total_result = roll_result + stat_value
            await ctx.send(f"{name} rolled for {stat_or_skill}: {roll_result} + {stat_value} = {total_result}")

        elif stat_or_skill in character['skills']:
            # Roll for a skill check (e.g., acrobatics, arcana)
            skill_info = character['skills'][stat_or_skill]
            proficiency = skill_info['proficiency']
            modifier = skill_info['modifier']

            # Calculate proficiency bonus based on level
            if proficiency == "full":
                proficiency_bonus = character["level"] // 4 + 2  # standard progression
            elif proficiency == "half":
                proficiency_bonus = (character["level"] // 4 + 2) // 2
            else:
                proficiency_bonus = 0

            total_modifier = proficiency_bonus + modifier

            # Roll the dice and calculate result
            roll_result = random.randint(1, 20)
            total_result = roll_result + total_modifier
            await ctx.send(f"Roll result for {stat_or_skill}: {roll_result} + {total_modifier} = {total_result}")
        else:
            await ctx.send(f"{name} doesn't have {stat_or_skill}.")
    else:
        # Regular d20 roll
        roll_result = random.randint(1, 20)
        await ctx.send(f"{name} rolled a {roll_result}.")


# Create a character and store basic information
characters = {}


@bot.command()
async def create_character(ctx, name: str, char_class: str, level: int = 1, constitution: int = 10):
    if ctx.author.id in characters:
        await ctx.send(f"You already have a character named {characters[ctx.author.id]['name']}.")
        return

    con_modifier = (constitution - 10) // 2

    # Calculate max HP: (One max roll on Hit Die) + ([Level] Rolls on Hit Die) + (Constitution Modifier × [Level])
    hit_die = class_hit_dice[char_class]
    max_hp = hit_die + (hit_die // 2 * level) + (con_modifier * level)

    # Default Armor Class (AC) is 10
    armor_class = 10

    # Create a new character with base attributes and empty skills, stats, and equipment
    characters[ctx.author.id] = {
        'name': name,
        'level': level,
        'max_hp': max_hp,
        'current_hp': max_hp,
        'armor_class': armor_class,
        'stats': {
            'strength': 10,
            'dexterity': 10,
            'constitution': constitution,
            'intelligence': 10,
            'wisdom': 10,
            'charisma': 10
        },
        'skills': {
            'acrobatics': {'proficiency': None, 'modifier': 0},
            'animal_handling': {'proficiency': None, 'modifier': 0},
            'arcana': {'proficiency': None, 'modifier': 0},
            'athletics': {'proficiency': None, 'modifier': 0},
            'deception': {'proficiency': None, 'modifier': 0},
            'history': {'proficiency': None, 'modifier': 0},
            'insight': {'proficiency': None, 'modifier': 0},
            'intimidation': {'proficiency': None, 'modifier': 0},
            'investigation': {'proficiency': None, 'modifier': 0},
            'medicine': {'proficiency': None, 'modifier': 0},
            'nature': {'proficiency': None, 'modifier': 0},
            'perception': {'proficiency': None, 'modifier': 0},
            'performance': {'proficiency': None, 'modifier': 0},
            'persuasion': {'proficiency': None, 'modifier': 0},
            'religion': {'proficiency': None, 'modifier': 0},
            'sleight_of_hand': {'proficiency': None, 'modifier': 0},
            'stealth': {'proficiency': None, 'modifier': 0},
            'survival': {'proficiency': None, 'modifier': 0}
        },
        'equipment': [],
        'equipped': [],
        'saving_throws': {}  # Saving throws can be customized separately for each stat
    }

    await ctx.send(f"Character {name} (Class: {char_class}, Level: {level}) created with {max_hp} HP and {armor_class} AC.")



@bot.command()
async def add_equipment(ctx, name: str, item_name: str, ac_mod: int = 0, quantity: int = 1, description: str = None, *modifiers):
    character = characters.get(ctx.author.id)

    if not character:
        await ctx.send("No character found for you.")
        return

    if name != character['name']:
        await ctx.send(f"You don't have a character named {name}.")
        return

    # Process modifiers (for both stats and skills)
    mod_dict = {}
    if modifiers:
        for mod in modifiers:
            # Each modifier should be provided in the format: "attribute:type:value"
            # Attributes can be stats (e.g., strength) or skills (e.g., acrobatics)
            attribute, mod_type, value = mod.split(":")
            mod_dict[attribute] = {"type": mod_type, "value": int(value)}

    # Create the equipment item
    item = {
        "name": item_name,
        "quantity": quantity,
        "description": description,
        'ac_mod': ac_mod,
        "modifiers": mod_dict if mod_dict else None
    }

    # Add the item to the character's equipment
    character['equipment'].append(item)

    response = f"{quantity}x {item_name} has been added to {name}'s equipment."
    if description:
        response += f" Description: {description}."
    if modifiers:
        response += f" Modifiers: {', '.join(modifiers)}."

    await ctx.send(response)


@bot.command()
async def remove_equipment(ctx, name: str, item_name: str):
    character = characters.get(ctx.author.id)

    if not character:
        await ctx.send("No character found for you.")
        return

    if name != character['name']:
        await ctx.send(f"You don't have a character named {name}.")
        return

    for item in character['equipment']:
        if item["name"].lower() == item_name.lower():
            character['equipment'].remove(item)
            await ctx.send(f"{item_name} removed from {name}'s equipment.")
            return

    await ctx.send(f"{name} doesn't have {item_name} in their equipment.")


@bot.command()
async def damage(ctx, name: str, damage_amount: int):
    if name in characters:
        characters[name]['current_hp'] -= damage_amount
        if characters[name]['current_hp'] < 0:
            characters[name]['current_hp'] = 0
        await ctx.send(f"{name} takes {damage_amount} damage. Current HP: {characters[name]['current_hp']}/{characters[name]['max_hp']}")
    else:
        await ctx.send(f"Character {name} not found.")

@bot.command()
async def heal(ctx, name: str, heal_amount: int):
    if name in characters:
        characters[name]['current_hp'] += heal_amount
        if characters[name]['current_hp'] > characters[name]['max_hp']:
            characters[name]['current_hp'] = characters[name]['max_hp']
        await ctx.send(f"{name} heals {heal_amount}. Current HP: {characters[name]['current_hp']}/{characters[name]['max_hp']}")
    else:
        await ctx.send(f"Character {name} not found.")


# Display character info
@bot.command()
async def character(ctx):
    character = characters.get(ctx.author.id)
    if character:
        await ctx.send(f"{character['name']} ({character['class']}) - Stats: {character['stats']}")
    else:
        await ctx.send("No character found for you.")

@bot.command()
async def passive(ctx):
    character = characters.get(ctx.author.id)
    if character:
        wisdom_mod = (character['stats']['wisdom'] - 10) // 2
        passive_perception = 10 + wisdom_mod
        await ctx.send(f"{character['name']}'s Passive Perception: {passive_perception}")
    else:
        await ctx.send("No character found for you.")

@bot.command()
@commands.is_owner()  # Only the DM (bot owner) can use this command
async def dm_roll(ctx, dice: str):
    try:
        rolls, modifier = dice.split('+') if '+' in dice else (dice, 0)
        number, die = rolls.split('d')
        rolls = [random.randint(1, int(die)) for _ in range(int(number))]
        total = sum(rolls) + int(modifier)
        await ctx.author.send(f"DM rolled {rolls} + {modifier} = {total}")  # Send result privately to DM
    except Exception as e:
        await ctx.send(f"Error: {str(e)}")


@bot.command()
async def saving_throw(ctx, name: str, stat: str):
    character = characters.get(ctx.author.id)

    if not character:
        await ctx.send("No character found for you.")
        return

    if name != character['name']:
        await ctx.send(f"You don't have a character named {name}.")
        return

    if stat not in character['stats']:
        await ctx.send(f"{name} doesn't have the stat {stat}.")
        return

    # Check if the character has a saving throw modifier for the stat
    saving_throw_modifier = character.get('saving_throws', {}).get(stat, character['stats'][stat])

    # Roll the dice and add the modifier
    roll_result = random.randint(1, 20)
    total_result = roll_result + saving_throw_modifier
    await ctx.send(f"Saving throw result for {stat}: {roll_result} + {saving_throw_modifier} = {total_result}")



@bot.command()
async def update_character(ctx, name: str, level: int = None):
    character = characters.get(ctx.author.id)

    if not character:
        await ctx.send("No character found for you.")
        return

    if name != character['name']:
        await ctx.send(f"You don't have a character named {name}.")
        return

    if level:
        character['level'] = level
        character['proficiency_bonus'] = calculate_proficiency_bonus(level)
        await ctx.send(
            f"{name} leveled up to level {level}. Proficiency bonus updated to {character['proficiency_bonus']}.")


@bot.command()
async def update_stat(ctx, name: str, stat: str, value: int):
    character = characters.get(ctx.author.id)

    if not character:
        await ctx.send("No character found for you.")
        return

    if name != character['name']:
        await ctx.send(f"You don't have a character named {name}.")
        return

    stat = stat.lower()
    if stat not in character['stats']:
        await ctx.send(
            f"{stat.capitalize()} is not a valid stat. Choose from: strength, dexterity, constitution, intelligence, wisdom, charisma.")
        return

    character['stats'][stat] = value
    await ctx.send(f"{character['name']}'s {stat.capitalize()} updated to {value}.")


@bot.command()
async def equip_item(ctx, name: str, item_name: str):
    character = characters.get(ctx.author.id)

    if not character:
        await ctx.send("No character found for you.")
        return

    if name != character['name']:
        await ctx.send(f"You don't have a character named {name}.")
        return

    # Check if the item exists in the equipment list
    for item in character['equipment']:
        if item['name'].lower() == item_name.lower():
            # Move item from equipment to equipped
            character['equipment'].remove(item)
            character['equipped'].append(item)

            characters[name]['armor_class'] += item['ac_mod']

            # Apply item modifiers, if any (to both stats and skills)
            if 'modifiers' in item:
                for attribute, modifier in item['modifiers'].items():
                    # Check if it's a stat or skill
                    if attribute in character['stats']:
                        # Apply stat modifiers
                        if modifier['type'] == "bonus":
                            character['stats'][attribute] += modifier['value']
                        elif modifier['type'] == "detriment":
                            character['stats'][attribute] -= modifier['value']
                    elif attribute in character['skills']:
                        # Apply skill modifiers
                        character['skills'][attribute]['modifier'] += modifier['value']

            await ctx.send(f"{item_name} has been equipped by {name}.")
            return

    await ctx.send(f"{name} doesn't have {item_name} in their inventory.")

@bot.command()
async def add_proficiency(ctx, name: str, skill_name: str, proficiency_type: str):
    character = characters.get(ctx.author.id)

    if not character:
        await ctx.send("No character found for you.")
        return

    if name != character['name']:
        await ctx.send(f"You don't have a character named {name}.")
        return

    if skill_name not in character['skills']:
        await ctx.send(f"{name} doesn't have a skill called {skill_name}.")
        return

    if proficiency_type not in ["full", "half"]:
        await ctx.send("Proficiency type must be either 'full' or 'half'.")
        return

    character['skills'][skill_name]['proficiency'] = proficiency_type
    await ctx.send(f"{name} now has {proficiency_type} proficiency in {skill_name}.")


@bot.command()
async def unequip_item(ctx, name: str, item_name: str):
    character = characters.get(ctx.author.id)

    if not character:
        await ctx.send("No character found for you.")
        return

    if name != character['name']:
        await ctx.send(f"You don't have a character named {name}.")
        return

    # Check if the item exists in the equipped list
    for item in character['equipped']:
        if item['name'].lower() == item_name.lower():
            # Remove item from equipped and put it back in equipment
            character['equipped'].remove(item)
            character['equipment'].append(item)

            # Revert AC modifiers
            characters[name]['armor_class'] -= item['ac_mod']

            # Reverse item modifiers, if any (for both stats and skills)
            if 'modifiers' in item:
                for attribute, modifier in item['modifiers'].items():
                    # Check if it's a stat or skill
                    if attribute in character['stats']:
                        # Reverse stat modifiers
                        if modifier['type'] == "bonus":
                            character['stats'][attribute] -= modifier['value']
                        elif modifier['type'] == "detriment":
                            character['stats'][attribute] += modifier['value']
                    elif attribute in character['skills']:
                        # Reverse skill modifiers
                        character['skills'][attribute]['modifier'] -= modifier['value']

            await ctx.send(f"{item_name} has been unequipped by {name}.")
            return

    await ctx.send(f"{name} doesn't have {item_name} equipped.")


@bot.command()
async def list_equipment(ctx, name: str):
    character = characters.get(ctx.author.id)

    if not character:
        await ctx.send("No character found for you.")
        return

    if name != character['name']:
        await ctx.send(f"You don't have a character named {name}.")
        return

    # Display equipped items
    if character['equipped']:
        equipped_response = f"{name}'s equipped items:\n"
        for item in character['equipped']:
            description = f" - {item['description']}" if item["description"] else ""
            equipped_response += f"{item['name']} (x{item['quantity']}){description}\n"
        await ctx.send(equipped_response)
    else:
        await ctx.send(f"{name} has no items equipped.")

    # Display unequipped items
    if character['equipment']:
        equipment_response = f"\n{name}'s inventory:\n"
        for item in character['equipment']:
            description = f" - {item['description']}" if item["description"] else ""
            equipment_response += f"{item['name']} (x{item['quantity']}){description}\n"
        await ctx.send(equipment_response)
    else:
        await ctx.send(f"{name} has no items in their inventory.")


bot.run(token)