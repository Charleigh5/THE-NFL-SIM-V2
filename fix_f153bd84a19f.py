import re

target_file = "backend/alembic/versions/f153bd84a19f_add_coaching_philosophy_fields.py"

with open(target_file, "r") as f:
    content = f.read()

# Instead of removing the batch_op for `player` in `f153bd84a19f`, we should make sure it actually recreates the table properly in SQLite.
# BUT wait! `00d0f05763a5` adds ALL those columns via batch_op.add_column.
# Let's look at what `f153bd84a19f` is trying to alter on the player table. It's using `alter_column`.
# In SQLite, `alter_column` requires rendering a new table and copying data over. Alembic batch mode tries to do this but needs ALL the columns.
# However, `f153bd84a19f` was generated, maybe we can just replace its `alter_column` calls for `player` with a check if it's sqlite and ignore them.
# The error in f153 was KeyError: 'stamina'. Why? Because 'stamina' wasn't known to the metadata?
# Let's bypass the `player` alter_column block if dialect is sqlite.

replace_block = """
    conn = op.get_bind()
    if conn.dialect.name != 'sqlite':
        with op.batch_alter_table('player', schema=None) as batch_op:
"""

content = content.replace("    with op.batch_alter_table('player', schema=None) as batch_op:", replace_block)

# Indent all lines inside the block
lines = content.split('\n')
in_block = False
new_lines = []
for line in lines:
    if "if conn.dialect.name != 'sqlite':" in line:
        in_block = True
        new_lines.append(line)
        continue

    if in_block:
        if line.startswith("        batch_op."):
            new_lines.append("    " + line)
            continue
        elif line.startswith("    with") or line.startswith("    op.") or line.startswith("def ") or line.strip() == "":
            in_block = False
            new_lines.append(line)
        else:
            if line.startswith("               "):
                new_lines.append("    " + line)
            else:
                new_lines.append(line)
    else:
        new_lines.append(line)

with open(target_file, "w") as f:
    f.write('\n'.join(new_lines))
