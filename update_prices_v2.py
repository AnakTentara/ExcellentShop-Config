"""
NaturalSMP Economy Overhaul v2 - Fixed DYNAMIC format
Correct format: BUY/SELL (uppercase), StartValue (not Start)
"""
import re
import os

SHOP_DIR = os.path.dirname(os.path.abspath(__file__))
SHOPS_DIR = os.path.join(SHOP_DIR, "virtual_shop", "shops")

# ============================================================================
# CORRECT DYNAMIC PRICING TEMPLATE (from in-game editor)
# ============================================================================
def dynamic_block(buy_start, sell_start, buy_off=1.0, sell_off=-1.0, min_off=-10.0, max_off=15.0, stab_interval=300, stab_amount=0.5):
    return (
        f"      Type: DYNAMIC\n"
        f"      BUY:\n"
        f"        StartValue: {buy_start}\n"
        f"        BuyOffset: {buy_off}\n"
        f"        SellOffset: {sell_off}\n"
        f"        MinOffset: {min_off}\n"
        f"        MaxOffset: {max_off}\n"
        f"      SELL:\n"
        f"        StartValue: {sell_start}\n"
        f"        BuyOffset: {buy_off}\n"
        f"        SellOffset: {sell_off}\n"
        f"        MinOffset: {min_off}\n"
        f"        MaxOffset: {max_off}\n"
        f"      Stabilization:\n"
        f"        Interval: {stab_interval}\n"
        f"        Amount: {stab_amount}"
    )

def flat_block(buy, sell):
    return (
        f"      Type: FLAT\n"
        f"      BUY: {buy}\n"
        f"      SELL: {sell}"
    )

# ============================================================================
# PRICING DEFINITIONS PER FILE
# ============================================================================

MINERALS_PRICES = {
    # Ores (Dynamic)
    'diamond_ore':           ('DYNAMIC', 2500.0, 500.0),
    'emerald_ore':           ('DYNAMIC', 3000.0, 600.0),
    'gold_ore':              ('DYNAMIC', 800.0, 160.0),
    'iron_ore':              ('DYNAMIC', 500.0, 100.0),
    'lapis_ore':             ('DYNAMIC', 400.0, 80.0),
    'redstone_ore':          ('DYNAMIC', 350.0, 70.0),
    'coal_ore':              ('DYNAMIC', 300.0, 60.0),
    # Deepslate Ores (Flat, +20% premium)
    'deepslate_diamond_ore': ('FLAT', 3000.0, 600.0),
    'deepslate_emerald_ore': ('FLAT', 3500.0, 700.0),
    'deepslate_gold_ore':    ('FLAT', 950.0, 190.0),
    'deepslate_iron_ore':    ('FLAT', 600.0, 120.0),
    'deepslate_lapis_ore':   ('FLAT', 500.0, 100.0),
    'deepslate_redstone_ore':('FLAT', 400.0, 80.0),
    'deepslate_coal_ore':    ('FLAT', 350.0, 70.0),
    'deepslate_copper_ore':  ('FLAT', 300.0, 60.0),
    # Nether Ores
    'nether_quartz_ore':     ('FLAT', 400.0, 80.0),
    'nether_gold_ore':       ('FLAT', 350.0, 70.0),
    # Ingots/Processed (Dynamic)
    'diamond':               ('DYNAMIC', 5000.0, 1000.0),
    'emerald':               ('DYNAMIC', 1500.0, 300.0),
    'gold_ingot':            ('DYNAMIC', 900.0, 180.0),
    'iron_ingot':            ('DYNAMIC', 500.0, 100.0),
    'copper_ingot':          ('DYNAMIC', 300.0, 60.0),
    'raw_iron':              ('DYNAMIC', 400.0, 80.0),
    'raw_gold':              ('DYNAMIC', 650.0, 130.0),
    'raw_copper':            ('DYNAMIC', 200.0, 40.0),
    'ancient_debris':        ('DYNAMIC', 8000.0, 1600.0),
    'netherite_scrap':       ('DYNAMIC', 10000.0, 2000.0),
    'netherite_ingot':       ('DYNAMIC', 15000.0, 3000.0),
    # Flat processed
    'lapis_lazuli':          ('FLAT', 350.0, 70.0),
    'redstone':              ('FLAT', 250.0, 50.0),
    'coal':                  ('FLAT', 250.0, 50.0),
    'quartz':                ('FLAT', 350.0, 70.0),
    'charcoal':              ('FLAT', 200.0, 40.0),
    # Nuggets
    'iron_nugget':           ('FLAT', 60.0, 12.0),
    'gold_nugget':           ('FLAT', 100.0, 20.0),
    # Blocks
    'diamond_block':         ('FLAT', 42000.0, 8400.0),
    'emerald_block':         ('FLAT', 12000.0, 2400.0),
    'gold_block':            ('FLAT', 7500.0, 1500.0),
    'iron_block':            ('FLAT', 4000.0, 800.0),
    'lapis_block':           ('FLAT', 3000.0, 600.0),
    'redstone_block':        ('FLAT', 2000.0, 400.0),
    'coal_block':            ('FLAT', 2000.0, 400.0),
    'quartz_block':          ('FLAT', 1200.0, 240.0),
    'copper_block':          ('FLAT', 2500.0, 500.0),
    'netherite_block':       ('FLAT', -1.0, -1.0),
    'raw_iron_block':        ('FLAT', 3200.0, 640.0),
    'raw_copper_block':      ('FLAT', 1600.0, 320.0),
    'raw_gold_block':        ('FLAT', 5500.0, 1100.0),
    # Copper ore flat
    'copper_ore':            ('FLAT', 300.0, 60.0),
}

FARMING_PRICES = {
    'wheat_seeds':           ('FLAT', 200.0, 5.0),
    'pumpkin_seeds':         ('FLAT', 200.0, 5.0),
    'melon_seeds':           ('FLAT', 200.0, 5.0),
    'beetroot_seeds':        ('FLAT', 200.0, 5.0),
    'wheat':                 ('DYNAMIC', 250.0, 50.0),
    'carrot':                ('DYNAMIC', 250.0, 50.0),
    'potato':                ('DYNAMIC', 250.0, 50.0),
    'sugar_cane':            ('DYNAMIC', 200.0, 40.0),
    'cocoa_beans':           ('FLAT', 300.0, 60.0),
    'pumpkin':               ('FLAT', 400.0, 80.0),
    'melon':                 ('FLAT', 350.0, 70.0),
    'melon_slice':           ('FLAT', 200.0, 25.0),
    'cactus':                ('FLAT', 300.0, 60.0),
    'nether_wart':           ('FLAT', 500.0, 100.0),
    'beetroot':              ('FLAT', 250.0, 50.0),
    'oak_sapling':           ('FLAT', 200.0, 10.0),
    'spruce_sapling':        ('FLAT', 200.0, 10.0),
    'birch_sapling':         ('FLAT', 200.0, 10.0),
    'jungle_sapling':        ('FLAT', 250.0, 15.0),
    'acacia_sapling':        ('FLAT', 200.0, 10.0),
    'dark_oak_sapling':      ('FLAT', 250.0, 15.0),
    'mangrove_propagule':    ('FLAT', 250.0, 15.0),
    'brown_mushroom':        ('FLAT', 250.0, 25.0),
    'red_mushroom':          ('FLAT', 250.0, 25.0),
    'crimson_fungus':        ('FLAT', 300.0, 30.0),
    'warped_fungus':         ('FLAT', 300.0, 30.0),
    'weeping_vines':         ('FLAT', 300.0, 30.0),
    'warped_roots':          ('FLAT', 250.0, 25.0),
    'twisting_vines':        ('FLAT', 300.0, 30.0),
    'bamboo':                ('FLAT', 200.0, 15.0),
    'kelp':                  ('FLAT', 200.0, 15.0),
    'lily_pad':              ('FLAT', 200.0, 20.0),
    'chorus_fruit':          ('FLAT', 400.0, 60.0),
    'chorus_flower':         ('FLAT', 500.0, 80.0),
}

FOOD_PRICES = {
    'apple':                 ('FLAT', 250.0, 50.0),
    'bread':                 ('FLAT', 300.0, 60.0),
    'baked_potato':          ('FLAT', 350.0, 70.0),
    'cooked_chicken':        ('FLAT', 400.0, 80.0),
    'cooked_cod':            ('FLAT', 350.0, 70.0),
    'cooked_salmon':         ('FLAT', 400.0, 80.0),
    'cooked_rabbit':         ('FLAT', 350.0, 70.0),
    'cooked_porkchop':       ('FLAT', 500.0, 100.0),
    'cooked_beef':           ('FLAT', 500.0, 100.0),
    'cooked_mutton':         ('FLAT', 450.0, 90.0),
    'mushroom_stew':         ('FLAT', 400.0, 80.0),
    'rabbit_stew':           ('FLAT', 500.0, 100.0),
    'beetroot_soup':         ('FLAT', 350.0, 70.0),
    'pumpkin_pie':           ('FLAT', 400.0, 80.0),
    'cookie':                ('FLAT', 200.0, 40.0),
    'cake':                  ('FLAT', 800.0, 160.0),
    'golden_apple':          ('FLAT', 3500.0, 700.0),
    'enchanted_golden_apple':('FLAT', 15000.0, 3000.0),
    'cod':                   ('FLAT', 200.0, 30.0),
    'salmon':                ('FLAT', 250.0, 40.0),
    'tropical_fish':         ('FLAT', 300.0, 45.0),
    'rabbit':                ('FLAT', 200.0, 30.0),
    'porkchop':              ('FLAT', 250.0, 40.0),
    'mutton':                ('FLAT', 250.0, 40.0),
    'chicken':               ('FLAT', 200.0, 30.0),
    'beef':                  ('FLAT', 300.0, 50.0),
    'sweet_berries':         ('FLAT', 200.0, 25.0),
    'glow_berries':          ('FLAT', 250.0, 30.0),
    'dried_kelp':            ('FLAT', 200.0, 20.0),
    'honey_bottle':          ('FLAT', 400.0, 60.0),
    'suspicious_stew':       ('FLAT', 500.0, -1.0),
}

MOB_DROPS_PRICES = {
    'rotten_flesh':          ('DYNAMIC', 200.0, 10.0),
    'bone':                  ('DYNAMIC', 250.0, 25.0),
    'ender_pearl':           ('DYNAMIC', 800.0, 120.0),
    'gunpowder':             ('FLAT', 400.0, 60.0),
    'string':                ('FLAT', 300.0, 40.0),
    'spider_eye':            ('FLAT', 350.0, 50.0),
    'feather':               ('FLAT', 250.0, 30.0),
    'egg':                   ('FLAT', 200.0, 20.0),
    'arrow':                 ('FLAT', 250.0, 15.0),
    'leather':               ('FLAT', 400.0, 60.0),
    'rabbit_hide':           ('FLAT', 300.0, 40.0),
    'rabbit_foot':           ('FLAT', 600.0, 100.0),
    'ink_sac':               ('FLAT', 300.0, 40.0),
    'glow_ink_sac':          ('FLAT', 400.0, 60.0),
    'slime_ball':            ('FLAT', 500.0, 80.0),
    'blaze_rod':             ('FLAT', 700.0, 120.0),
    'magma_cream':           ('FLAT', 600.0, 100.0),
    'ghast_tear':            ('FLAT', 1000.0, 180.0),
    'prismarine_shard':      ('FLAT', 500.0, 80.0),
    'prismarine_crystals':   ('FLAT', 500.0, 80.0),
    'totem_of_undying':      ('FLAT', 12000.0, 2000.0),
    'turtle_scute':          ('FLAT', 800.0, 130.0),
    'phantom_membrane':      ('FLAT', 700.0, 120.0),
    'nautilus_shell':        ('FLAT', 1200.0, 200.0),
    'armadillo_scute':       ('FLAT', 600.0, 100.0),
    'sculk_catalyst':        ('FLAT', 1500.0, 250.0),
}

COMBAT_TOOLS_PRICES = {
    'iron_helmet':           ('FLAT', 1500.0, -1.0),
    'iron_chestplate':       ('FLAT', 2500.0, -1.0),
    'iron_leggings':         ('FLAT', 2200.0, -1.0),
    'iron_boots':            ('FLAT', 1200.0, -1.0),
    'iron_sword':            ('FLAT', 800.0, -1.0),
    'iron_pickaxe':          ('FLAT', 1000.0, -1.0),
    'iron_axe':              ('FLAT', 1000.0, -1.0),
    'iron_shovel':           ('FLAT', 500.0, -1.0),
    'iron_hoe':              ('FLAT', 700.0, -1.0),
    'diamond_helmet':        ('FLAT', 7500.0, 1200.0),
    'diamond_chestplate':    ('FLAT', 12000.0, 2000.0),
    'diamond_leggings':      ('FLAT', 10500.0, 1700.0),
    'diamond_boots':         ('FLAT', 6000.0, 1000.0),
    'diamond_sword':         ('FLAT', 5000.0, 800.0),
    'diamond_pickaxe':       ('FLAT', 7500.0, 1200.0),
    'diamond_axe':           ('FLAT', 7500.0, 1200.0),
    'diamond_shovel':        ('FLAT', 3000.0, 500.0),
    'diamond_hoe':           ('FLAT', 5000.0, 800.0),
    'turtle_helmet':         ('FLAT', 3500.0, -1.0),
    'bow':                   ('FLAT', 500.0, -1.0),
    'crossbow':              ('FLAT', 600.0, -1.0),
    'arrow':                 ('FLAT', 200.0, 15.0),
    'spectral_arrow':        ('FLAT', 500.0, -1.0),
    'trident':               ('FLAT', 10000.0, 1500.0),
    'shield':                ('FLAT', 400.0, -1.0),
    'elytra':                ('FLAT', 14000.0, 2500.0),
    'netherite_upgrade_smithing_template': ('FLAT', 8000.0, 1500.0),
    'fishing_rod':           ('FLAT', 400.0, -1.0),
    'carrot_on_a_stick':     ('FLAT', 300.0, -1.0),
    'warped_fungus_on_a_stick': ('FLAT', 300.0, -1.0),
    'flint_and_steel':       ('FLAT', 350.0, -1.0),
    'name_tag':              ('FLAT', 1500.0, -1.0),
    'lead':                  ('FLAT', 500.0, -1.0),
    'shears':                ('FLAT', 350.0, -1.0),
}

REDSTONE_PRICES = {
    'redstone':              ('DYNAMIC', 250.0, 50.0),
    'lectern':               ('FLAT', 600.0, 100.0),
    'repeater':              ('FLAT', 400.0, 60.0),
    'comparator':            ('FLAT', 500.0, 80.0),
    'hopper':                ('FLAT', 1200.0, 200.0),
    'piston':                ('FLAT', 800.0, 130.0),
    'sticky_piston':         ('FLAT', 1200.0, 200.0),
    'daylight_detector':     ('FLAT', 600.0, 100.0),
    'target':                ('FLAT', 500.0, 80.0),
    'note_block':            ('FLAT', 400.0, 60.0),
    'dropper':               ('FLAT', 500.0, 80.0),
    'dispenser':             ('FLAT', 600.0, 100.0),
    'observer':              ('FLAT', 800.0, 130.0),
    'crafter':               ('FLAT', 1500.0, 250.0),
    'trapped_chest':         ('FLAT', 400.0, 60.0),
    'redstone_torch':        ('FLAT', 300.0, 40.0),
    'redstone_lamp':         ('FLAT', 700.0, 110.0),
    'lever':                 ('FLAT', 200.0, 15.0),
    'tripwire_hook':         ('FLAT', 400.0, 60.0),
}

MISCELLANEOUS_PRICES = {
    'composter':             ('FLAT', 300.0, -1.0),
    'honeycomb':             ('FLAT', 400.0, 50.0),
    'spyglass':              ('FLAT', 500.0, 80.0),
    'brewing_stand':         ('FLAT', 800.0, -1.0),
    'cauldron':              ('FLAT', 500.0, 80.0),
    'clock':                 ('FLAT', 1200.0, -1.0),
    'compass':               ('FLAT', 1000.0, -1.0),
    'saddle':                ('FLAT', 2500.0, 400.0),
    'anvil':                 ('FLAT', 3000.0, -1.0),
    'amethyst_shard':        ('FLAT', 500.0, 60.0),
    'echo_shard':            ('FLAT', 2500.0, 400.0),
    'sculk_shrieker':        ('FLAT', 2000.0, 300.0),
    'sculk_sensor':          ('FLAT', 1500.0, 250.0),
    'leather_horse_armor':   ('FLAT', 1000.0, -1.0),
    'iron_horse_armor':      ('FLAT', 2500.0, 400.0),
    'golden_horse_armor':    ('FLAT', 4000.0, 650.0),
    'diamond_horse_armor':   ('FLAT', 8000.0, 1300.0),
    'bucket':                ('FLAT', 1000.0, -1.0),
    'milk_bucket':           ('FLAT', 1200.0, -1.0),
    'water_bucket':          ('FLAT', 1000.0, -1.0),
    'lava_bucket':           ('FLAT', 2000.0, -1.0),
    'powder_snow_bucket':    ('FLAT', 1200.0, -1.0),
    'pufferfish_bucket':     ('FLAT', 1500.0, -1.0),
    'salmon_bucket':         ('FLAT', 1500.0, -1.0),
    'cod_bucket':            ('FLAT', 1500.0, -1.0),
    'tropical_fish_bucket':  ('FLAT', 1500.0, -1.0),
    'axolotl_bucket':        ('FLAT', 2000.0, -1.0),
    'tadpole_bucket':        ('FLAT', 1500.0, -1.0),
}

# ============================================================================
# PRICE UPDATE ENGINE - Works with both old and new format
# ============================================================================
def find_and_replace_price(content, item_name, price_type, buy, sell):
    """Find the Price block for an item and replace it entirely."""
    lines = content.split('\n')
    
    # Find the item header line (2-space indent)
    item_start = None
    for i, line in enumerate(lines):
        # Match "  item_name:" exactly at 2-space indent
        stripped = line.rstrip()
        if stripped == f'  {item_name}:':
            item_start = i
            break
    
    if item_start is None:
        return content, False
    
    # Find the Price: line within this item
    price_line = None
    for i in range(item_start + 1, min(item_start + 20, len(lines))):
        if lines[i].strip() == 'Price:':
            price_line = i
            break
    
    if price_line is None:
        return content, False
    
    # Find the end of Price block (next line at 4-space indent that's not part of Price)
    price_end = None
    for i in range(price_line + 1, min(price_line + 30, len(lines))):
        stripped = lines[i].strip()
        if stripped == '':
            continue
        # Check indent level - Price content is at 6+ spaces
        # Stock: or Shop_View: at 4 spaces marks end
        leading = len(lines[i]) - len(lines[i].lstrip())
        if leading <= 4 and stripped != '':
            price_end = i
            break
    
    if price_end is None:
        return content, False
    
    # Build new price block
    if price_type == 'DYNAMIC':
        new_price_lines = [
            '    Price:',
            dynamic_block(buy, sell),
        ]
    else:
        new_price_lines = [
            '    Price:',
            flat_block(buy, sell),
        ]
    
    # Replace lines
    new_lines = lines[:price_line] + new_price_lines + lines[price_end:]
    return '\n'.join(new_lines), True


def update_file(filepath, prices_dict):
    """Update prices in a YAML file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    changes = 0
    
    for item_name, price_info in prices_dict.items():
        if price_info is None:
            continue
        
        price_type, buy, sell = price_info
        content, changed = find_and_replace_price(content, item_name, price_type, buy, sell)
        if changed:
            changes += 1
        else:
            print(f"  [SKIP] {item_name} not found in {os.path.basename(filepath)}")
    
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✅ Updated {os.path.basename(filepath)}: {changes} items changed")
    else:
        print(f"  ⏭️  No changes for {os.path.basename(filepath)}")
    
    return changes


# ============================================================================
# MAIN
# ============================================================================
def main():
    print("=" * 60)
    print("NaturalSMP Economy Overhaul v2 - Fixed Format")
    print("Key: BUY/SELL (uppercase), StartValue (not Start)")
    print("=" * 60)

    total = 0

    print("\n⛏️ Minerals")
    total += update_file(os.path.join(SHOPS_DIR, "minerals.yml"), MINERALS_PRICES)

    print("\n🌾 Farming")
    total += update_file(os.path.join(SHOPS_DIR, "farming.yml"), FARMING_PRICES)

    print("\n🍖 Food")
    total += update_file(os.path.join(SHOPS_DIR, "food.yml"), FOOD_PRICES)

    print("\n💀 Mob Drops")
    total += update_file(os.path.join(SHOPS_DIR, "mob_drops.yml"), MOB_DROPS_PRICES)

    print("\n⚔️ Combat & Tools")
    total += update_file(os.path.join(SHOPS_DIR, "combat_tools.yml"), COMBAT_TOOLS_PRICES)

    print("\n🔴 Redstone")
    total += update_file(os.path.join(SHOPS_DIR, "redstone.yml"), REDSTONE_PRICES)

    print("\n🧩 Miscellaneous")
    total += update_file(os.path.join(SHOPS_DIR, "miscellaneous.yml"), MISCELLANEOUS_PRICES)

    print(f"\n{'=' * 60}")
    print(f"✅ Total: {total} items updated across all files")
    print("=" * 60)

if __name__ == "__main__":
    main()
