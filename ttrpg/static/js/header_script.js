// static/js/script.js
document.addEventListener("DOMContentLoaded", function() {
  
  // From homepage.html, 'header.html' is in the same directory.
  // Electron is smart enough to handle this file request.
  fetch("header.html") 
    .then(response => {
      if (!response.ok) {
        throw new Error("Network response was not ok " + response.statusText);
      }
      return response.text();
    })
    .then(data => {
      document.getElementById("header-placeholder").innerHTML = data;
      setActiveLink();
    })
    .catch(error => {
      console.error('Error fetching header:', error);
      // Show an error to the user in the placeholder
      document.getElementById("header-placeholder").innerHTML = 
        "<p style='color:red;'>Error: Could not load header.</p>";
    });
});

function setActiveLink() {
  // Get the name of the current file (e.g., "homepage.html")
  const pathParts = window.location.pathname.split('/');
  const currentPageFile = pathParts.pop(); // Gets the last part of the path

  // Find all the nav links inside the header we just loaded
  const header = document.getElementById("header-placeholder");
  if (!header) return; // Safety check

  const navLinks = header.querySelectorAll(".nav-link");

  // Loop through each link
  navLinks.forEach(link => {
    // Get the file name from the link's href (e.g., "char_list.html")
    const linkFile = link.getAttribute('href').split('/').pop();

    // If the link's href matches the current page's file name...
    if (linkFile === currentPageFile) {
      link.classList.add("active");
      
      // Optional: Add 'active' to the parent <li> as well, if needed
      // link.parentElement.classList.add("active");
    }
  });
}
