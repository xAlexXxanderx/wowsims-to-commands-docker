# Import
import js
import pickle

from pandas import DataFrame

################################
# Load input, Setup output
################################

# Load names from textArea
inputTextArea = js.document.getElementById("inputTextArea")
outputTextArea = js.document.getElementById("outputTextArea")

# Load input bin
from js import inputDfSpell, inputDfItem
# deserialize the bytes object into a DataFrame
df_spell: DataFrame = pickle.loads(inputDfSpell.to_bytes())
df_item: DataFrame = pickle.loads(inputDfItem.to_bytes())

# Read json
import json
try:
    data = json.loads(inputTextArea.value)
except json.decoder.JSONDecodeError:
    raise ValueError('Invalid JSON!')

################################
# Script starts here
################################
items = data['player']['equipment']['items']

# find enchant spells from enchant effect
SPELL_EFFECT_ENCHANT_ITEM = 53
enchant_eff_to_id = {}
for item in items:
    enchant_id = item.get('enchant')
    if not enchant_id:
        continue
    df = df_spell.loc[(df_spell['Effect1'] == SPELL_EFFECT_ENCHANT_ITEM) & (df_spell['EffectMiscValue1'] == enchant_id)]
    if df.empty:
        print(f'ERROR: No match for `enchant_id` in spell.dbc {enchant_id}')
        continue
    spell_id = df['ID'].values[0]
    enchant_eff_to_id[spell_id] = enchant_eff_to_id.get(spell_id, 0) + 1
print(enchant_eff_to_id)

out: list[str] = []

# print .add commands for enchantItems, gems, gear, glyphs
errors = []
for spell_id, amount in enchant_eff_to_id.items():
    df = df_item.loc[df_item['spellid_1'] == spell_id]
    if df.empty:
        errors.append(f'ERROR: No match for `spellid_1` in spell.dbc {spell_id}')
        continue
    entry = df['entry'].values[0]
    out.append(f'.add {entry} {amount}')

out.append('')

gems_total = {}
for i in items:
    if i.get('gems'):
        for j in i['gems']:
            if (j == 0): # sometimes gems are 0
                continue
            if j not in gems_total:
                gems_total[j] = 1
            else:
                gems_total[j] += 1
for gemId, amount in gems_total.items():
    out.append(f'.add {gemId} {amount}')

out.append('')

for i, item in enumerate(items):
    item_id = item.get('id')
    if item_id:
        out.append(f'.add {item_id}')

out.append('')

glyphs = data['player']['glyphs']
for _, itemId in glyphs.items():
    out.append(f'.add {itemId}')

################################
# Output
################################
output = '\n'.join(out)
outputTextArea.value = output