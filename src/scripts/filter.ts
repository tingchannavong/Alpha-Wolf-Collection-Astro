const categoryFilter = document.querySelector("#category-select");
// const filteredResults = document.querySelector("#filteredResults");

// Function to filter and display results
// function filterResults(category) {
//     const allGameElements = Array.from(document.querySelectorAll(".game-item"));

//     allGameElements.forEach((game) => {
//       const gameCategory = game.querySelector("p:nth-child(3)").textContent.replace("Category: ", "");
//       if (!category || gameCategory === category) {
//         game.style.display = "block";
//       } else {
//         game.style.display = "none";
//       }
//     });
//   }

// Add event listener to the dropdown
categoryFilter.addEventListener("change", (event) => {
    const selectedCategory = event.target.value.toString();
    console.log(selectedCategory);
    if (!selectedCategory || selectedCategory.length === 0)  return;
    const url = new URL("/category", window.location.origin);
    url.searchParams.set("filter", selectedCategory); // set filtered param
    window.location.assign(url.toString());

    // filterResults(selectedCategory);
  });