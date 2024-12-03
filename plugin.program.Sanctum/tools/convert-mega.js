function convertMegaLink() {
    const megaLink = document.getElementById('megaLink').value;
    const output = document.getElementById('megaOutput');

    if (!megaLink.includes("mega.nz")) {
        output.textContent = "Please enter a valid MEGA link.";
        return;
    }

    const fileID = megaLink.match(/\/file\/(.+?)#/);
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

    fetch(apiURL, {
        method: "POST",
        headers: { "Content-Type": "text/plain" },
        body: requestPayload
    })
    .then(response => response.json())
    .then(data => {
        if (data[0]?.g && data[0]?.n) {
            const directLink = data[0].g;
            const fileName = data[0].n;

            output.innerHTML = `
                <p>Direct Link: <a href="${directLink}" download="${fileName}">${fileName}</a></p>
            `;
        } else {
            output.textContent = "Failed to convert MEGA link or retrieve file metadata.";
        }
    })
    .catch(error => {
        console.error(error);
        output.textContent = "An error occurred while converting the link.";
    });
}
