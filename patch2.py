with open("backend/alembic/versions/126ecc4d4b88_decompose_player_model.py", "r") as f:
    lines = f.readlines()

new_lines = []
skip = False
for line in lines:
    if line.strip() == "# --- Data Migration: Preserving Data ---":
        skip = True

    if skip:
        if line.strip() == "# --- Dropping Old Columns ---":
            skip = False
            new_lines.append("    pass\n")
            new_lines.append(line)
        else:
            new_lines.append("# " + line)
    else:
        new_lines.append(line)

with open("backend/alembic/versions/126ecc4d4b88_decompose_player_model.py", "w") as f:
    f.writelines(new_lines)
