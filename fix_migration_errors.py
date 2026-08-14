import re
import os

target_file = "backend/alembic/versions/126ecc4d4b88_decompose_player_model.py"

with open(target_file, "r") as f:
    content = f.read()

# Since `stamina`, `play_recognition`, etc., aren't created in SQLite because we bypassed batch_op.alter_column and didn't add them,
# wait, `00d0f05763a5` adds `stamina` using batch_op! Oh!
# Let's check `00d0f05763a5` again.
