function get_hash() {
    const value = document.getElementById('inputValue').value;

    if (!value) {
        alert("Please enter a Value first!");
        return;
    }

    fetch(`/get_hash?value=${encodeURIComponent(value)}`, {method: "GET",})
    .then(response => {
        if (!response.ok) {
            throw new Error("API error")
        }
        return response.json()
    })
    .then(data => {
        document.getElementById('hashResult').textContent = 'Hash: ' + data.hash;
    })
    .catch(error => {
        console.error("Error: ", error);
        document.getElementById('hashResult').textContent = "Error. Check console in you Browser (type F12, then go to console tab)"
    });
}