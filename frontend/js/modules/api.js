function readCookie(name) {
  const match = document.cookie.match(
    new RegExp("(?:^|; )" + name + "=([^;]*)")
  );
  return match ? decodeURIComponent(match[1]) : "";
}

export async function apiRequest(path, options = {}) {
  const token = readCookie("bozg_csrf");
  const headers = Object.assign(
    {
      "Content-Type": "application/json",
      "X-CSRF-Token": token,
    },
    options.headers || {}
  );

  let response;
  try {
    response = await fetch(
      path,
      Object.assign({ credentials: "same-origin" }, options, { headers })
    );
  } catch (err) {
    throw new Error("Error de red. Revisa tu conexión.");
  }

  if (response.status === 401 || response.status === 403) {
    if (window.location.pathname.startsWith("/admin")) {
      window.location.href = "/admin/login?error=sin_permiso";
    }
    throw new Error("Sesión expirada o sin permisos.");
  }

  if (!response.ok) {
    let detail = "";
    try {
      const payload = await response.json();
      detail = payload.error || JSON.stringify(payload.errors || payload);
    } catch {
      detail = response.statusText;
    }
    throw new Error(detail || "Error " + response.status);
  }

  return response.json().catch(() => ({}));
}