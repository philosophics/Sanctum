function fetchMD5(event) {
    event.preventDefault();
    const md5Content = document.getElementById('md5-content');
    md5Content.style.display = 'block';
    md5Content.textContent = 'Loading...';

    fetch('/lib/addons.xml.md5')
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.text();
        })
        .then(data => {
            md5Content.textContent = data;
        })
        .catch(error => {
            md5Content.textContent = `Error loading file: ${error}`;
        });
}
function loadRandomLogo() {
    const logosDir = "lib/resources/images/logos/";
    const logoFiles = ["logo1.png", "logo2.png", "logo3.png", "logo4.png", "logo5.png"];

    // Select a random logo from the array
    const randomLogo = logoFiles[Math.floor(Math.random() * logoFiles.length)];

    // Update the logo's src attribute
    const logoElement = document.getElementById("site-logo");
    logoElement.src = logosDir + randomLogo;
}

// Run the function when the page loads
window.onload = loadRandomLogo;
