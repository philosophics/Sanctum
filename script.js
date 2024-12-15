function fetchMD5(event) {
  event.preventDefault(); // Prevent default link behavior

  const md5Content = document.getElementById("md5-content");

  // Reset content and show loading message
  md5Content.classList.remove("hidden");
  md5Content.classList.add("file-content");
  md5Content.textContent = "Loading...";

  // Fetch the MD5 file
  fetch("./lib/addons.xml.md5")
    .then((response) => {
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
      return response.text(); // Return the file content as text
    })
    .then((data) => {
      md5Content.textContent = data; // Display the file content
    })
    .catch((error) => {
      md5Content.textContent = `Error loading file: ${error}`; // Show error
    });
}

function loadRandomLogo() {
  const logosDir = "lib/resources/images/logos/";
  const logoFiles = [
    "logo1.png",
    "logo2.png",
    "logo3.png",
    "logo4.png",
    "logo5.png",
  ];

  // Select a random logo from the array
  const randomLogo = logoFiles[Math.floor(Math.random() * logoFiles.length)];

  // Update the logo's src attribute
  const logoElement = document.getElementById("site-logo");
  logoElement.src = logosDir + randomLogo;
}

// Run the function when the page loads
window.onload = loadRandomLogo;

// Check if the browser supports Service Workers
if ("serviceWorker" in navigator) {
  // Register the Service Worker
  navigator.serviceWorker
    .register("/service-worker.js")
    .then((registration) => {
      console.log("Service Worker registered with scope:", registration.scope);
    })
    .catch((error) => {
      console.error("Service Worker registration failed:", error);
    });
}
