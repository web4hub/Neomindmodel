from brain.models.snn_model import SNNModel

def test_snn_spike():
    model = SNNModel(1.0)
    assert model.spike(1.0) == 1
    assert model.spike(0.5) == 0
