with open("backend/alembic/versions/f153bd84a19f_add_coaching_philosophy_fields.py", "r") as f:
    lines = f.readlines()

in_player_block = False
new_lines = []
for line in lines:
    if line.strip() == "batch_op.alter_column('position',":
        in_player_block = True

    if in_player_block:
        if line.strip() == "with op.batch_alter_table('player_game_starts', schema=None) as batch_op:":
            in_player_block = False
            new_lines.append(line)
        else:
            new_lines.append("# " + line)
    else:
        new_lines.append(line)

with open("backend/alembic/versions/f153bd84a19f_add_coaching_philosophy_fields.py", "w") as f:
    f.writelines(new_lines)
