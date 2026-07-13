const CATEGORY_LABELS = {
  advice: "Doctor guidance",
  study: "Study & news",
  news: "Study & news",
};

function escapeHtml(text) {
  return String(text)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

let allPosts = [];

async function loadBlog() {
  const container = document.getElementById("blog-posts");
  const updatedEl = document.getElementById("blog-updated");

  try {
    const response = await fetch("blog/posts.json");
    if (!response.ok) throw new Error("Could not load posts");

    const data = await response.json();
    allPosts = data.posts || [];

    if (updatedEl) {
      const date = data.last_updated
        ? new Date(data.last_updated + "T12:00:00").toLocaleDateString("en-US", {
            year: "numeric",
            month: "long",
            day: "numeric",
          })
        : "Unknown";
      updatedEl.textContent = `Last updated: ${date} · ${allPosts.length} articles`;
    }

    renderPosts("all");
  } catch {
    if (container) {
      container.innerHTML =
        "<p class='muted'>Could not load articles. Run <code>python scripts/update_blog.py</code> locally.</p>";
    }
  }
}

function renderPosts(filter) {
  const container = document.getElementById("blog-posts");
  if (!container) return;

  const posts =
    filter === "all" ? allPosts : allPosts.filter((p) => p.category === filter);

  if (!posts.length) {
    container.innerHTML = "<p class='muted'>No articles in this category yet.</p>";
    return;
  }

  container.innerHTML = posts
    .map((post) => {
      const label = CATEGORY_LABELS[post.category] || "Update";
      const date = post.published
        ? new Date(post.published + "T12:00:00").toLocaleDateString("en-US", {
            year: "numeric",
            month: "short",
            day: "numeric",
          })
        : "";

      return `
        <article class="blog-card" data-category="${escapeHtml(post.category)}">
          <div class="blog-card-meta">
            <span class="blog-category">${escapeHtml(label)}</span>
            <span class="blog-date">${escapeHtml(date)}</span>
          </div>
          <h2 class="blog-card-title">
            <a href="${escapeHtml(post.url)}" target="_blank" rel="noopener noreferrer">${escapeHtml(post.title)}</a>
          </h2>
          <p class="blog-card-summary">${escapeHtml(post.summary)}</p>
          <a
            class="blog-card-link"
            href="${escapeHtml(post.url)}"
            target="_blank"
            rel="noopener noreferrer"
          >
            Read on ${escapeHtml(post.source)} (${escapeHtml(post.domain)}) →
          </a>
        </article>
      `;
    })
    .join("");
}

document.querySelectorAll(".filter-btn").forEach((btn) => {
  btn.addEventListener("click", () => {
    document.querySelectorAll(".filter-btn").forEach((b) => b.classList.remove("active"));
    btn.classList.add("active");
    renderPosts(btn.dataset.filter);
  });
});

loadBlog();
