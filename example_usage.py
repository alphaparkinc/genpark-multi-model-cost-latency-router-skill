from client import MultiModelCostLatencyRouterClient

def main():
    client = MultiModelCostLatencyRouterClient()
    res = client.route_query("Explain quantum entanglement and implement Bell state in Qiskit")
    print("=== Multi-Model Cost & Latency Router Output ===")
    print(f"Detected Intent: {res['detected_intent']}")
    print(f"Selected Model: {res['selected_model']} (Score: {res['composite_rank']})")
    print(f"Est. Latency: {res['estimated_latency_ms']}ms")
    print("\nAll Evaluated Models:")
    for c in res['pareto_candidates']:
        print(f"  - {c['model']:<18} | Rank: {c['composite_rank']} | Latency: {c['estimated_latency_ms']}ms | Cost: ${c['blended_cost_per_m']}/M")

if __name__ == '__main__':
    main()
