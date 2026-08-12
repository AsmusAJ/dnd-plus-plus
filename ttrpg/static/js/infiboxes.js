if (userOwnsPage) {
  const textElements = document.getElementsByClassName("text");
  for (let i = 0; i < textElements.length; i++) {
    textElements[i].contentEditable = true;
  }
  const headerElements = document.getElementsByClassName("header");
  for (let i = 0; i < headerElements.length; i++) {
    headerElements[i].contentEditable = true;
  }
  document.getElementById("title").contentEditable = true;
}

function newBox() {
  // Add to database
  let pageId = document.getElementById("add-card").getAttribute("page-id");
  const payload = {
    page_id: pageId,
  };

  fetch("/api/v1/create_box", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
    credentials: "include",
  })
    .then((response) => response.json())
    .then((data) => {
      const boxId = data.box_id;
      const newBox = document.createElement("div");

      newBox.className = "card";

      // ADD 'two-col' CLASS IF IN TWO COLUMN MODE
      const container = document.getElementById("flexContainer");
      if (container.classList.contains("flex-row")) {
        newBox.classList.add("two-col");
      }

      newBox.innerHTML = `
                    <div class="card-header d-flex justify-content-between align-items-center">
                        <h5 class="mb-0 pt-2 pb-2 header" box-id="${boxId}" box-title="Add Title">Add Title</h5>
                        <nav>
                            <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor"
                                class="bi bi-fullscreen icon-grey" viewBox="0 0 16 16">
                                <path
                                    d="M1.5 1a.5.5 0 0 0-.5.5v4a.5.5 0 0 1-1 0v-4A1.5 1.5 0 0 1 1.5 0h4a.5.5 0 0 1 0 1zM10 .5a.5.5 0 0 1 .5-.5h4A1.5 1.5 0 0 1 16 1.5v4a.5.5 0 0 1-1 0v-4a.5.5 0 0 0-.5-.5h-4a.5.5 0 0 1-.5-.5M.5 10a.5.5 0 0 1 .5.5v4a.5.5 0 0 0 .5.5h4a.5.5 0 0 1 0 1h-4A1.5 1.5 0 0 1 0 14.5v-4a.5.5 0 0 1 .5-.5m15 0a.5.5 0 0 1 .5.5v4a1.5 1.5 0 0 1-1.5 1.5h-4a.5.5 0 0 1 0-1h4a.5.5 0 0 0 .5-.5v-4a.5.5 0 0 1 .5-.5" />
                            </svg>
                        </nav>
                    </div>
                    <div class="card-body">
                        <span class="fs-6 text">Add Content</span>
                        ${
                          userOwnsPage
                            ? `<form action="/api/v1/upload_image?target={{ request.path }}" method="post"
            enctype="multipart/form-data">
              <input type="file" name="file" required />
              <input type="submit" name="submit" value="submit" />
              <input type="hidden" name="operation" value="upload" />
              <input type="hidden" name="box_id" value="{{box.box_id}}" />
          </form>`
                            : ""
                        }
                    </div>
`;

      const headerText = newBox.querySelector("h5.header");
      if (headerText) headerText.contentEditable = true;

      const bodyText = newBox.querySelector(".card-body .text");
      if (bodyText) bodyText.contentEditable = true;

      // Add to flexbox container
      document.getElementById("flexContainer").appendChild(newBox);
    })
    .catch((error) => {
      console.error("Error creating box:", error);
      alert("Unable to create new box. Please try again.");
    });
}

document
  .getElementById("flexContainer")
  .addEventListener("click", async function (event) {
    const lockButton = event.target.closest(".lock-toggle");
    if (lockButton) {
      const boxId = lockButton.getAttribute("data-box-id");
      if (!boxId) {
        return;
      }

      try {
        const response = await fetch("/api/v1/toggle_box_visibility", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ box_id: Number(boxId) }),
          credentials: "include",
        });

        if (!response.ok) {
          const err = await response.json().catch(() => ({}));
          throw new Error(err.error || "Failed to toggle box visibility");
        }

        const data = await response.json();
        const icon = lockButton.querySelector("svg");
        if (data.show_all_players === 1) {
          icon.classList.remove("bi-lock-fill");
          icon.classList.add("bi-unlock-fill");
        } else {
          icon.classList.remove("bi-unlock-fill");
          icon.classList.add("bi-lock-fill");
        }

        window.location.reload();
        return;
      } catch (error) {
        console.error("Error toggling box visibility:", error);
        alert("Unable to change box visibility. Please try again.");
        return;
      }
    }

    const svg = event.target.closest("svg.bi-fullscreen.icon-grey");
    if (!svg) return;

    const cardHeader = svg.closest(".card-header");
    const headerTitle = cardHeader?.querySelector("h5.header");
    if (!headerTitle || !cardHeader) {
      console.error("Could not find card header for fullscreen page creation.");
      return;
    }

    const boxTitle = headerTitle.innerText.trim() || "Untitled";
    const boxId = headerTitle.getAttribute("box-id");
    const username = document.querySelector("main")?.getAttribute("username");

    if (!boxId || !username) {
      console.error("Missing box id or username while creating page.", {
        boxId,
        username,
        boxTitle,
      });
      alert("Unable to create page from this card. Missing card metadata.");
      return;
    }

    try {
      const pageId = await createPage(boxTitle, boxId);
      const targetLink = `/users/${username}/page/${pageId}/`;
      const nav = cardHeader.querySelector("nav");
      const linkHtml = `
            <a href="${targetLink}">
                <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor"
                    class="bi bi-fullscreen icon-black" viewBox="0 0 16 16">
                    <path
                        d="M1.5 1a.5.5 0 0 0-.5.5v4a.5.5 0 0 1-1 0v-4A1.5 1.5 0 0 1 1.5 0h4a.5.5 0 0 1 0 1zM10 .5a.5.5 0 0 1 .5-.5h4A1.5 1.5 0 0 1 16 1.5v4a.5.5 0 0 1-1 0v-4a.5.5 0 0 0-.5-.5h-4a.5.5 0 0 1-.5-.5M.5 10a.5.5 0 0 1 .5.5v4a.5.5 0 0 0 .5.5h4a.5.5 0 0 1 0 1h-4A1.5 1.5 0 0 1 0 14.5v-4a.5.5 0 0 1 .5-.5m15 0a.5.5 0 0 1 .5.5v4a1.5 1.5 0 0 1-1.5 1.5h-4a.5.5 0 0 1 0-1h4a.5.5 0 0 0 .5-.5v-4a.5.5 0 0 1 .5-.5" />
                </svg>
            </a>`;
      if (nav) {
        nav.innerHTML = linkHtml;
      } else {
        const newNav = document.createElement("nav");
        newNav.innerHTML = linkHtml;
        cardHeader.appendChild(newNav);
      }

      window.location.href = targetLink;
    } catch (error) {
      console.error("Error creating page:", error);
      alert("Unable to create page from this card. Please try again.");
    }
  });

function setLayout(mode) {
  const container = document.getElementById("flexContainer");
  if (mode === "one") {
    container.classList.remove("flex-row", "flex-wrap");
    container.classList.add("flex-column");
    Array.from(container.children).forEach((card) =>
      card.classList.remove("two-col"),
    );
  } else if (mode === "two") {
    container.classList.remove("flex-column");
    container.classList.add("flex-row", "flex-wrap");
    Array.from(container.children).forEach((card) =>
      card.classList.add("two-col"),
    );
  }
}

//creates and navigates to page
function createPage(boxTitle, boxId) {
  const payload = {
    page_title: boxTitle,
    box_id: boxId,
  };

  return fetch("/api/v1/create_page", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
    credentials: "include",
  })
    .then((response) => {
      if (!response.ok) {
        return response.json().then((err) => {
          throw new Error(err.error || "Create page failed");
        });
      }
      return response.json();
    })
    .then((data) => {
      if (!data.page_id) {
        throw new Error("Create page returned no page id");
      }
      return data.page_id;
    });
}

if (userOwnsPage) {
  window.addEventListener("beforeunload", function () {
    //we redo this to catch newly added items
    const textElements = document.getElementsByClassName("text");
    const headerElements = document.getElementsByClassName("header");

    let allTexts = [];
    let allHeaders = [];

    for (let i = 0; i < textElements.length; i++) {
      const textId = textElements[i].getAttribute("text-id");
      const currentText = textElements[i].innerText;
      allTexts.push({ id: textId, text: currentText });
    }

    for (let i = 0; i < headerElements.length; i++) {
      const boxId = headerElements[i].getAttribute("box-id");
      const currentHeader = headerElements[i].innerText;
      allHeaders.push({ id: boxId, title: currentHeader });
    }

    let pageTitle = document.getElementById("title").innerText;

    let pageId = document.getElementById("add-card").getAttribute("page-id");

    const payload = {
      texts: allTexts,
      headers: allHeaders,
      page_title: pageTitle,
      page_id: pageId,
    };
    const blob = new Blob([JSON.stringify(payload)], {
      type: "application/json",
    });
    navigator.sendBeacon("/api/v1/save_on_unload", blob);
  });
}
