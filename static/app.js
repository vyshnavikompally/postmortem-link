async function analyze() {
    const change = document.getElementById("change").value;
    const result = document.getElementById("result");

    if (!change.trim()) {
        result.innerHTML = `
            <div class="warning">
                <h2>Please enter a code change</h2>
            </div>
        `;
        return;
    }

    result.innerHTML = "<p>Searching Hindsight memory...</p>";

    try {
        const response = await fetch("/analyze", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                change: change
            })
        });

        const data = await response.json();

        if (!data.found) {
            result.innerHTML = `
                <div class="success">
                    <h2>✓ No Similar Incident Found</h2>
                    <p>${data.recommendation}</p>
                </div>
            `;
            return;
        }

        const memories = data.memories
            .map(memory => `<li>${memory}</li>`)
            .join("");

        result.innerHTML = `
            <div class="warning">
                <h2>⚠ Similar Historical Incidents Found</h2>

                <p>
                    <strong>Hindsight retrieved these memories:</strong>
                </p>

                <ul>
                    ${memories}
                </ul>

                <hr>

                <p>
                    <strong>Recommendation:</strong>
                    ${data.recommendation}
                </p>

                <small>
                    Memory retrieved from Hindsight
                </small>
            </div>
        `;
    } catch (error) {
        result.innerHTML = `
            <div class="warning">
                <h2>Something went wrong</h2>
                <p>${error.message}</p>
            </div>
        `;
    }
}