<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dropbox Link Converter</title>
    <script>
        // Function to convert the Dropbox link
        function convertDropboxLink() {
            // Get the link from the input field
            let link = document.getElementById('dropboxLink').value;

            // Replace '&' with '&amp;'
            link = link.replace(/&/g, '&amp;');

            // Replace 'dl=0' with 'dl=1' (to force download)
            link = link.replace(/dl=0/, 'dl=1');

            // Display the converted link in the result field
            document.getElementById('dropboxOutput').innerText = `Converted Link: ${convertedLink}`;
        }
    </script>
</head>
<body>
    <h1>Dropbox Link Converter</h1>

    <label for="dropboxLink">Enter Dropbox Link:</label>
    <input type="text" id="dropboxLink" placeholder="Enter Dropbox link" size="50">
    <button onclick="convertDropboxLink()">Convert Link</button>

    <h2>Converted Link:</h2>
    <textarea id="result" rows="4" cols="50" readonly></textarea>
</body>
</html>
