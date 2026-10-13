from ..models.synthesis import Synthesis,Generator,Unknown
from ..models.evidence import digest
from .template import generate
from .provider import configured_provider,PRICE_TABLE
from .llm import messages,render,PROMPT_VERSION
from .validate import validate_synthesis
import asyncio,json,time


class Service:
    def __init__(self,config,budget=None,provider=None):
        self.config,self.budget,self.provider=config,budget,provider or configured_provider()
        self.called=set()
        self.metrics={'calls':0,'cache_hits':0,'input_tokens':0,'output_tokens':0,'estimated_usd':0,'fallbacks':0}

    async def summarize(self,envelope):
        try:base=generate(envelope)
        except Exception:
            result=Synthesis(generator=Generator(input_sha256=digest([envelope.organisation_number,'template_error'])))
            result.checks.fallback_used=True
            result.checks.rejections=[{'section':'synthesis','reason':'template_generation_error'}]
            result.sections.unknowns=[Unknown(family='synthesis',state='failed',reason='Summary generation could not be completed; source results remain available.')]
            self.metrics['fallbacks']+=1
            return result
        if self.config.synthesis=='template':return base
        if self.provider is None:
            if self.config.synthesis=='llm':return self.fallback(base,'provider_not_configured')
            return base
        if not any(getattr(base.sections,key) for key in ('what_it_does','scale','leadership')):return base
        cache=None
        try:
            request,specs=messages(base,envelope)
            model=self.provider.model
            if model not in PRICE_TABLE:raise ValueError('price_not_configured')
            key=digest([model,PROMPT_VERSION,request,base.generator.input_sha256])
            cache=self.config.state_dir/'llm-cache'/key
            if cache.exists():
                saved=json.loads(cache.read_text(encoding='utf8'))
                self.metrics['cache_hits']+=1
                if 'fallback' in saved:return self.fallback(base,saved['fallback'])
                result=render(saved['text'],base,envelope,specs)
            else:
                prices=PRICE_TABLE[model];bound=(2000*prices[0]+500*prices[1])/1_000_000
                cap=min(self.config.llm_max_cost_usd,self.config.max_cost_usd)
                if len(self.called)>=self.config.llm_max_calls or envelope.organisation_number in self.called:raise ValueError('call_cap')
                if self.metrics['estimated_usd']+bound>cap:raise ValueError('cost_cap')
                timeout=self.config.llm_timeout_seconds
                if self.budget:
                    self.budget.check();timeout=min(timeout,self.budget.deadline-time.monotonic())
                self.called.add(envelope.organisation_number);self.metrics['calls']+=1
                self.metrics['estimated_usd']+=bound
                async with asyncio.timeout(timeout):reply=await self.provider.complete(request,500)
                if reply.input_tokens<0 or reply.output_tokens<0:raise ValueError('invalid_usage')
                actual=(reply.input_tokens*prices[0]+reply.output_tokens*prices[1])/1_000_000
                self.metrics['estimated_usd']+=actual-bound
                self.metrics['input_tokens']+=reply.input_tokens;self.metrics['output_tokens']+=reply.output_tokens
                if reply.input_tokens>2000 or reply.output_tokens>500:raise ValueError('token_cap')
                result=render(reply.text,base,envelope,specs)
                cache.parent.mkdir(parents=True,exist_ok=True)
                cache.write_text(json.dumps({'text':reply.text}),encoding='utf8')
            result.mode='llm';result.generator.name=self.provider.name
            result.generator.model=model;result.generator.prompt_version=PROMPT_VERSION
            return validate_synthesis(result,envelope)
        except Exception as exc:
            reason=str(exc) if isinstance(exc,ValueError) and str(exc) in {'input_cap','price_not_configured','call_cap','cost_cap','invalid_usage','token_cap','invalid_model_json','too_many_sentences','invalid_model_sentence','unapproved_frame_or_raw_value','missing_or_misbound_claim','duplicate_model_sentence','empty_model_summary'} else type(exc).__name__
            if cache is not None and envelope.organisation_number in self.called:
                try:
                    cache.parent.mkdir(parents=True,exist_ok=True);cache.write_text(json.dumps({'fallback':reason}),encoding='utf8')
                except OSError:pass
            return self.fallback(base,reason)

    def fallback(self,base,reason):
        base.checks.fallback_used=True
        base.checks.rejections.append({'section':'llm','reason':reason})
        if reason in {'unapproved_frame_or_raw_value','missing_or_misbound_claim','invalid_model_sentence'}:base.checks.dropped_sentences+=1
        self.metrics['fallbacks']+=1
        return base
