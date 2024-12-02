async function fetchMegaLink(url) {
    const fileID = url.match(/file\/(.+?)#/)[1];
    const apiURL = "https://eu.api.mega.co.nz/cs";
    const body = JSON.stringify([{
        a: "g",
        g: 1,
        ssl: 0,
        p: fileID
    }]);

    try {
        const response = await fetch(apiURL, {
            method: "POST",
            headers: {
                "Content-Type": "text/plain;charset=UTF-8",
            },
            body: body
        });
        const result = await response.json();
        const directLink = result[0]?.g;
        const fileSize = result[0]?.s;
        if (directLink) {
            console.log(`Direct URL: ${directLink}`);
            console.log(`File Size: ${fileSize} bytes`);
        } else {
            console.error("Failed to generate a direct link.");
        }
    } catch (error) {
        console.error("Error:", error);
    }
}

// Example usage:
fetchMegaLink("https://mega.nz/file/uYclAS7J#zK5hpLs2uXEYgWxfpqGtOAxwvBZ97GyWHKwYdxsDLSs");
