function loadRandomLogo() {
  const logosDir = "../lib/resources/images/logos/";
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
