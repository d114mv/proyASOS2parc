from Simulacion.simulator import simulate


if __name__ == "__main__":
    processes = [
        {'arrival': 0, 'burst': 5, 'priority': 2},
        {'arrival': 1, 'burst': 3, 'priority': 1},
        {'arrival': 2, 'burst': 8, 'priority': 3},
        {'arrival': 3, 'burst': 6, 'priority': 2},
    ]
    res = simulate('RR', processes, rr_quantum=2, rr_context=1)
    print("Gantt:")
    for seg in res['gantt']:
        print(seg)
    print("\nSample ready_history (first 10):")
    for r in res['ready_history'][:20]:
        print(r)
    print("\nMetrics:")
    print(res['metrics'])
