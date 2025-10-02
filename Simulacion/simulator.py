"""
simulator.py

Motor de simulación para algoritmos de planificación:
- Prioridades (no preemptivo)
- FCFS
- SJF (no preemptivo)
- SRT (preemptivo)
- RR (Round Robin, preemptivo con quantum y opcional cambio de contexto)

Salida principal (por cada simulación):
{
  'gantt': [ {'pid': 'P1'|'CS'|'idle', 'start': 0, 'end': 3}, ... ],
  'ready_history': [ {'time': 0, 'ready': ['P2','P1'], 'running': 'P2'|'P1'|None}, ... ],
  'metrics': { 'P1': {'waiting_time': X, 'turnaround_time': Y}, ... , 'avg_waiting': Z, 'avg_turnaround': W }
}

Notas:
- Tiempos enteros (ticks = 1).
- Tie-breaker: menor arrival_time (si aplica), si persiste -> PID menor (P1, P2, ...).
- Prioridad: valor numérico menor = mayor prioridad (p.ej. 1 > 3).
- Context switch (CS) representado con pid = 'CS' en el Gantt (para que el frontend lo destaque).
"""

from copy import deepcopy
from collections import deque

class Process:
    def __init__(self, pid:int, arrival:int, burst:int, priority:int=None):
        self.pid = f'P{pid}'
        self.arrival = int(arrival)
        self.burst = int(burst)
        self.priority = priority if priority is None else int(priority)
        self.remaining = int(burst)
        # metrics placeholders
        self.start_time = None
        self.finish_time = None

    def __repr__(self):
        return f"<{self.pid} a={self.arrival} b={self.burst} pr={self.priority} rem={self.remaining}>"

def _calc_metrics(processes):
    metrics = {}
    total_wait = 0
    total_turn = 0
    n = len(processes)
    for p in processes:
        turnaround = p.finish_time - p.arrival
        waiting = turnaround - p.burst
        metrics[p.pid] = {'waiting_time': waiting, 'turnaround_time': turnaround}
        total_wait += waiting
        total_turn += turnaround
    metrics['avg_waiting'] = total_wait / n if n else 0
    metrics['avg_turnaround'] = total_turn / n if n else 0
    return metrics

def _snapshot(ready_q, running):
    return {'ready': [p.pid for p in ready_q], 'running': running.pid if running else None}

def simulate_fcfs(process_list):
    procs = [Process(i+1, p['arrival'], p['burst'], p.get('priority')) for i,p in enumerate(process_list)]
    procs.sort(key=lambda x: (x.arrival, int(x.pid[1:])))  # arrival then PID

    time = 0
    gantt = []
    ready_history = []
    completed = []
    queue = deque()
    idx = 0
    n = len(procs)

    while len(completed) < n:
        # add arrivals
        while idx < n and procs[idx].arrival <= time:
            queue.append(procs[idx])
            idx += 1

        running = None
        if queue:
            running = queue.popleft()
            if running.start_time is None:
                running.start_time = time
            # run to completion (non-preemptive)
            start = time
            end = time + running.remaining
            gantt.append({'pid': running.pid, 'start': start, 'end': end})
            # snapshots per tick (we'll append per tick for frontend)
            for t in range(start, end):
                # update arrivals in ticks inside the run (arrived processes go to ready)
                while idx < n and procs[idx].arrival <= t:
                    queue.append(procs[idx]); idx += 1
                ready_history.append({'time': t, 'ready': [p.pid for p in queue], 'running': running.pid})
            time = end
            running.remaining = 0
            running.finish_time = time
            completed.append(running)
        else:
            # idle until next arrival
            if idx < n:
                next_arr = procs[idx].arrival
                # represent idle time as idle blocks (useful for Gantt)
                if time < next_arr:
                    gantt.append({'pid': 'idle', 'start': time, 'end': next_arr})
                    for t in range(time, next_arr):
                        ready_history.append({'time': t, 'ready': [], 'running': None})
                    time = next_arr
            else:
                break

    metrics = _calc_metrics(completed)
    return {'gantt': gantt, 'ready_history': ready_history, 'metrics': metrics}

def simulate_sjf_nonpreemptive(process_list):
    procs = [Process(i+1, p['arrival'], p['burst'], p.get('priority')) for i,p in enumerate(process_list)]
    procs.sort(key=lambda x: (x.arrival, int(x.pid[1:])))
    time = 0
    gantt=[]
    ready_history=[]
    completed=[]
    idx=0
    n=len(procs)
    ready=[]

    while len(completed) < n:
        while idx < n and procs[idx].arrival <= time:
            ready.append(procs[idx]); idx+=1
        if ready:
            # choose shortest burst; tie-breaker: arrival then PID
            ready.sort(key=lambda x: (x.burst, x.arrival, int(x.pid[1:])))
            running = ready.pop(0)
            if running.start_time is None:
                running.start_time = time
            start = time
            end = time + running.remaining
            gantt.append({'pid': running.pid, 'start': start, 'end': end})
            for t in range(start, end):
                # add arrivals during run to ready
                while idx < n and procs[idx].arrival <= t:
                    ready.append(procs[idx]); idx+=1
                ready_history.append({'time': t, 'ready': [p.pid for p in ready], 'running': running.pid})
            time = end
            running.remaining=0
            running.finish_time=time
            completed.append(running)
        else:
            if idx < n:
                next_arr = procs[idx].arrival
                if time < next_arr:
                    gantt.append({'pid': 'idle', 'start': time, 'end': next_arr})
                    for t in range(time, next_arr):
                        ready_history.append({'time': t, 'ready': [], 'running': None})
                    time = next_arr
            else:
                break

    metrics = _calc_metrics(completed)
    return {'gantt': gantt, 'ready_history': ready_history, 'metrics': metrics}

def simulate_priority_nonpreemptive(process_list):
    # lower numeric = higher priority
    procs = [Process(i+1, p['arrival'], p['burst'], p.get('priority', 0)) for i,p in enumerate(process_list)]
    procs.sort(key=lambda x: (x.arrival, int(x.pid[1:])))
    time = 0
    gantt=[]
    ready_history=[]
    completed=[]
    idx=0
    n=len(procs)
    ready=[]

    while len(completed) < n:
        while idx < n and procs[idx].arrival <= time:
            ready.append(procs[idx]); idx+=1
        if ready:
            # choose highest priority (lowest number)
            ready.sort(key=lambda x: (x.priority, x.arrival, int(x.pid[1:])))
            running = ready.pop(0)
            if running.start_time is None:
                running.start_time = time
            start=time
            end=time+running.remaining
            gantt.append({'pid': running.pid, 'start': start, 'end': end})
            for t in range(start, end):
                while idx < n and procs[idx].arrival <= t:
                    ready.append(procs[idx]); idx+=1
                ready_history.append({'time': t, 'ready': [p.pid for p in ready], 'running': running.pid})
            time = end
            running.remaining = 0
            running.finish_time = time
            completed.append(running)
        else:
            if idx < n:
                next_arr = procs[idx].arrival
                if time < next_arr:
                    gantt.append({'pid': 'idle', 'start': time, 'end': next_arr})
                    for t in range(time, next_arr):
                        ready_history.append({'time': t, 'ready': [], 'running': None})
                    time = next_arr
            else:
                break

    metrics = _calc_metrics(completed)
    return {'gantt': gantt, 'ready_history': ready_history, 'metrics': metrics}

def simulate_srt_preemptive(process_list):
    # Shortest Remaining Time (preemptive SJF)
    procs = [Process(i+1, p['arrival'], p['burst'], p.get('priority')) for i,p in enumerate(process_list)]
    n=len(procs)
    procs.sort(key=lambda x: (x.arrival, int(x.pid[1:])))
    time=0
    idx=0
    ready=[]
    gantt=[]
    ready_history=[]
    completed=[]
    running=None
    last_pid = None

    while len(completed) < n:
        # add arrivals at this time
        while idx < n and procs[idx].arrival <= time:
            ready.append(procs[idx]); idx+=1
        # choose process with smallest remaining
        if running:
            # include running in ready for comparison
            candidates = ready + [running]
        else:
            candidates = ready[:]
        if candidates:
            candidates.sort(key=lambda x: (x.remaining, x.arrival, int(x.pid[1:])))
            chosen = candidates[0]
            # update ready / running sets
            if running and chosen.pid != running.pid:
                # preempt
                ready = [p for p in ready if p.pid != chosen.pid]
                ready.append(running)  # preempted goes to ready
                running = chosen
            elif not running:
                # start chosen
                ready = [p for p in ready if p.pid != chosen.pid]
                running = chosen

            # run one tick
            if running.start_time is None:
                running.start_time = time
            # For building gantt, coalesce consecutive ticks of same running pid later
            # Update ready_history for this tick
            ready_history.append({'time': time, 'ready': [p.pid for p in ready], 'running': running.pid})
            running.remaining -= 1
            last_pid = running.pid
            # check if completes
            if running.remaining == 0:
                running.finish_time = time + 1
                completed.append(running)
                running = None
            time += 1
        else:
            # idle
            # advance to next arrival
            if idx < n:
                next_arr = procs[idx].arrival
                for t in range(time, next_arr):
                    gantt.append({'pid': 'idle', 'start': t, 'end': t+1})
                    ready_history.append({'time': t, 'ready': [], 'running': None})
                time = next_arr
            else:
                break

    # Convert tickwise ready_history & running ticks into coalesced gantt
    # We'll produce gantt by scanning ready_history
    i = 0
    L = len(ready_history)
    while i < L:
        r = ready_history[i]
        pid = r['running'] if r['running'] else 'idle'
        start = r['time']
        j = i+1
        while j < L and ready_history[j]['running'] == r['running']:
            j += 1
        end = ready_history[j-1]['time'] + 1
        gantt.append({'pid': pid, 'start': start, 'end': end})
        i = j

    metrics = _calc_metrics(completed)
    return {'gantt': gantt, 'ready_history': ready_history, 'metrics': metrics}

def simulate_rr(process_list, quantum:int, context_switch:int=0):
    """
    Round Robin simulation.
    - quantum: integer > 0
    - context_switch: integer >= 0 (time units for a context switch). If 0, no explicit CS delay.
    Behavior:
    - At a quantum expiry (or when a process finishes earlier), if a different process runs next and context_switch > 0,
      we insert a 'CS' block of length context_switch in the Gantt.
    - Ready queue follows FIFO for RR; arrivals during execution are appended to queue.
    """
    if quantum <= 0:
        raise ValueError("Quantum must be > 0")

    procs = [Process(i+1, p['arrival'], p['burst'], p.get('priority')) for i,p in enumerate(process_list)]
    procs.sort(key=lambda x: (x.arrival, int(x.pid[1:])))
    n = len(procs)
    idx = 0
    time = 0
    queue = deque()
    gantt = []
    ready_history = []
    completed = []
    running = None
    last_running_pid = None

    while len(completed) < n:
        # enqueue arrivals at current time
        while idx < n and procs[idx].arrival <= time:
            queue.append(procs[idx]); idx += 1

        if not running and queue:
            running = queue.popleft()

        if running:
            if running.start_time is None:
                running.start_time = time
            # execute up to quantum or remaining, but allow arrival handling per tick
            run_len = min(quantum, running.remaining)
            # run tick-by-tick to capture arrivals
            for t in range(run_len):
                # before executing this tick, append arrivals that happen exactly at 'time'
                while idx < n and procs[idx].arrival <= time:
                    queue.append(procs[idx]); idx += 1
                ready_history.append({'time': time, 'ready': [p.pid for p in queue], 'running': running.pid})
                running.remaining -= 1
                time += 1
                if running.remaining == 0:
                    running.finish_time = time
                    completed.append(running)
                    break

            # if process finished within its quantum
            if running.remaining == 0:
                # choose next process (if any)
                prev_pid = running.pid
                running = None
                if queue:
                    # context switch before next runs if context_switch>0
                    if context_switch > 0:
                        # insert CS block
                        cs_start = time
                        cs_end = time + context_switch
                        gantt.append({'pid': 'CS', 'start': cs_start, 'end': cs_end})
                        # record ready_history during CS (running = None)
                        for tt in range(cs_start, cs_end):
                            # arrivals during CS
                            while idx < n and procs[idx].arrival <= tt:
                                queue.append(procs[idx]); idx += 1
                            ready_history.append({'time': tt, 'ready': [p.pid for p in queue], 'running': None})
                        time = cs_end
                    # next will be popped at next loop iteration
                    running = queue.popleft()
                else:
                    # no one ready: loop will advance to next arrival / idle
                    pass
            else:
                # quantum expired, process not finished -> requeue
                queue.append(running)
                prev_pid = running.pid
                running = None
                # context switch if there is someone else to run next
                if queue:
                    if context_switch > 0:
                        cs_start = time
                        cs_end = time + context_switch
                        gantt.append({'pid': 'CS', 'start': cs_start, 'end': cs_end})
                        for tt in range(cs_start, cs_end):
                            while idx < n and procs[idx].arrival <= tt:
                                queue.append(procs[idx]); idx += 1
                            ready_history.append({'time': tt, 'ready': [p.pid for p in queue], 'running': None})
                        time = cs_end
                    # next process will be popped in next iteration
                else:
                    # nothing to run; loop will advance to next arrival / idle
                    pass
        else:
            # CPU idle: advance to next arrival
            if idx < n:
                next_arr = procs[idx].arrival
                if time < next_arr:
                    gantt.append({'pid': 'idle', 'start': time, 'end': next_arr})
                    for t in range(time, next_arr):
                        ready_history.append({'time': t, 'ready': [p.pid for p in queue], 'running': None})
                    time = next_arr
                # next iteration will enqueue arrivals
            else:
                break

    # coalesce gantt: build from ready_history and explicit CS/idle entries
    # Start by appending intervals for running pids using ready_history
    # We'll scan ready_history to create contiguous blocks of same running pid
    i = 0
    L = len(ready_history)
    while i < L:
        r = ready_history[i]
        pid = r['running'] if r['running'] else 'idle'
        start = r['time']
        j = i+1
        while j < L and ready_history[j]['running'] == r['running']:
            j += 1
        end = ready_history[j-1]['time'] + 1
        gantt.append({'pid': pid, 'start': start, 'end': end})
        i = j

    # Note: We already appended CS blocks into gantt as we simulated (so ordering may need sorting/merging)
    # Sort gantt by start time and merge overlapping/adjacent same-pid blocks
    gantt.sort(key=lambda x: x['start'])
    merged = []
    for seg in gantt:
        if not merged:
            merged.append(seg.copy())
        else:
            last = merged[-1]
            if seg['pid'] == last['pid'] and seg['start'] == last['end']:
                last['end'] = seg['end']
            else:
                # if overlapping (shouldn't happen) we still append
                merged.append(seg.copy())
    gantt = merged

    metrics = _calc_metrics([p for p in procs if p.finish_time is not None])
    return {'gantt': gantt, 'ready_history': ready_history, 'metrics': metrics}

# Convenience dispatcher
def simulate(algorithm:str, processes:list, rr_quantum:int=None, rr_context:int=0):
    """
    algorithm: 'FCFS', 'SJF', 'SRT', 'PRIORITY', 'RR'
    processes: list of dicts: [{'arrival': int, 'burst': int, 'priority': int (optional)}...]
    For RR supply rr_quantum (int) and optionally rr_context (int).
    """
    alg = algorithm.strip().upper()
    if alg == 'FCFS':
        return simulate_fcfs(processes)
    elif alg == 'SJF':
        return simulate_sjf_nonpreemptive(processes)
    elif alg == 'PRIORITY':
        return simulate_priority_nonpreemptive(processes)
    elif alg == 'SRT':
        return simulate_srt_preemptive(processes)
    elif alg == 'RR':
        if rr_quantum is None:
            raise ValueError("RR requires rr_quantum parameter")
        return simulate_rr(processes, quantum=rr_quantum, context_switch=rr_context)
    else:
        raise ValueError("Algorithm not recognized")
    
class Simulator:
    def __init__(self, processes, algorithm, quantum=None, context_switch=0):
        """
        processes: lista de diccionarios [{pid, arrival, burst, priority}, ...]
        algorithm: string (FCFS, SJF, SRT, RR, PRIORITY)
        quantum: entero (solo RR)
        context_switch: entero (tiempo de cambio de contexto)
        """
        self.processes = [
            {
                "pid": p["pid"],
                "arrival": int(p["arrival"]),
                "burst": int(p["burst"]),
                "priority": int(p.get("priority", 0)),
                "remaining": int(p["burst"]),
                "start": None,
                "finish": None,
                "waiting": 0,
                "turnaround": 0
            }
            for p in processes
        ]
        self.algorithm = algorithm.upper()
        self.quantum = quantum
        self.context_switch = context_switch
        self.timeline = []
        self.time = 0

    def run_step_by_step(self):
        """
        Generador que emite tick por tick.
        Cada yield devuelve un diccionario:
        {
            "tick": t,
            "current_process": "P1",
            "ready_queue": ["P2","P3"]
        }
        """
        ready_queue = []
        running_process = None
        quantum_counter = 0

        while True:
            # Ingresan procesos nuevos a la cola
            for p in self.processes:
                if p["arrival"] == self.time:
                    ready_queue.append(p)

            # Si no hay proceso corriendo, elegir uno según algoritmo
            if not running_process and ready_queue:
                if self.algorithm == "FCFS":
                    ready_queue.sort(key=lambda x: (x["arrival"], x["pid"]))
                elif self.algorithm == "SJF":
                    ready_queue.sort(key=lambda x: (x["burst"], x["arrival"], x["pid"]))
                elif self.algorithm == "SRT":
                    ready_queue.sort(key=lambda x: (x["remaining"], x["arrival"], x["pid"]))
                elif self.algorithm == "PRIORITY":
                    ready_queue.sort(key=lambda x: (x["priority"], x["arrival"], x["pid"]))
                elif self.algorithm == "RR":
                    pass  # RR maneja quantum más abajo

                running_process = ready_queue.pop(0)
                if running_process["start"] is None:
                    running_process["start"] = self.time
                quantum_counter = self.quantum if self.algorithm == "RR" else None

            # Avanzar CPU
            if running_process:
                running_process["remaining"] -= 1
                self.timeline.append(running_process["pid"])
                quantum_counter = quantum_counter - 1 if quantum_counter else None

                # Proceso terminado
                if running_process["remaining"] == 0:
                    running_process["finish"] = self.time + 1
                    running_process = None
                    if self.context_switch > 0:
                        for _ in range(self.context_switch):
                            self.time += 1
                            self.timeline.append("CS")
                            yield {
                                "tick": self.time,
                                "current_process": "CS",
                                "ready_queue": [p["pid"] for p in ready_queue]
                            }

                # Round Robin → si expira quantum
                elif self.algorithm == "RR" and quantum_counter == 0:
                    ready_queue.append(running_process)
                    running_process = None
                    if self.context_switch > 0:
                        for _ in range(self.context_switch):
                            self.time += 1
                            self.timeline.append("CS")
                            yield {
                                "tick": self.time,
                                "current_process": "CS",
                                "ready_queue": [p["pid"] for p in ready_queue]
                            }

            else:
                # CPU ociosa
                self.timeline.append("IDLE")

            # Emitimos tick actual
            yield {
                "tick": self.time,
                "current_process": running_process["pid"] if running_process else "IDLE",
                "ready_queue": [p["pid"] for p in ready_queue]
            }

            # Condición de salida: todos terminaron
            if all(p["remaining"] == 0 for p in self.processes):
                break

            self.time += 1

    def get_results(self):
        """
        Calcula métricas finales: waiting time y turnaround
        """
        for p in self.processes:
            p["turnaround"] = p["finish"] - p["arrival"]
            p["waiting"] = p["turnaround"] - p["burst"]

        return [
            {"pid": p["pid"], "waiting_time": p["waiting"], "turnaround_time": p["turnaround"]}
            for p in self.processes
        ]