with open("backend/alembic/versions/6b7dacdbe3be_add_weather_models.py", "r") as f:
    content = f.read()

content = content.replace("with op.batch_alter_table('team', schema=None) as batch_op:\n        # batch_op.create_foreign_key('fk_team_stadium_id', 'stadium', ['stadium_id'], ['id'])", "with op.batch_alter_table('team', schema=None) as batch_op:\n        pass")

with open("backend/alembic/versions/6b7dacdbe3be_add_weather_models.py", "w") as f:
    f.write(content)
