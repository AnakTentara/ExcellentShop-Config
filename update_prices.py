"""
NaturalSMP Economy Overhaul - Bulk Price Update Script
Updates all ExcellentShop YAML configs with new balanced pricing.
"""
import re
import os

SHOP_DIR = os.path.dirname(os.path.abspath(__file__))
SHOPS_DIR = os.path.join(SHOP_DIR, "virtual_shop", "shops")

# ============================================================================
# DYNAMIC PRICING TEMPLATE
# ============================================================================
def dynamic_block(buy_start, sell_start, buy_off=1.0, sell_off=-1.0, min_off=-10.0, max_off=15.0, stab_interval=300, stab_amount=0.5):
    return (
        f"      Type: DYNAMIC\n"
        f"      Buy:\n"
        f"        Start: {buy_start}\n"
        f"        BuyOffset: {buy_off}\n"
        f"        SellOffset: {sell_off}\n"
        f"        MinOffset: {min_off}\n"
        f"        MaxOffset: {max_off}\n"
        f"      Sell:\n"
        f"        Start: {sell_start}\n"
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
        f"      SELL: {sell}\n"
        f"      BUY: {buy}"
    )

# ============================================================================
# PRICING DEFINITIONS PER FILE
# Key = item name in YAML, Value = (type, buy, sell) or (type, buy, sell, offsets...)
# type: 'FLAT' or 'DYNAMIC'
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
}

FARMING_PRICES = {
    # Seeds (cheap, barely sellable)
    'wheat_seeds':           ('FLAT', 200.0, 5.0),
    'pumpkin_seeds':         ('FLAT', 200.0, 5.0),
    'melon_seeds':           ('FLAT', 200.0, 5.0),
    'beetroot_seeds':        ('FLAT', 200.0, 5.0),
    # Crops (Dynamic, farmable)
    'wheat':                 ('DYNAMIC', 250.0, 50.0),
    'carrot':                ('DYNAMIC', 250.0, 50.0),
    'potato':                ('DYNAMIC', 250.0, 50.0),
    'sugar_cane':            ('DYNAMIC', 200.0, 40.0),
    # Crops (Flat)
    'cocoa_beans':           ('FLAT', 300.0, 60.0),
    'pumpkin':               ('FLAT', 400.0, 80.0),
    'melon':                 ('FLAT', 350.0, 70.0),
    'melon_slice':           ('FLAT', 200.0, 25.0),
    'cactus':                ('FLAT', 300.0, 60.0),
    'nether_wart':           ('FLAT', 500.0, 100.0),
    'beetroot':              ('FLAT', 250.0, 50.0),
    # Saplings
    'oak_sapling':           ('FLAT', 200.0, 10.0),
    'spruce_sapling':        ('FLAT', 200.0, 10.0),
    'birch_sapling':         ('FLAT', 200.0, 10.0),
    'jungle_sapling':        ('FLAT', 250.0, 15.0),
    'acacia_sapling':        ('FLAT', 200.0, 10.0),
    'dark_oak_sapling':      ('FLAT', 250.0, 15.0),
    'mangrove_propagule':    ('FLAT', 250.0, 15.0),
    # Nether/Misc plants
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
    # Basic food
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
    # Prepared food
    'mushroom_stew':         ('FLAT', 400.0, 80.0),
    'rabbit_stew':           ('FLAT', 500.0, 100.0),
    'beetroot_soup':         ('FLAT', 350.0, 70.0),
    'pumpkin_pie':           ('FLAT', 400.0, 80.0),
    'cookie':                ('FLAT', 200.0, 40.0),
    'cake':                  ('FLAT', 800.0, 160.0),
    # Premium food
    'golden_apple':          ('FLAT', 3500.0, 700.0),
    'enchanted_golden_apple':('FLAT', 15000.0, 3000.0),
    # Raw food
    'cod':                   ('FLAT', 200.0, 30.0),
    'salmon':                ('FLAT', 250.0, 40.0),
    'tropical_fish':         ('FLAT', 300.0, 45.0),
    'rabbit':                ('FLAT', 200.0, 30.0),
    'porkchop':              ('FLAT', 250.0, 40.0),
    'mutton':                ('FLAT', 250.0, 40.0),
    'chicken':               ('FLAT', 200.0, 30.0),
    'beef':                  ('FLAT', 300.0, 50.0),
    # Berries & snacks
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
    # Flat drops
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
    # Iron gear (buy only)
    'iron_helmet':           ('FLAT', 1500.0, -1.0),
    'iron_chestplate':       ('FLAT', 2500.0, -1.0),
    'iron_leggings':         ('FLAT', 2200.0, -1.0),
    'iron_boots':            ('FLAT', 1200.0, -1.0),
    'iron_sword':            ('FLAT', 800.0, -1.0),
    'iron_pickaxe':          ('FLAT', 1000.0, -1.0),
    'iron_axe':              ('FLAT', 1000.0, -1.0),
    'iron_shovel':           ('FLAT', 500.0, -1.0),
    'iron_hoe':              ('FLAT', 700.0, -1.0),
    # Diamond gear (sellable)
    'diamond_helmet':        ('FLAT', 7500.0, 1200.0),
    'diamond_chestplate':    ('FLAT', 12000.0, 2000.0),
    'diamond_leggings':      ('FLAT', 10500.0, 1700.0),
    'diamond_boots':         ('FLAT', 6000.0, 1000.0),
    'diamond_sword':         ('FLAT', 5000.0, 800.0),
    'diamond_pickaxe':       ('FLAT', 7500.0, 1200.0),
    'diamond_axe':           ('FLAT', 7500.0, 1200.0),
    'diamond_shovel':        ('FLAT', 3000.0, 500.0),
    'diamond_hoe':           ('FLAT', 5000.0, 800.0),
    # Special equipment
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

# Building blocks: fix the extreme ratios (20:1) but keep prices low for building
BUILDING_BLOCKS_PRICES = {
    'grass_block':           ('FLAT', 100.0, 20.0),
    'dirt':                  ('FLAT', 50.0, 10.0),
    'coarse_dirt':           ('FLAT', 100.0, 15.0),
    'farmland':              ('FLAT', 100.0, 15.0),
    'rooted_dirt':           ('FLAT', 100.0, 15.0),
    'podzol':                ('FLAT', 150.0, 20.0),
    'mycelium':              ('FLAT', 200.0, 30.0),
    'crimson_nylium':        ('FLAT', 200.0, 30.0),
    'warped_nylium':         ('FLAT', 200.0, 30.0),
    'warped_wart_block':     ('FLAT', 150.0, 20.0),
    'gravel':                ('FLAT', 80.0, 15.0),
    'glass':                 ('FLAT', 150.0, 30.0),
    'glass_pane':            ('FLAT', 80.0, 10.0),
    'ice':                   ('FLAT', 200.0, 30.0),
    'blue_ice':              ('FLAT', 500.0, 80.0),
    'packed_ice':            ('FLAT', 300.0, 50.0),
    'snow_block':            ('FLAT', 100.0, 15.0),
    'obsidian':              ('FLAT', 500.0, 100.0),
    'crying_obsidian':       ('FLAT', 1000.0, 200.0),
    'respawn_anchor':        ('FLAT', 5000.0, 800.0),
    'bookshelf':             ('FLAT', 300.0, 50.0),
    'soul_sand':             ('FLAT', 200.0, 30.0),
    'soul_soil':             ('FLAT', 200.0, 30.0),
    'glowstone':             ('FLAT', 400.0, 60.0),
    'hay_block':             ('FLAT', 250.0, 40.0),
    'magma_block':           ('FLAT', 300.0, 50.0),
    'bone_block':            ('FLAT', 250.0, 40.0),
    'prismarine':            ('FLAT', 400.0, 60.0),
    'prismarine_bricks':     ('FLAT', 500.0, 80.0),
    'dark_prismarine':       ('FLAT', 500.0, 80.0),
    'sea_lantern':           ('FLAT', 600.0, 100.0),
    'end_stone':             ('FLAT', 300.0, 50.0),
    'end_stone_bricks':      ('FLAT', 400.0, 60.0),
    'purpur_block':          ('FLAT', 400.0, 60.0),
    'purpur_pillar':         ('FLAT', 400.0, 60.0),
    'purpur_slab':           ('FLAT', 200.0, 30.0),
    'purpur_stairs':         ('FLAT', 400.0, 60.0),
    'nether_bricks':         ('FLAT', 300.0, 50.0),
    'red_nether_bricks':     ('FLAT', 400.0, 60.0),
    'chiseled_nether_bricks':('FLAT', 400.0, 60.0),
    'cracked_nether_bricks': ('FLAT', 400.0, 60.0),
    'basalt':                ('FLAT', 150.0, 20.0),
    'polished_basalt':       ('FLAT', 200.0, 30.0),
    'smooth_basalt':         ('FLAT', 200.0, 30.0),
    'blackstone':            ('FLAT', 150.0, 20.0),
    'polished_blackstone':   ('FLAT', 200.0, 30.0),
    'polished_blackstone_bricks': ('FLAT', 250.0, 40.0),
    'chiseled_polished_blackstone': ('FLAT', 300.0, 50.0),
    'cracked_polished_blackstone_bricks': ('FLAT', 250.0, 40.0),
    'gilded_blackstone':     ('FLAT', 500.0, 80.0),
    'netherrack':            ('FLAT', 50.0, 5.0),
    'nether_wart_block':     ('FLAT', 150.0, 20.0),
    'shroomlight':           ('FLAT', 400.0, 60.0),
    'crimson_stem':          ('FLAT', 150.0, 20.0),
    'warped_stem':           ('FLAT', 150.0, 20.0),
    'stripped_crimson_stem':  ('FLAT', 200.0, 30.0),
    'stripped_warped_stem':   ('FLAT', 200.0, 30.0),
    'crimson_hyphae':        ('FLAT', 150.0, 20.0),
    'warped_hyphae':         ('FLAT', 150.0, 20.0),
    'stripped_crimson_hyphae':('FLAT', 200.0, 30.0),
    'stripped_warped_hyphae': ('FLAT', 200.0, 30.0),
    'crimson_planks':        ('FLAT', 100.0, 15.0),
    'warped_planks':         ('FLAT', 100.0, 15.0),
    'crimson_slab':          ('FLAT', 50.0, 8.0),
    'warped_slab':           ('FLAT', 50.0, 8.0),
    'crimson_stairs':        ('FLAT', 100.0, 15.0),
    'warped_stairs':         ('FLAT', 100.0, 15.0),
    'crimson_fence':         ('FLAT', 100.0, 15.0),
    'warped_fence':          ('FLAT', 100.0, 15.0),
    'crimson_fence_gate':    ('FLAT', 150.0, 20.0),
    'warped_fence_gate':     ('FLAT', 150.0, 20.0),
    'crimson_door':          ('FLAT', 150.0, 20.0),
    'warped_door':           ('FLAT', 150.0, 20.0),
    'crimson_trapdoor':      ('FLAT', 150.0, 20.0),
    'warped_trapdoor':       ('FLAT', 150.0, 20.0),
    'crimson_pressure_plate':('FLAT', 100.0, 15.0),
    'warped_pressure_plate': ('FLAT', 100.0, 15.0),
    'crimson_button':        ('FLAT', 50.0, 8.0),
    'warped_button':         ('FLAT', 50.0, 8.0),
    'crimson_sign':          ('FLAT', 100.0, 15.0),
    'warped_sign':           ('FLAT', 100.0, 15.0),
    'crimson_hanging_sign':  ('FLAT', 150.0, 20.0),
    'warped_hanging_sign':   ('FLAT', 150.0, 20.0),
    # Stone variants
    'stone':                 ('FLAT', 100.0, 15.0),
    'cobblestone':           ('FLAT', 50.0, 8.0),
    'mossy_cobblestone':     ('FLAT', 150.0, 20.0),
    'smooth_stone':          ('FLAT', 150.0, 20.0),
    'stone_bricks':          ('FLAT', 150.0, 20.0),
    'mossy_stone_bricks':    ('FLAT', 200.0, 30.0),
    'cracked_stone_bricks':  ('FLAT', 200.0, 30.0),
    'chiseled_stone_bricks': ('FLAT', 200.0, 30.0),
    'deepslate':             ('FLAT', 100.0, 15.0),
    'cobbled_deepslate':     ('FLAT', 100.0, 15.0),
    'polished_deepslate':    ('FLAT', 150.0, 20.0),
    'deepslate_bricks':      ('FLAT', 200.0, 30.0),
    'deepslate_tiles':       ('FLAT', 200.0, 30.0),
    'chiseled_deepslate':    ('FLAT', 250.0, 40.0),
    'cracked_deepslate_bricks': ('FLAT', 200.0, 30.0),
    'cracked_deepslate_tiles':  ('FLAT', 200.0, 30.0),
    'tuff':                  ('FLAT', 100.0, 15.0),
    'polished_tuff':         ('FLAT', 150.0, 20.0),
    'tuff_bricks':           ('FLAT', 200.0, 30.0),
    'chiseled_tuff':         ('FLAT', 200.0, 30.0),
    'chiseled_tuff_bricks':  ('FLAT', 250.0, 40.0),
    'calcite':               ('FLAT', 150.0, 20.0),
    'dripstone_block':       ('FLAT', 150.0, 20.0),
    'pointed_dripstone':     ('FLAT', 200.0, 30.0),
    'amethyst_block':        ('FLAT', 400.0, 60.0),
    'budding_amethyst':      ('FLAT', 2000.0, 300.0),
    'mud':                   ('FLAT', 100.0, 15.0),
    'packed_mud':            ('FLAT', 150.0, 20.0),
    'mud_bricks':            ('FLAT', 200.0, 30.0),
    'clay':                  ('FLAT', 200.0, 30.0),
    'bricks':                ('FLAT', 200.0, 30.0),
    'terracotta':            ('FLAT', 200.0, 30.0),
    'sandstone':             ('FLAT', 100.0, 15.0),
    'red_sandstone':         ('FLAT', 100.0, 15.0),
    'smooth_sandstone':      ('FLAT', 150.0, 20.0),
    'smooth_red_sandstone':  ('FLAT', 150.0, 20.0),
    'chiseled_sandstone':    ('FLAT', 200.0, 30.0),
    'chiseled_red_sandstone':('FLAT', 200.0, 30.0),
    'cut_sandstone':         ('FLAT', 150.0, 20.0),
    'cut_red_sandstone':     ('FLAT', 150.0, 20.0),
    'sand':                  ('FLAT', 50.0, 8.0),
    'red_sand':              ('FLAT', 80.0, 12.0),
    # Wood types (common pattern)
    'oak_log':               ('FLAT', 100.0, 15.0),
    'spruce_log':            ('FLAT', 100.0, 15.0),
    'birch_log':             ('FLAT', 100.0, 15.0),
    'jungle_log':            ('FLAT', 100.0, 15.0),
    'acacia_log':            ('FLAT', 100.0, 15.0),
    'dark_oak_log':          ('FLAT', 100.0, 15.0),
    'mangrove_log':          ('FLAT', 100.0, 15.0),
    'cherry_log':            ('FLAT', 150.0, 20.0),
    'stripped_oak_log':      ('FLAT', 150.0, 20.0),
    'stripped_spruce_log':   ('FLAT', 150.0, 20.0),
    'stripped_birch_log':    ('FLAT', 150.0, 20.0),
    'stripped_jungle_log':   ('FLAT', 150.0, 20.0),
    'stripped_acacia_log':   ('FLAT', 150.0, 20.0),
    'stripped_dark_oak_log': ('FLAT', 150.0, 20.0),
    'stripped_mangrove_log': ('FLAT', 150.0, 20.0),
    'stripped_cherry_log':   ('FLAT', 200.0, 30.0),
    'oak_wood':              ('FLAT', 100.0, 15.0),
    'spruce_wood':           ('FLAT', 100.0, 15.0),
    'birch_wood':            ('FLAT', 100.0, 15.0),
    'jungle_wood':           ('FLAT', 100.0, 15.0),
    'acacia_wood':           ('FLAT', 100.0, 15.0),
    'dark_oak_wood':         ('FLAT', 100.0, 15.0),
    'mangrove_wood':         ('FLAT', 100.0, 15.0),
    'cherry_wood':           ('FLAT', 150.0, 20.0),
    'stripped_oak_wood':     ('FLAT', 150.0, 20.0),
    'stripped_spruce_wood':  ('FLAT', 150.0, 20.0),
    'stripped_birch_wood':   ('FLAT', 150.0, 20.0),
    'stripped_jungle_wood':  ('FLAT', 150.0, 20.0),
    'stripped_acacia_wood':  ('FLAT', 150.0, 20.0),
    'stripped_dark_oak_wood':('FLAT', 150.0, 20.0),
    'stripped_mangrove_wood':('FLAT', 150.0, 20.0),
    'stripped_cherry_wood':  ('FLAT', 200.0, 30.0),
    'oak_planks':            ('FLAT', 50.0, 8.0),
    'spruce_planks':         ('FLAT', 50.0, 8.0),
    'birch_planks':          ('FLAT', 50.0, 8.0),
    'jungle_planks':         ('FLAT', 50.0, 8.0),
    'acacia_planks':         ('FLAT', 50.0, 8.0),
    'dark_oak_planks':       ('FLAT', 50.0, 8.0),
    'mangrove_planks':       ('FLAT', 50.0, 8.0),
    'cherry_planks':         ('FLAT', 80.0, 12.0),
    'bamboo_planks':         ('FLAT', 50.0, 8.0),
    'bamboo_mosaic':         ('FLAT', 80.0, 12.0),
    'bamboo_block':          ('FLAT', 100.0, 15.0),
    'stripped_bamboo_block':  ('FLAT', 150.0, 20.0),
}

# Potions: all buy-only, already reasonable prices. Just ensure consistency.
# We'll apply a standard potion pricing tier system.
POTIONS_PRICES = {
    # Basic potions: 200-300
    'potion': None,     # Skip - individual potion items have different names
    'potion_1': None,
    # We'll handle potions with a default fallback approach
}

# ============================================================================
# PRICE UPDATE ENGINE
# ============================================================================
def find_price_block(content, item_name):
    """Find the Price block for an item in the YAML content.
    Returns (start_pos, end_pos) of the Price block content (after 'Price:' line, before 'Stock:' line)."""
    # Find the item definition
    item_pattern = re.compile(r'^  ' + re.escape(item_name) + r':\s*$', re.MULTILINE)
    match = item_pattern.search(content)
    if not match:
        return None, None

    item_start = match.start()

    # Find Price: within this item (before next item or end)
    # Next item starts with '  <name>:' at 2-space indent (same level)
    next_item = re.search(r'\n  [a-z_]+:', content[item_start + len(match.group()):])
    item_end = item_start + len(match.group()) + next_item.start() if next_item else len(content)

    item_content = content[item_start:item_end]

    # Find Price: block within item
    price_match = re.search(r'\n    Price:\n', item_content)
    if not price_match:
        return None, None

    price_start_in_item = price_match.start() + 1  # skip leading \n
    price_start_abs = item_start + price_start_in_item

    # Find Stock: block (marks end of Price block)
    stock_match = re.search(r'\n    Stock:', item_content[price_match.end():])
    if not stock_match:
        return None, None

    price_end_abs = item_start + price_match.end() + stock_match.start()

    return price_start_abs, price_end_abs


def update_file_prices(filepath, prices_dict, default_handler=None):
    """Update prices in a YAML file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content
    changes = 0

    # If we have specific prices, apply them
    for item_name, price_info in prices_dict.items():
        if price_info is None:
            continue

        price_type, buy, sell = price_info[0], price_info[1], price_info[2]

        price_start, price_end = find_price_block(content, item_name)
        if price_start is None:
            print(f"  [SKIP] {item_name} not found in {os.path.basename(filepath)}")
            continue

        # Build new price block
        if price_type == 'DYNAMIC':
            new_price = "    Price:\n" + dynamic_block(buy, sell)
        else:
            new_price = "    Price:\n" + flat_block(buy, sell)

        # Replace
        old_price = content[price_start:price_end]
        content = content[:price_start] + new_price + "\n" + content[price_end:]
        changes += 1

    # Handle items NOT in prices_dict but present in file (for default pricing on building blocks etc.)
    if default_handler:
        content = default_handler(content, prices_dict)

    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✅ Updated {os.path.basename(filepath)}: {changes} items changed")
    else:
        print(f"  ⏭️  No changes needed for {os.path.basename(filepath)}")

    return changes


def apply_default_building_prices(content, known_items):
    """For building block items not in our pricing dict, apply sensible defaults.
    Default: BUY:200 SELL:30 for items currently at BUY:1000 SELL:50."""
    # Find all items with SELL: 50.0 BUY: 1000.0 and replace with SELL: 30.0 BUY: 200.0
    content = re.sub(
        r'(      Type: FLAT\n      SELL: )50\.0(\n      BUY: )1000\.0',
        r'\g<1>30.0\g<2>200.0',
        content
    )
    # Fix items with SELL: 100.0 BUY: 1000.0 (glowstone, magma, bone_block, packed_ice, etc.)
    content = re.sub(
        r'(      Type: FLAT\n      SELL: )100\.0(\n      BUY: )1000\.0',
        r'\g<1>40.0\g<2>300.0',
        content
    )
    # Fix items with SELL: 200.0 BUY: 2000.0 (soul sand, blue ice, etc.)
    content = re.sub(
        r'(      Type: FLAT\n      SELL: )200\.0(\n      BUY: )2000\.0',
        r'\g<1>60.0\g<2>400.0',
        content
    )
    # Fix items with SELL: 1000.0 BUY: 5000.0 (crying obsidian)
    content = re.sub(
        r'(      Type: FLAT\n      SELL: )1000\.0(\n      BUY: )5000\.0',
        r'\g<1>200.0\g<2>1000.0',
        content
    )
    # Fix items with SELL: 3000.0 BUY: 15000.0 (respawn anchor)
    content = re.sub(
        r'(      Type: FLAT\n      SELL: )3000\.0(\n      BUY: )15000\.0',
        r'\g<1>800.0\g<2>5000.0',
        content
    )
    return content


def apply_default_decoration_prices(content, known_items):
    """Fix overpriced decoration items."""
    # Fix SELL: 20.0 BUY: 100.0 → keep as is (already reasonable for decoration)
    # Fix SELL: 200.0 BUY: 2000.0 → SELL: 40.0 BUY: 300.0
    content = re.sub(
        r'(      Type: FLAT\n      SELL: )200\.0(\n      BUY: )2000\.0',
        r'\g<1>40.0\g<2>300.0',
        content
    )
    # Fix SELL: 100.0 BUY: 1000.0 → SELL: 30.0 BUY: 200.0
    content = re.sub(
        r'(      Type: FLAT\n      SELL: )100\.0(\n      BUY: )1000\.0',
        r'\g<1>30.0\g<2>200.0',
        content
    )
    return content


def apply_default_potions_prices(content, known_items):
    """Potions are buy-only. Just ensure the prices are sensible.
    Current prices range 150-600 which is already good for the new economy.
    We'll bump them up slightly to match the tighter economy."""
    # Most potions at BUY: 200-250 → bump to 400-500
    # Strong potions at BUY: 400-600 → bump to 800-1200
    # Basic/utility potions at BUY: 150-200 → bump to 300-400

    # Tier 1: cheap potions (150) → 300
    content = re.sub(
        r'(      Type: FLAT\n      SELL: -1\.0\n      BUY: )150\.0',
        r'\g<1>300.0',
        content
    )
    # Tier 2: basic potions (200) → 400
    content = re.sub(
        r'(      Type: FLAT\n      SELL: -1\.0\n      BUY: )200\.0',
        r'\g<1>400.0',
        content
    )
    # Tier 3: mid potions (250) → 500
    content = re.sub(
        r'(      Type: FLAT\n      SELL: -1\.0\n      BUY: )250\.0',
        r'\g<1>500.0',
        content
    )
    # Tier 4: good potions (300) → 600
    content = re.sub(
        r'(      Type: FLAT\n      SELL: -1\.0\n      BUY: )300\.0',
        r'\g<1>600.0',
        content
    )
    # Tier 5: strong potions (350) → 700
    content = re.sub(
        r'(      Type: FLAT\n      SELL: -1\.0\n      BUY: )350\.0',
        r'\g<1>700.0',
        content
    )
    # Tier 6: premium potions (400) → 800
    content = re.sub(
        r'(      Type: FLAT\n      SELL: -1\.0\n      BUY: )400\.0',
        r'\g<1>800.0',
        content
    )
    # Tier 7: high potions (450) → 900
    content = re.sub(
        r'(      Type: FLAT\n      SELL: -1\.0\n      BUY: )450\.0',
        r'\g<1>900.0',
        content
    )
    # Tier 8: top potions (500) → 1000
    content = re.sub(
        r'(      Type: FLAT\n      SELL: -1\.0\n      BUY: )500\.0',
        r'\g<1>1000.0',
        content
    )
    # Tier 9: best potions (600) → 1200
    content = re.sub(
        r'(      Type: FLAT\n      SELL: -1\.0\n      BUY: )600\.0',
        r'\g<1>1200.0',
        content
    )
    return content


def apply_default_colored_prices(content, known_items):
    """Colored blocks already have reasonable prices. Just adjust the 200→150 for wool
    and keep carpet at 100."""
    # Wool at BUY:200 SELL:40 → keep as is (already reasonable)
    # Carpet at BUY:100 SELL:20 → keep as is (already reasonable)
    # BUT fix any items with extreme ratios
    # Stained glass panes etc at BUY:100 SELL:20 → keep
    # Glazed terracotta, concrete, etc at BUY:200 SELL:40 → keep
    # These are all already reasonable with 5:1 ratio
    return content


# ============================================================================
# SETTINGS.yml UPDATE - Sell Multipliers
# ============================================================================
def update_settings():
    """Update sell multipliers for rank system."""
    settings_path = os.path.join(SHOP_DIR, "virtual_shop", "settings.yml")
    with open(settings_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find and update Sell_Multipliers section
    # Current: VIP: 1.5, Gold: 2.0
    # New: midi: 1.05, vip: 1.1, mvp: 1.2, nature: 1.3

    old_multiplier = """Sell_Multipliers:
    vip: 1.5
    gold: 2.0"""

    new_multiplier = """Sell_Multipliers:
    midi: 1.05
    vip: 1.1
    mvp: 1.2
    nature: 1.3"""

    if old_multiplier in content:
        content = content.replace(old_multiplier, new_multiplier)
        with open(settings_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("  ✅ Updated settings.yml: Sell multipliers (midi 1.05x, vip 1.1x, mvp 1.2x, nature 1.3x)")
    else:
        print("  ⚠️  Could not find Sell_Multipliers in settings.yml (might already be updated or different format)")


# ============================================================================
# MAIN
# ============================================================================
def main():
    print("=" * 60)
    print("NaturalSMP Economy Overhaul - Price Updater")
    print("=" * 60)

    print("\n📋 Phase 1: Settings")
    update_settings()

    print("\n⛏️ Phase 2: Minerals")
    update_file_prices(os.path.join(SHOPS_DIR, "minerals.yml"), MINERALS_PRICES)

    print("\n🌾 Phase 3: Farming")
    update_file_prices(os.path.join(SHOPS_DIR, "farming.yml"), FARMING_PRICES)

    print("\n🍖 Phase 4: Food")
    update_file_prices(os.path.join(SHOPS_DIR, "food.yml"), FOOD_PRICES)

    print("\n💀 Phase 5: Mob Drops")
    update_file_prices(os.path.join(SHOPS_DIR, "mob_drops.yml"), MOB_DROPS_PRICES)

    print("\n⚔️ Phase 6: Combat & Tools")
    update_file_prices(os.path.join(SHOPS_DIR, "combat_tools.yml"), COMBAT_TOOLS_PRICES)

    print("\n🔴 Phase 7: Redstone")
    update_file_prices(os.path.join(SHOPS_DIR, "redstone.yml"), REDSTONE_PRICES)

    print("\n🧩 Phase 8: Miscellaneous")
    update_file_prices(os.path.join(SHOPS_DIR, "miscellaneous.yml"), MISCELLANEOUS_PRICES)

    print("\n🧱 Phase 9: Building Blocks")
    update_file_prices(os.path.join(SHOPS_DIR, "building_blocks.yml"), BUILDING_BLOCKS_PRICES, apply_default_building_prices)

    print("\n🎨 Phase 10: Colored Blocks")
    update_file_prices(os.path.join(SHOPS_DIR, "colored_blocks.yml"), {}, apply_default_colored_prices)

    print("\n🌸 Phase 11: Decoration")
    update_file_prices(os.path.join(SHOPS_DIR, "decoration.yml"), {}, apply_default_decoration_prices)

    print("\n🧪 Phase 12: Potions")
    update_file_prices(os.path.join(SHOPS_DIR, "potions.yml"), {}, apply_default_potions_prices)

    print("\n" + "=" * 60)
    print("✅ Economy Overhaul Complete!")
    print("=" * 60)

if __name__ == "__main__":
    main()
