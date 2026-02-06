const categoryFilter = document.querySelector("#category-select");
const locationFilter = document.querySelector("#location-select");
const playerNumFilter = document.querySelector("#player-num-select");

const filter_readout = document.querySelector("#filter_readout");
const searchResultsContainer = document.querySelector("#search_results");

const titleSort = document.querySelector("#sort-title-select");
const playtimeSort = document.querySelector("#sort-time-select");
const playersSort = document.querySelector("#sort-players-select");

// Function to fetch all games data from .json file
async function fetchData() {
  const response = await fetch("/search.json");
  const data = await response.json();
  return data;
}

function updateFilterSelection(filter_type, value) {
  if (!value) {filter_type.value = "all"}
  else {
    filter_type.value = value; 
    filter_readout.textContent = value
    ? `Filter results for ${value}:` 
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
            <div class="game-info-container">
                <p class="game-location">Playing Time:  ${game.frontmatter.playing_time} Minutes</p>
                <p class="game-location">Minimum Players:  ${game.frontmatter.min_players}</p>
                <p class="game-location">Maximum Players:  ${game.frontmatter.max_players}</p>
                <p class="game-location">Size: ${game.frontmatter.box_size}</p>
            </div>
          </div>
          <div class="game-meta">
              <a href="${game.url}" class="game-read-more">Read more</a>
          </div>
      </div>
      `).join("");

      searchResultsContainer.innerHTML = html;
}

function updateFilters(key, value) {
  const params = new URLSearchParams(window.location.search);

  if (value) {
    params.set(key, value); // Update the filter
  } else {
    params.delete(key); // Remove filter if empty
  }
  const url = new URL("/filter", window.location.origin);
  const newUrl = `${url}?${params.toString()}`;
  window.location.assign(newUrl.toString());
  
}

function extractUrlParams() {
  const query = new URLSearchParams(window.location.search);

  const filters = {
    category: query.get("category")|| "all",
    location: query.get("location")|| "all",
    players: query.get("players")|| "all",
  }
  console.log(filters);
    return filters;
};

function calcFilterSize(filteredGames) {
   // calculation filter size
   const FilterSize = filteredGames.length;
   filter_readout.textContent = `Filter results (${FilterSize}):`;
}

function isMin(value1, filter) {
  return value1 === filter;
}

function filterLoc(data, filters) {
  const filteredData = data.filter(game => game.frontmatter.location.includes(filters.location));
  return filteredData;
}

function filterCat(data, filters) {
  const filteredData = data.filter(game => game.frontmatter.category.includes(filters.category));
  return filteredData;
}

function filterPlayers(data, filters) {
  const filteredData = data.filter(game => isMin(game.frontmatter.min_players, Number(filters.players)));
  return filteredData;
}

async function filterQuery(filters) {

  const data = await fetchData();

  if (filters.category === "all" && filters.location === "all" && filters.players === "all") {
    displayFilterResults(data);
    calcFilterSize(data);
    return data;

  } else if (filters.category === "all" && filters.location === "all") {
  const filter2 = filterPlayers(data, filters)
  displayFilterResults(filter2);
  calcFilterSize(filter2);
  return filter2;

} else if (filters.category === "all" && filters.players === "all") {
  const filter2 = filterLoc(data, filters)
  displayFilterResults(filter2);
  calcFilterSize(filter2);
  return filter2;

} else if (filters.location === "all" && filters.players === "all") {
  const filter2 = filterCat(data, filters)
  displayFilterResults(filter2);
  calcFilterSize(filter2);
  return filter2;

} else if (filters.category === "all") {
    const filter1 = filterLoc(data, filters)
    const filter2 = filterPlayers(filter1, filters)
    displayFilterResults(filter2);
    calcFilterSize(filter2);
    return filter2;

  } else if (filters.location === "all") {
    const filter1 = filterCat(data, filters)
    const filter2 = filterPlayers(filter1, filters)
    displayFilterResults(filter2);
    calcFilterSize(filter2);
    return filter2;

  } else if (filters.players === "all") {
    const filter1 = filterCat(data, filters)
    const filter2 = filterLoc(filter1, filters)
    displayFilterResults(filter2);
    calcFilterSize(filter2);
    return filter2;
  } else {
  const filteredGames = data
  .filter(game => game.frontmatter.category.includes(filters.category))
  .filter(game => game.frontmatter.location.includes(filters.location))
  .filter(game => isMin(game.frontmatter.min_players, Number(filters.players)))

  displayFilterResults(filteredGames);
  calcFilterSize(filteredGames);
  return filteredGames;
  }
}

function extractSortParams() {
  const query = new URLSearchParams(window.location.search);

  const sort = {
    sort_title: query.get("sort_title")|| "none",
    sort_players: query.get("sort_players")|| "none",
    sort_time: query.get("sort_time")|| "none",
  }
  console.log(sort);
    return sort;
}

async function sortQuery(filteredData, sort_queries) {
  await filteredData;
   if (sort_queries.sort_title === "z-a") {
      // both filtered and sorted data is a fulfilled promise so need to handly by .then(arrow func)
      const sortedData = filteredData.then((array) => array.reverse());
      sortedData.then((array) => displayFilterResults(array));
    } else if (sort_queries.sort_title === "a-z") {
      const sortedData = filteredData.then((array) => array.sort());
      sortedData.then((array) => displayFilterResults(array));
    
    } else if (sort_queries.sort_time === "asc") {
      console.log(filteredData);
      const sortedData = filteredData.then((array) => array.sort((a,b) => a.frontmatter.playing_time - b.frontmatter.playing_time));
      sortedData.then((array) => displayFilterResults(array));
    } else if (sort_queries.sort_time === "des") {
      const sortedData = filteredData.then((array) => array.sort((a,b) => b.frontmatter.playing_time - a.frontmatter.playing_time));
      sortedData.then((array) => displayFilterResults(array));
    
    } else if (sort_queries.sort_players === "asc") {
      const sortedData = filteredData.then((array) => array.sort((a,b) => a.frontmatter.min_players - b.frontmatter.min_players));
      sortedData.then((array) => displayFilterResults(array));
    } else if (sort_queries.sort_players === "des") {
      const sortedData = filteredData.then((array) => array.sort((a,b) => b.frontmatter.min_players - a.frontmatter.min_players));
      sortedData.then((array) => displayFilterResults(array));
}}

function clearSortFilters( keysToRemove: string[]) {
  const params = new URLSearchParams(window.location.search); // Get current url

  // Remove specified keys
  keysToRemove.forEach((key) => params.delete(key));

  const newUrl = `${window.location.pathname}?${params.toString()}`;

  window.location.assign(newUrl.toString());

}

// Add event listener to the category dropdown
categoryFilter.addEventListener("change", (event) => { 
  const selectedCategory = (event.target as HTMLInputElement).value.toString();
    if (!selectedCategory || selectedCategory.length === 0)  return;

    //set new url
    updateFilters('category', selectedCategory);
  });

// Add event listener to location dropdown
locationFilter.addEventListener("change", (event) => { 
  const selectedLocation = (event.target as HTMLInputElement).value.toString();
    if (!selectedLocation || selectedLocation.length === 0)  return;

    //set new url
    updateFilters('location', selectedLocation);
  });

// Add event listener to player number dropdown
playerNumFilter.addEventListener("change", (event) => { 
  const playerNumFilter = (event.target as HTMLInputElement).value;
    if (!playerNumFilter || playerNumFilter.length === 0 || playerNumFilter === null)  return;

    //set new url
    updateFilters('players', playerNumFilter);
  });

// Add event listener to sort title dropdown
titleSort.addEventListener("change", (event) => { 
  const titleSort = (event.target as HTMLInputElement).value;
    if (!titleSort) return;

    //set new url
    updateFilters('sort_title', titleSort);
  });

// Add event listener to sort playtime dropdown
playtimeSort.addEventListener("change", (event) => { 
  const playtimeSort = (event.target as HTMLInputElement).value;
    if (!playtimeSort)  return;

    //set new url
    updateFilters('sort_time', playtimeSort);

    //update other sort queries as none
    (titleSort as HTMLInputElement).value === "none";
    (playersSort as HTMLInputElement).value === "none";
  });

// Add event listener to sort players dropdown
playersSort.addEventListener("change", (event) => { 
  const playersSort = (event.target as HTMLInputElement).value;
    if (!playersSort)  return;

    //set new url
    updateFilters('sort_players', playersSort);

    //update other sort queries as none
    (titleSort as HTMLInputElement).value === "none";
    (playtimeSort as HTMLInputElement).value === "none";
  });

// event listener when a page finishes loading
window.addEventListener("DOMContentLoaded", () => {
  const path = window.location.pathname;

  if (path.match(/^\/boardgames\/\d+$/) || path === "/boardgames/1") {
        return; 
    } else {

  // Handle filters first 
    const catParams = new URLSearchParams(window.location.search).get("category");
    const locParams = new URLSearchParams(window.location.search).get("location");
    const playersParams = new URLSearchParams(window.location.search).get("players");
    
    updateFilterSelection(categoryFilter, catParams);
    updateFilterSelection(locationFilter, locParams);
    updateFilterSelection(playerNumFilter, playersParams);

    const queries = extractUrlParams();

    const filteredData = filterQuery(queries);

    // Handle sorting second
    const sortTitleParams = new URLSearchParams(window.location.search).get("sort_title");
    const sortTimeParams = new URLSearchParams(window.location.search).get("sort_time");
    const sortPlayersParams = new URLSearchParams(window.location.search).get("sort_players");

    // Need to get rid of the url params for each sort case
    updateFilterSelection(titleSort, sortTitleParams);
    updateFilterSelection(playtimeSort, sortTimeParams);
    updateFilterSelection(playersSort, sortPlayersParams);

    const sort_queries = extractSortParams();

    sortQuery(filteredData, sort_queries);
      }

});
