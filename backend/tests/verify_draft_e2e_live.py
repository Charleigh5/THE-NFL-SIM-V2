"""Live verification script for Draft Room API and flow."""
import urllib.request
import json

def verify_draft_flow():
    s_id = 1
    base = 'http://127.0.0.1:8000/api'
    
    # 1. Draft Board
    board_res = urllib.request.urlopen(f'{base}/draft/board')
    board = json.loads(board_res.read().decode())
    print(f"[1/7] Draft Board Prospects Available: {len(board)}")
    assert len(board) > 0, "Draft board should not be empty"
    
    # 2. Current Pick
    curr_res = urllib.request.urlopen(f'{base}/season/{s_id}/draft/current')
    current = json.loads(curr_res.read().decode())
    print(f"[2/7] Initial On-The-Clock: Round {current['round']}, Pick #{current['pick_number']} for Team {current['team_id']}")
    assert current['player_id'] is None, "Current pick should be unassigned"
    
    # 3. Team Needs
    needs_res = urllib.request.urlopen(f'{base}/season/{s_id}/needs/{current["team_id"]}')
    needs = json.loads(needs_res.read().decode())
    print(f"[3/7] Team Needs for Team {current['team_id']}: {len(needs)} positions, Top need = {needs[0]['position']} (Score: {needs[0]['need_score']})")
    
    # 4. Make Manual Selection
    top_player = board[0]
    pick_req = urllib.request.Request(
        f'{base}/season/{s_id}/draft/pick',
        data=json.dumps({'player_id': top_player['id']}).encode(),
        headers={'Content-Type': 'application/json'}
    )
    pick_res = json.loads(urllib.request.urlopen(pick_req).read().decode())
    print(f"[4/7] Pick Success: {top_player['first_name']} {top_player['last_name']} ({top_player['position']}) drafted to Team {pick_res['team_id']} with Pick #{pick_res['pick_number']}")
    assert pick_res['player_id'] == top_player['id']
    
    # 5. Check Next Pick Advanced
    curr2_res = urllib.request.urlopen(f'{base}/season/{s_id}/draft/current')
    current_after = json.loads(curr2_res.read().decode())
    print(f"[5/7] Next On-The-Clock: Round {current_after['round']}, Pick #{current_after['pick_number']} for Team {current_after['team_id']}")
    assert current_after['pick_number'] == current['pick_number'] + 1
    
    # 6. Simulate Next Pick
    sim_req = urllib.request.Request(
        f'{base}/season/{s_id}/draft/simulate-next',
        data=b'{}',
        headers={'Content-Type': 'application/json'}
    )
    sim_res = json.loads(urllib.request.urlopen(sim_req).read().decode())
    print(f"[6/7] AI Pick Simulation Success: Team {sim_res['team_id']} selected {sim_res['player_name']} ({sim_res['player_position']}) with Pick #{sim_res['pick_number']}")
    
    # 7. Check Next Pick Advanced After Sim
    curr3_res = urllib.request.urlopen(f'{base}/season/{s_id}/draft/current')
    current_after_sim = json.loads(curr3_res.read().decode())
    print(f"[7/7] On-The-Clock After Sim: Round {current_after_sim['round']}, Pick #{current_after_sim['pick_number']} for Team {current_after_sim['team_id']}")
    assert current_after_sim['pick_number'] == current_after['pick_number'] + 1
    
    print("\nSUCCESS: All 7 Draft Room live interactions verified end-to-end!")

if __name__ == '__main__':
    verify_draft_flow()
