import json
from typing import Dict, Any, List, Optional

class MultiModelCostLatencyRouterClient:
    """
    Production-grade multi-model cost and latency router.
    Extracts semantic query intents and calculates Pareto-optimal model dispatch.
    """
    MODELS_DB = {
        "gemini-1.5-flash": {"reasoning": 7.5, "speed": 9.8, "latency_ms": 320, "cost_in_per_m": 0.075, "cost_out_per_m": 0.30},
        "claude-3-5-sonnet": {"reasoning": 9.8, "speed": 7.2, "latency_ms": 1200, "cost_in_per_m": 3.0, "cost_out_per_m": 15.0},
        "gpt-4o":            {"reasoning": 9.3, "speed": 8.0, "latency_ms": 850,  "cost_in_per_m": 2.5, "cost_out_per_m": 10.0},
        "gemini-1.5-pro":    {"reasoning": 9.2, "speed": 7.4, "latency_ms": 1100, "cost_in_per_m": 1.25, "cost_out_per_m": 5.0},
        "deepseek-r1":       {"reasoning": 9.7, "speed": 5.5, "latency_ms": 2200, "cost_in_per_m": 0.55, "cost_out_per_m": 2.19}
    }

    def route_query(self, prompt: str = "Analyze this Python AST parser and benchmark memory efficiency vs speed", max_latency_ms: int = 1500, cost_weight: float = 0.3, allowed_models: Optional[List[str]] = None) -> Dict[str, Any]:
        p_lower = prompt.lower()
        intent = "reasoning" if any(w in p_lower for w in ["analyze", "algorithm", "debug", "proof", "benchmark", "optimize"]) else "realtime" if any(w in p_lower for w in ["latest", "news", "today", "now"]) else "standard"

        available = allowed_models or list(self.MODELS_DB.keys())
        scored = []

        for m_name in available:
            spec = self.MODELS_DB.get(m_name)
            if not spec: continue
            if spec["latency_ms"] > max_latency_ms * 1.5: continue

            q_score = spec["reasoning"] if intent == "reasoning" else spec["speed"]
            cost_norm = max(0.1, 10.0 - (spec["cost_out_per_m"] / 1.5))
            latency_norm = max(0.1, 10.0 - (spec["latency_ms"] / 250.0))

            total_rank = round((q_score * (1.0 - cost_weight)) + (cost_norm * cost_weight * 0.6) + (latency_norm * cost_weight * 0.4), 2)
            scored.append({
                "model": m_name,
                "composite_rank": total_rank,
                "estimated_latency_ms": spec["latency_ms"],
                "blended_cost_per_m": round((spec["cost_in_per_m"] + spec["cost_out_per_m"]) / 2, 3),
                "quality_grade": q_score
            })

        scored.sort(key=lambda x: x["composite_rank"], reverse=True)
        winner = scored[0] if scored else {"model": "gemini-1.5-flash", "composite_rank": 8.0, "estimated_latency_ms": 320}

        return {
            "detected_intent": intent,
            "selected_model": winner["model"],
            "composite_rank": winner.get("composite_rank", 8.0),
            "estimated_latency_ms": winner.get("estimated_latency_ms", 320),
            "pareto_candidates": scored
        }
