const processForm = document.getElementById("processForm");
const processTable = document.getElementById("processTable");
const clearBtn = document.getElementById("clearBtn");
const startBtn = document.getElementById("startBtn");

let processes = [];

processForm.addEventListener("submit", (e) => {
  e.preventDefault();

  const pid = document.getElementById("pid").value.trim();
  const arrival = parseInt(document.getElementById("arrival").value);
  const burst = parseInt(document.getElementById("burst").value);
  const priority = parseInt(document.getElementById("priority").value) || "-";

  processes.push({ pid, arrival, burst, priority });
  renderTable();
  processForm.reset();
});

function renderTable() {
  processTable.innerHTML = "";
  processes.forEach((p, index) => {
    const row = `
      <tr>
        <td class="border p-2">${p.pid}</td>
        <td class="border p-2">${p.arrival}</td>
        <td class="border p-2">${p.burst}</td>
        <td class="border p-2">${p.priority}</td>
        <td class="border p-2">
          <button onclick="removeProcess(${index})" class="bg-red-500 hover:bg-red-600 text-white px-3 py-1 rounded">Eliminar</button>
        </td>
      </tr>`;
    processTable.innerHTML += row;
  });
}

function removeProcess(index) {
  processes.splice(index, 1);
  renderTable();
}

clearBtn.addEventListener("click", () => {
  processes = [];
  renderTable();
});

startBtn.addEventListener("click", async () => {
  if (processes.length === 0) {
    alert("Debes ingresar al menos un proceso.");
    return;
  }

  const response = await fetch("/start", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(processes),
  });

  const data = await response.json();
  alert(data.message);
});
