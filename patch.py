with open("backend/alembic/versions/6e7b75fed3d6_add_season_id_to_playergamestats.py", "r") as f:
    content = f.read()
content = content.replace("batch_op.create_foreign_key('fk_team_stadium_id', 'stadium', ['stadium_id'], ['id'])", "# batch_op.create_foreign_key('fk_team_stadium_id', 'stadium', ['stadium_id'], ['id'])")
with open("backend/alembic/versions/6e7b75fed3d6_add_season_id_to_playergamestats.py", "w") as f:
    f.write(content)
