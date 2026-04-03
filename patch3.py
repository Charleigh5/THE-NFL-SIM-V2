with open("backend/alembic/versions/da6e871020ca_drop_redundant_player_columns.py", "r") as f:
    lines = f.readlines()

new_lines = []
in_player_block = False
for line in lines:
    if line.strip() == "with op.batch_alter_table('player', schema=None) as batch_op:":
        in_player_block = True
        new_lines.append("    pass\n")
        new_lines.append("    # " + line.strip() + "\n")
        continue

    if in_player_block:
        if line.strip() == "# ### end Alembic commands ###" or not line.strip().startswith("batch_op") and not line.strip().startswith("#"):
            in_player_block = False
            new_lines.append(line)
        else:
            new_lines.append("    # " + line.strip() + "\n")
    else:
        new_lines.append(line)

with open("backend/alembic/versions/da6e871020ca_drop_redundant_player_columns.py", "w") as f:
    f.writelines(new_lines)
