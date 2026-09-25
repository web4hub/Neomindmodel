from brain.swarm.swarm_manager import SwarmManager

def test_swarm_peers():
    swarm = SwarmManager("a")
    swarm.register_peer("b")
    assert swarm.peers_snapshot() == ["b"]
