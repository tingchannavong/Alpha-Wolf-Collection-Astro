import DOMPurify from "dompurify";
import Fuse from "fuse.js";

let SEARCH_DATA;
let FUSE_INSTANCE;
const FUSE_OPTIONS = {
    includeScore: true,
    shouldSort: true,
    threshold: 0.5,
    keys: [
        {
            name: "frontmatter.title",
            weight: 1,
        },
        {
            name: "frontmatter.description",
            weight: 0.75,
        }
    ]
}

const search = document.querySelector("#search");
const search_readout = document.querySelector("#search_readout");
const searchResultsContainer = document.querySelector("#search_results");

function updateDocumentTitle(search) {
    document.title = search 
    ? `Search results for ${search}` 
    : ""
}

function updateSearchReadout(search) {
    search_readout.textContent = search 
    ? `Search results for ${search}:` 
    : "";    
}

async function initializeFuse() {
if (!SEARCH_DATA) {
    const response = await fetch("/search.json");
    SEARCH_DATA = await response.json();
}
if (!FUSE_INSTANCE) {
    FUSE_INSTANCE = new Fuse(SEARCH_DATA, FUSE_OPTIONS);
}
}

async function fetchSearchResults(search) {
    if (!search) return;

    await initializeFuse();
    const results = FUSE_INSTANCE.search(search);
    displaySearchResults(results);
}

// Display the search results in the DOM using the <Card> format
function displaySearchResults(results: SearchResult[]): void {
    if (!searchResultsContainer) return;

    searchResultsContainer.innerHTML = ""; // Clear previous results

    if (results.length === 0) {
        searchResultsContainer.innerHTML = "<li>No results found.</li>";
        return;
    }

    results.forEach((result) => {
        const game = result.item;
        const listItem = document.createElement('ul');

        listItem.innerHTML = `
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
               <div class="game-info-container">
                <p class="game-location">Playing Time:  ${game.frontmatter.location} Minutes</p>
                <p class="game-location">Minimum Players:  ${game.frontmatter.location}</p>
                <p class="game-location">Maximum Players:  ${game.frontmatter.max_players}</p>
                <p class="game-location">Location: ${game.frontmatter.location}</p>
            </div>
            </div>
            <div class="game-meta">
                <a href="${game.url}" class="game-read-more">Read more</a>
            </div>
        </div>
        `;
        searchResultsContainer.appendChild(listItem);
    });
}

window.addEventListener("DOMContentLoaded", () => {
    const urlParams = DOMPurify.sanitize(
        new URLSearchParams(window.location.search).get("q")
    );
    fetchSearchResults(urlParams);
    updateDocumentTitle(urlParams);
    updateSearchReadout(urlParams);
    search.value = urlParams;
    search.focus();
})

// Handle search input
search.addEventListener("input", () => {
    const search_term = DOMPurify.sanitize(search.value);
    updateDocumentTitle(search_term);
    updateSearchReadout(search_term);
    fetchSearchResults(search_term);
});
  
