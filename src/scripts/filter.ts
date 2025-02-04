const categoryFilter = document.querySelector("#category-select");
const filter_readout = document.querySelector("#filter_readout");
const searchResultsContainer = document.querySelector("#search_results");

async function fetchData() {
  const response = await fetch("/search.json");
  const data = await response.json();
  return data;
}

async function fetchFilter(filter) {
  const data = await fetchData();

  if (filter === "all") {
    window.location.href = "/boardgames/1"; 
  } else {
    const filteredData = data.filter((game) => 
      game.frontmatter.category.includes(filter) 
    );
    displayFilterResults(filteredData);
    console.log(filteredData);

    // calculation filter size
    const FilterSize = filteredData.length;
    filter_readout.textContent = filter
    ? `Filter results for ${filter} (${FilterSize}):` 
    : "";
  }
}

function updateDocumentTitle(filter) {
  document.title = filter 
  ? `Filter results for ${filter}` 
  : ""
}

function updateFilterSelection(filter) {
  if (!filter) {categoryFilter.value = "all"}
  else {
    categoryFilter.value = filter; 
    filter_readout.textContent = filter
    ? `Filter results for ${filter}:` 
    : "";
  };
}

// Display the search results in the DOM using the <Card> format
function displayFilterResults(results) {
  if (!searchResultsContainer) return;

  searchResultsContainer.innerHTML = ""; // Clear previous results

  if (results.length === 0) {
      searchResultsContainer.innerHTML = "<li>No results found.</li>";
      return;
  }

  const html = results.map((game) => 
  `
      <div class="game-item">
          <div class="game-image-container">
              <img src="${game.frontmatter.image}" alt="${game.frontmatter.title}" class="game-image">
          </div>
          <div class="game-details">
              <h3 class="game-title">${game.frontmatter.title}</h3>
              <p class="game-description">
                  ${game.frontmatter.description}
              </p>
              <p class="game-category">Category: ${game.frontmatter.category}</p>
              <p class="game-location">Location: ${game.frontmatter.location}</p>
          </div>
          <div class="game-meta">
              <a href="${game.url}" class="game-read-more">Read more</a>
          </div>
      </div>
      `).join("");

      searchResultsContainer.innerHTML = html;
}

// Add event listener to the dropdown
categoryFilter.addEventListener("change", (event) => {
    const selectedCategory = event.target.value.toString();
    if (!selectedCategory || selectedCategory.length === 0)  return;
    const url = new URL("/filter", window.location.origin);
    url.searchParams.set("category", selectedCategory); // set filtered param
    window.location.assign(url.toString());
  });

// when filter is selected update the filter terms
window.addEventListener("DOMContentLoaded", () => {
    const urlParams = new URLSearchParams(window.location.search).get("category");

    if (urlParams === null) {return} else {
      updateDocumentTitle(urlParams);
      updateFilterSelection(urlParams);
      fetchFilter(urlParams);
    }
})
