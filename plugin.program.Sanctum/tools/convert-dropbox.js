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
