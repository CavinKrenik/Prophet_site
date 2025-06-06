// router.js - Basic SPA Router
// Handles hash-based routing for single-page navigation

document.addEventListener("DOMContentLoaded", () => {
  const routes = {
    "#dashboard": "index.html",
    "#logs": "logs.html",
    "#analytics": "analytics.html"
  };

  function navigateTo(route) {
    const path = routes[route] || "index.html";
    window.location.href = path;
  }

  const navLinks = document.querySelectorAll("#menu a[href^='#']");
  navLinks.forEach(link => {
    link.addEventListener("click", (e) => {
      e.preventDefault();
      const hash = link.getAttribute("href");
      navigateTo(hash);
    });
  });

  if (window.location.hash && routes[window.location.hash]) {
    navigateTo(window.location.hash);
  }
});
