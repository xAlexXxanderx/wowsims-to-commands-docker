#!/bin/bash

cd /app/
jupyter execute wowsims_to_add_commands.ipynb

mkdir web/data
cp df_item.pkl web/data/df_item.pkl
cp df_spell.pkl web/data/df_spell.pkl
