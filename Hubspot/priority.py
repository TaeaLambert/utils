import pydantic

class PriorityConfig(pydantic.BaseModel):
    sleep_if_no_writes: int
    sleep_if_write: float


PRIORITY_CONFIG: dict[str, PriorityConfig] = {
    "fast": PriorityConfig(sleep_if_no_writes=1, sleep_if_write=0.2),
    "normal": PriorityConfig(sleep_if_no_writes=3, sleep_if_write=0.5),
    "slow": PriorityConfig(sleep_if_no_writes=5, sleep_if_write=2),
}
