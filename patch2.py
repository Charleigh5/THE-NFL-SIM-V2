import re
with open("backend/alembic/versions/6b7dacdbe3be_add_weather_models.py", "r") as f:
    content = f.read()

content = content.replace("batch_op.create_foreign_key('fk_team_stadium_id', 'stadium', ['stadium_id'], ['id'])", "# batch_op.create_foreign_key('fk_team_stadium_id', 'stadium', ['stadium_id'], ['id'])")

with open("backend/alembic/versions/6b7dacdbe3be_add_weather_models.py", "w") as f:
    f.write(content)
