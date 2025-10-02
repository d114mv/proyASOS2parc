const socket = io();

function startSimulation() {
    const algorithm = document.getElementById("algorithm").value;
    const quantum = document.getElementById("quantum").value;
    const contextSwitch = document.getElementById("context_switch").value;

    // TODO: capturar procesos desde un formulario dinámico
    const processes = [
        { pid: "P1", arrival: 0, burst: 5, priority: 2 },
        { pid: "P2", arrival: 1, burst: 3, priority: 1 }
    ];

    socket.emit("start_simulation", {
        algorithm,
        processes,
        quantum: quantum ? parseInt(quantum) : null,
        context_switch: contextSwitch ? parseInt(contextSwitch) : 0
    });
}

// Recibimos actualizaciones paso a paso
socket.on("simulation_update", (data) => {
    console.log("Tick:", data);

    // Actualizar diagrama de Gantt
    const timeline = document.getElementById("timeline");
    const block = document.createElement("div");
    block.className = "gantt-block";
    block.textContent = data.current_process || "CS"; // CS = context switch
    timeline.appendChild(block);

    // Actualizar cola de listos
    const queue = document.getElementById("ready_queue");
    queue.innerHTML = "";
    data.ready_queue.forEach(p => {
        const li = document.createElement("li");
        li.textContent = p;
        queue.appendChild(li);
    });
});

// Al terminar mostramos resultados finales
socket.on("simulation_finished", (results) => {
    console.log("Resultados:", results);

    const tbody = document.querySelector("#result_table tbody");
    tbody.innerHTML = "";
    results.forEach(r => {
        const row = `<tr>
            <td>${r.pid}</td>
            <td>${r.waiting_time}</td>
            <td>${r.turnaround_time}</td>
        </tr>`;
        tbody.innerHTML += row;
    });
});
