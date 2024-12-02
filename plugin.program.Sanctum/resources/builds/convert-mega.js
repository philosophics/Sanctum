function convertMegaLink() {
    const megaLink = document.getElementById('megaLink').value; // Get input link
    const output = document.getElementById('output'); // Get the output element

    if (!megaLink.includes("mega.nz")) {
        output.textContent = "Please enter a valid MEGA link.";
        return;
    }

    const fileID = megaLink.match(/\/file\/(.+?)#/); // Extract file ID from the link
    if (!fileID) {
        output.textContent = "Invalid MEGA link format.";
        return;
    }

    const apiURL = "https://eu.api.mega.co.nz/cs";
    const requestPayload = JSON.stringify([{
        a: "g",
        g: 1,
        ssl: 0,
        p: fileID[1]
    }]);

    // Make the API call
    fetch(apiURL, {
        method: "POST",
        headers: { "Content-Type": "text/plain" },
        body: requestPayload
    })
    .then(response => response.json())
    .then(data => {
        if (data[0]?.g) {
            output.textContent = `Direct Link: ${data[0].g}`;
        } else {
            output.textContent = "Failed to convert MEGA link.";
        }
    })
    .catch(error => {
        console.error(error);
        output.textContent = "An error occurred while converting the link.";
    });
}
