import { apiRequest } from "./api.js";

const projectList = document.getElementById("project-list");
const projectForm = document.getElementById("project-form");
const newButton = document.getElementById("new-project");
const cancelButton = document.getElementById("cancel-project");
const projectStatus = document.querySelector('[data-role="project-status"]');
const messageList = document.getElementById("message-list");
const refreshMessages = document.getElementById("refresh-messages");

function field(name) {
  return projectForm.querySelector(`[name="${name}"]`);
}

function setStatus(text, isError = false) {
  projectStatus.textContent = text;
  projectStatus.className = `form-status ${isError ? "text-red" : "text-green"}`;
}

function el(tag, props = {}, children = []) {
  const node = document.createElement(tag);
  for (const [k, v] of Object.entries(props)) {
    if (k === "text") node.textContent = v;
    else if (k === "className") node.className = v;
    else if (k === "style") node.setAttribute("style", v);
    else if (k.startsWith("on") && typeof v === "function") {
      node.addEventListener(k.slice(2).toLowerCase(), v);
    } else {
      node.setAttribute(k, v);
    }
  }
  for (const child of children) {
    node.append(
      child instanceof Node ? child : document.createTextNode(String(child))
    );
  }
  return node;
}

function openForm(project) {
  projectForm.hidden = false;
  field("id").value = project ? project.id : "";
  field("slug").value = project ? project.slug : "";
  field("title").value = project ? project.title : "";
  field("category").value = project ? project.category : "";
  field("challenge").value = project ? project.challenge : "";
  field("solution").value = project ? project.solution : "";
  field("result").value = project ? project.result : "";
  field("published").checked = project ? !!project.published : true;
  setStatus("");
  projectForm.scrollIntoView({ behavior: "smooth", block: "start" });
}

function closeForm() {
  projectForm.hidden = true;
  projectForm.reset();
  field("id").value = "";
}

function renderError(container, message) {
  container.innerHTML = "";
  container.append(el("li", { className: "item-error", text: message }));
}

async function loadProjects() {
  projectList.innerHTML = "";
  projectList.append(
    el("li", {}, [el("div", { className: "skeleton skeleton-title" })]),
    el("li", {}, [el("div", { className: "skeleton skeleton-title" })])
  );
  try {
    const data = await apiRequest("/api/admin/projects");
    projectList.innerHTML = "";
    (data.projects || []).forEach((project) => {
      const info = el("div", {}, [
        el("strong", { className: "text-blue", text: project.title }),
        el("br"),
        el("span", {
          className: "item-meta",
          text: `/${project.slug} | ${project.category} | ${
            project.published ? "ACTIVE" : "DRAFT"
          }`,
        }),
      ]);
      const actions = el("div", { style: "display:flex;gap:8px;" });
      const edit = el("button", {
        className: "btn btn-secondary btn-sm",
        text: "EDIT",
        onClick: () => openForm(project),
      });
      const remove = el("button", {
        className: "btn btn-primary btn-sm",
        text: "DEL",
        onClick: async () => {
          if (!confirm("¿CONFIRMAR BORRADO DE REGISTRO?")) return;
          try {
            await apiRequest(`/api/admin/projects/${project.id}`, {
              method: "DELETE",
            });
            await loadProjects();
          } catch (e) {
            setStatus(`> ERROR: ${e.message}`, true);
          }
        },
      });
      actions.append(edit, remove);
      projectList.append(el("li", {}, [info, actions]));
    });
  } catch (e) {
    renderError(projectList, `> ERROR: ${e.message}`);
  }
}

async function loadMessages() {
  messageList.innerHTML = "";
  messageList.append(
    el("li", {}, [el("div", { className: "skeleton skeleton-title" })]),
    el("li", {}, [el("div", { className: "skeleton skeleton-title" })])
  );
  try {
    const data = await apiRequest("/api/admin/messages");
    messageList.innerHTML = "";
    (data.messages || []).forEach((message) => {
      const info = el("div", {}, [
        el("strong", { className: "text-red", text: message.name }),
        " ",
        el("span", { className: "text-blue", text: `<${message.email}>` }),
        el("br"),
        el("span", {
          style: "font-size:0.9rem;color:var(--text-main);",
          text: message.body,
        }),
        el("br"),
        el("span", {
          className: "item-meta",
          text: `${message.created_at} | ${message.read ? "READ" : "UNREAD"}`,
        }),
      ]);
      const actions = el("div", { style: "display:flex;gap:8px;" });
      if (!message.read) {
        actions.append(
          el("button", {
            className: "btn btn-secondary btn-sm",
            text: "MARK_READ",
            onClick: async () => {
              try {
                await apiRequest(`/api/admin/messages/${message.id}/read`, {
                  method: "POST",
                });
                await loadMessages();
              } catch (e) {
                setStatus(`> ERROR: ${e.message}`, true);
              }
            },
          })
        );
      }
      actions.append(
        el("button", {
          className: "btn btn-primary btn-sm",
          text: "DEL",
          onClick: async () => {
            if (!confirm("¿CONFIRMAR BORRADO DE MENSAJE?")) return;
            try {
              await apiRequest(`/api/admin/messages/${message.id}`, {
                method: "DELETE",
              });
              await loadMessages();
            } catch (e) {
              setStatus(`> ERROR: ${e.message}`, true);
            }
          },
        })
      );
      messageList.append(el("li", {}, [info, actions]));
    });
  } catch (e) {
    renderError(messageList, `> ERROR: ${e.message}`);
  }
}

newButton.addEventListener("click", () => openForm(null));
cancelButton.addEventListener("click", closeForm);
refreshMessages.addEventListener("click", loadMessages);

projectForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const payload = {
    slug: field("slug").value.trim(),
    title: field("title").value.trim(),
    category: field("category").value.trim(),
    challenge: field("challenge").value.trim(),
    solution: field("solution").value.trim(),
    result: field("result").value.trim(),
    published: field("published").checked ? 1 : 0,
  };
  const id = field("id").value;
  try {
    if (id) {
      await apiRequest(`/api/admin/projects/${id}`, {
        method: "PUT",
        body: JSON.stringify(payload),
      });
    } else {
      await apiRequest("/api/admin/projects", {
        method: "POST",
        body: JSON.stringify(payload),
      });
    }
    setStatus("> REGISTRO GUARDADO CON ÉXITO");
    closeForm();
    await loadProjects();
  } catch (error) {
    setStatus(`> ERROR: ${error.message}`, true);
  }
});

loadProjects();
loadMessages();