from __future__ import annotations
from pathlib import Path
from typing import Any

def load_edq_model(checkpoint: str|None=None, vocab_size: int=1000, device: str|None=None) -> Any:
    """Load the repository's existing EDQBrain when PyTorch/checkpoint are available."""
    import torch
    from hybrid_EDQ_Brain import EDQBrain
    model=EDQBrain(vocab_size=vocab_size)
    if checkpoint:
        state=torch.load(Path(checkpoint),map_location=device or "cpu")
        model.load_state_dict(state)
    model.to(device or ("cuda" if torch.cuda.is_available() else "cpu"))
    model.eval()
    return model
