from typing import Literal
from pydantic import Field,StrictInt
from .evidence import Model
from .states import Availability


class Sentence(Model):
    text: str
    claim_ids: list[str]
    value_kind: Literal['reported','derived'] = 'reported'
    count: StrictInt | None = None
    record_type: Literal['workplaces','board_members','active_ads'] | None = None
    observation_ids: list[str] = Field(default_factory=list)
    topic: Literal['activity','change','unknown','financial','takeaway'] | None = None
    formula: Literal['operating_margin','equity_ratio','revenue_yoy'] | None = None


class RunObservation(Model):
    id: str
    kind: str
    section: str
    data: dict


class FinancialMetric(Model):
    formula: Literal['operating_margin','equity_ratio','revenue_yoy']
    value: str
    unit: Literal['percent'] = 'percent'
    input_claim_ids: list[str]
    reporting_period: dict
    previous_period: dict | None = None
    carried_forward: bool = False


class Unknown(Model):
    family: str
    state: Availability
    reason: str
    field: str | None = None
    text: str | None = None


class TimelineEntry(Model):
    date: str
    precision: Literal['year','day','timestamp']
    text: str
    claim_ids: list[str]
    evidence_ids: list[str]
    source_field: str


class Sections(Model):
    timeline: list[TimelineEntry] = Field(default_factory=list)
    what_it_does: list[Sentence] = Field(default_factory=list)
    scale: list[Sentence] = Field(default_factory=list)
    leadership: list[Sentence] = Field(default_factory=list)
    changes: list[Sentence] = Field(default_factory=list)
    unknowns: list[Unknown] = Field(default_factory=list)
    limitations: list[Sentence] = Field(default_factory=list)
    takeaway: list[Sentence] = Field(default_factory=list)


class Checks(Model):
    sentences: int = 0
    cited: int = 0
    values_verified: bool = True
    fallback_used: bool = False
    dropped_sentences: int = 0
    rejections: list[dict[str,str]] = Field(default_factory=list)


class Generator(Model):
    name: str = 'template'
    version: str = '1'
    model: str | None = None
    prompt_version: str | None = None
    input_sha256: str


class ChangeClaim(Model):
    id: str
    field: str
    value: object
    evidence_ids: list[str]


class Synthesis(Model):
    mode: Literal['template','llm'] = 'template'
    language: Literal['en'] = 'en'
    summary: str = ''
    briefing: list[Sentence] = Field(default_factory=list)
    sections: Sections = Field(default_factory=Sections)
    checks: Checks = Field(default_factory=Checks)
    generator: Generator
    change_claims: list[ChangeClaim] = Field(default_factory=list)
    contract_version: Literal['r5-S'] | None = None
    observations: list[RunObservation] = Field(default_factory=list)
    financial_metrics: list[FinancialMetric] = Field(default_factory=list)
    financial_year_check: dict | None = None
