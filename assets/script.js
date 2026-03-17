function fetchMD5(event) {
  event.preventDefault();

  const md5Content = document.getElementById("md5-content");

  md5Content.classList.remove("hidden");
  md5Content.classList.add("file-content");
  md5Content.textContent = "Loading...";

  fetch("./lib/addons.xml.md5")
    .then((response) => {
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
      return response.text();
    })
    .then((data) => {
      md5Content.textContent = data;
    })
    .catch((error) => {
      md5Content.textContent = `Error loading file: ${error}`;
    });
}

function loadRandomLogo() {
  const logoElement = document.getElementById("site-logo");
  if (!logoElement) return;

  const logoFiles = ["logo1.png", "logo2.png", "logo3.png", "logo4.png", "logo5.png"];
  const randomLogo = logoFiles[Math.floor(Math.random() * logoFiles.length)];

  const currentURL = window.location.href;
  const isSubfolder = currentURL.includes("/repo/") || currentURL.includes("/lib/");

  const prefix = isSubfolder ? "../" : "";
  const logosDir = prefix + "lib/resources/images/logos/";

  logoElement.src = logosDir + randomLogo;

  console.log("Detecting Subfolder:", isSubfolder);
  console.log("Final Logo Path:", logoElement.src);
}

window.onload = loadRandomLogo;

if ("serviceWorker" in navigator) {
  navigator.serviceWorker
    .register("/service-worker.js", { scope: "/" })
    .then((registration) => {
      console.log("Service Worker registered with scope:", registration.scope);
    })
    .catch((error) => {
      console.error("Service Worker registration failed:", error);
    });
}
