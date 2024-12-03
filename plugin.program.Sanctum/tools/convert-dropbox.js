<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dropbox Link Converter</title>
    <script>
        function convertDropboxLink() {
            console.log("Function called");
            let link = document.getElementById('dropboxLink').value;
            console.log("Original Link:", link);

            link = link.replace(/&/g, '&amp;');
            console.log("After replacing '&':", link);

            link = link.replace(/dl=0/, 'dl=1');
            console.log("After replacing 'dl=0':", link);

            document.getElementById('dropboxoutput').innerText = `Converted Link: ${link}`;
            console.log("Output updated");
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
