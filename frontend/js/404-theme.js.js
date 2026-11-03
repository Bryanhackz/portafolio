// Sincroniza el tema claro/oscuro con la página principal.
document.addEventListener("DOMContentLoaded", () => {
  const savedTheme = localStorage.getItem("bzg-theme") || "dark";
  document.documentElement.setAttribute("data-theme", savedTheme);
});