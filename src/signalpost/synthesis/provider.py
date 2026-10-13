"""Provider-agnostic interface. No network adapter is enabled in this release."""
from dataclasses import dataclass
from typing import Protocol

# Synthetic USD/million-token rates for offline budget tests only.
# Populate verified model rates before enabling an execution adapter.
PRICE_TABLE={'offline-fake':(0.0,0.0),'offline-priced':(1.0,2.0)}
PRICE_TABLE_REQUIRES_UPDATE=True

@dataclass
class Reply:
    text: str
    input_tokens: int
    output_tokens: int

class Provider(Protocol):
    name: str
    model: str
    async def complete(self,messages:list[dict],max_output_tokens:int)->Reply: ...

def configured_provider():
    # Environment selection is reserved; adapters require explicit injection.
    return None
