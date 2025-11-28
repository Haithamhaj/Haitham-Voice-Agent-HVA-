"""
Model Router for HVA

Deterministically chooses the best model configuration (provider + logical_model_name + mode)
for each task based on structured metadata, NOT by asking another LLM.

Priority:
1. QUALITY and CORRECTNESS first
2. COST optimization (use cheaper logical models when safe)
3. Architecture alignment (Gemini for docs/analysis, GPT for planning/tools)
"""

from dataclasses import dataclass, field
from typing import Literal, Optional, Dict, Any


@dataclass
class TaskMeta:
    """
    Metadata describing the task, used as input to the model router.
    This struct MUST be stable and well-documented.
    """
    # Approximate number of tokens in the full input context
    context_tokens: int

    # High-level type of task
    task_type: Literal[
        "classification",      # simple labels/tags
        "tagging",
        "short_rewrite",
        "planning",            # execution plans, tool orchestration
        "tool_calling",
        "memory_op",           # save/query memory
        "email_reply",
        "doc_analysis",        # summarization / extraction from longer docs
        "translation",
        "comparison",
        "multi_step_reasoning",
        "other"
    ]

    # Risk level of the task
    risk: Literal["low", "medium", "high"]

    # Latency sensitivity:
    # - "interactive": user is waiting in voice/chat session
    # - "background": offline/batch processing
    latency: Literal["interactive", "background"]

    # Optional flags
    is_document: bool = False     # is this clearly a document-level task?
    is_multi_modal: bool = False  # text + image etc.

    # Extra hints (free-form metadata)
    extra: Optional[Dict[str, Any]] = field(default_factory=dict)


# Type alias for router result
RouterResult = Dict[str, str]


def choose_model(meta: TaskMeta) -> RouterResult:
    """
    Deterministically choose the best model for the given task meta.
    Priority: quality first, then cost.
    Must NOT call any LLM.
    
    Args:
        meta: TaskMeta instance describing the task
        
    Returns:
        RouterResult with keys: provider, model (logical name), mode, reason
    """
    
    # Rule 1: Long documents or very large context → Gemini
    if meta.is_document or meta.context_tokens > 20_000:
        return {
            "provider": "gemini",
            "model": "logical.doc-gemini",
            "mode": "default" if meta.latency == "interactive" else "flex",
            "reason": "Long document or very large context → use Gemini logical doc model."
        }
    
    # Rule 2: Document-level analysis/translation with larger context → Gemini
    if (meta.task_type in ["doc_analysis", "comparison", "translation"] 
        and meta.context_tokens > 8_000):
        return {
            "provider": "gemini",
            "model": "logical.doc-gemini",
            "mode": "default" if meta.latency == "interactive" else "flex",
            "reason": "Document-level analysis/translation with larger context → Gemini."
        }
    
    # Rule 3: Non-document tasks with normal context
    
    # Rule 3a: Simple, low-risk tasks → nano
    if (meta.task_type in ["classification", "tagging", "short_rewrite"] 
        and meta.risk == "low"):
        return {
            "provider": "openai",
            "model": "logical.nano",
            "mode": "batch+flex" if meta.latency == "background" else "default",
            "reason": "Simple, low-risk task; nano is sufficient and cheapest."
        }
    
    # Rule 3b: Simple but medium risk → nano-plus
    if (meta.task_type in ["classification", "tagging"] 
        and meta.risk == "medium"):
        return {
            "provider": "openai",
            "model": "logical.nano-plus",
            "mode": "batch+flex" if meta.latency == "background" else "default",
            "reason": "Simple but medium risk; nano-plus offers better reliability."
        }
    
    # Rule 3c: High-stakes or complex multi-step reasoning → premium
    # CHECK THIS BEFORE planning/tool_calling to catch high-risk variants
    if meta.task_type == "multi_step_reasoning" or meta.risk == "high":
        return {
            "provider": "openai",
            "model": "logical.premium",
            "mode": "default",
            "reason": "High-stakes or complex multi-step reasoning; use premium logical model."
        }
    
    # Rule 3d: Planning/tool calling/memory/email → mini (main workhorse)
    if meta.task_type in ["planning", "tool_calling", "memory_op", "email_reply"]:
        return {
            "provider": "openai",
            "model": "logical.mini",
            "mode": "default" if meta.latency == "interactive" else "flex",
            "reason": "Planning/tool calling/memory/email in HVA; logical.mini is main workhorse."
        }
    
    # Rule 4: Fallback for unknown task types
    return {
        "provider": "openai",
        "model": "logical.mini",
        "mode": "default",
        "reason": "Safe default: balanced quality and cost for unknown task type."
    }
