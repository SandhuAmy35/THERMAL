import torch
import torch.nn as nn

class DummyAgent(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc = nn.Linear(5, 3) 

    def forward(self, x):
        return self.fc(x)

model = DummyAgent()
sm = torch.jit.script(model)
sm.save("dummy_dqn.pt")
