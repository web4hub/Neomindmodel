"""Swarm coordination primitives."""
class SwarmManager:
    def __init__(self, node_id: str) -> None:
        self.node_id = node_id
        self.peers: set[str] = set()
    def register_peer(self, peer_id: str) -> None:
        if peer_id != self.node_id:
            self.peers.add(peer_id)
    def peers_snapshot(self) -> list[str]:
        return sorted(self.peers)
