from pathlib import Path
from pydantic import BaseModel, Field


class Config(BaseModel):
    organisations: Path
    output: Path
    report: Path
    bulk: Path | None = None
    verify_bulk: bool = False
    previous: Path | None = None
    site_dir: Path | None = None
    profiles_output: Path | None = None
    state_dir: Path = Path("state")
    envelope_shape: str = "union"
    emit_duplicates: bool = True
    expected_count: int | None = None
    run_id: str = ""
    unrecognized_arguments: list[str] = Field(default_factory=list)
    max_requests: int | None = Field(default=None, ge=0)
    time_budget_seconds: float = Field(default=2100, gt=0)
    # Opt-in only: use the scaled limit (35 min per 100 unique inputs) as the total budget.
    scaled_time_budget: bool = False
    deadline_fraction: float = Field(default=0.85, gt=0, le=1)
    max_cost_usd: float = Field(default=0, ge=0)
    host_concurrency: int = Field(default=10, ge=1)
    workers: int = Field(default=64, ge=1)
    request_timeout: float = Field(default=10, gt=0)
    official_source_health: bool = True
    official_batch_size: int = Field(default=1100, ge=1)
    max_output_mb: float = Field(default=256, gt=0)
    websites: bool = True
    website_seed_index: bool = False
    gleif: bool = True
    procurement: bool = True
    state_aid: bool = True  # Stage S2 Støtteregisteret exact-beneficiary awards
    research: bool = True  # Stage S3 bundled RCN/SkatteFUNN exact-owner projects
    licences: bool = True  # Stage S4 Finanstilsynet exact-orgnr licences/registrations
    inspections: bool = True  # Stage S5 bundled Mattilsynet smilefjes inspections
    adaptive_websites: bool = True
    adaptive_extra_budget: bool = True
    dns_precheck: bool = True
    registry_declared: bool = False
    website_stop_after_verified: bool = True
    nav_rank_candidates: bool = True
    public_activity: bool = True
    registry_changes: bool = True
    website_request_cap: int = Field(default=8, ge=0, le=8)
    website_total_request_cap: int = Field(default=13, ge=0, le=13)
    website_politeness_seconds: float = Field(default=1, ge=1)
    website_user_agent: str = "SignalpostAgent/1.0 (+https://github.com/NethraVenkat/signalpost-agent)"
    hiring: bool = True
    nav_max_pages: int = Field(default=512,ge=0)
    nav_max_details: int | None = Field(default=None,ge=0)
    nav_time_cap_seconds: float | None = Field(default=None,gt=0)
    nav_lookback_days: int = Field(default=185,ge=1)
    nav_concurrency: int = Field(default=4, ge=1, le=12)
    nav_request_timeout: float = Field(default=30,gt=0)
    nav_body_cap_mb: float = Field(default=2,gt=0)
    nav_index_path: Path | None = None
    nav_index_max_age_days: float = Field(default=21,gt=0)
    prevent_system_sleep: bool = True
    search_max_queries: int | None = Field(default=None,ge=0)
    search_max_cost_usd: float = Field(default=5,ge=0)
    search_unit_price_usd: float = Field(default=.005,ge=0)
    synthesis: str = 'template'
    llm_max_calls: int = Field(default=100,ge=0)
    llm_max_cost_usd: float = Field(default=.50,ge=0)
    llm_timeout_seconds: float = Field(default=15,gt=0,le=15)
