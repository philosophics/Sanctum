<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dropbox Link Converter</title>
    <script>
        function convertDropboxLink() {
            let link = document.getElementById('dropboxLink').value;

            link = link.replace(/&/g, '&amp;');

            link = link.replace(/dl=0/, 'dl=1');

            document.getElementById('dropboxoutput').innerText = `Converted Link: ${link}`;
        }
    </script>
</head>
<body>
    <h1>Dropbox Link Converter</h1>

    <label for="dropboxLink">Enter Dropbox Link:</label>
    <input type="text" id="dropboxLink" placeholder="Enter Dropbox link" size="50">
    <button onclick="convertDropboxLink()">Convert Link</button>

    <h2>Converted Link:</h2>
    <p id="dropboxoutput"></p>
</body>
</html>
