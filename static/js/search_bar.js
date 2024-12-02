 // Reattach the input event listener to the search bar on the new template
//  document.getElementById("search-bar").addEventListener("input", async function() {
//     const query = this.value.trim();
//     if (query.length > 0) {
//       try {
//         const response = await fetch(`/search_bar?query=${encodeURIComponent(query)}`);
//         const html = await response.text();
//         document.body.innerHTML = html;
//       } catch (error) {
//         console.error("Error fetching search results:", error);
//       }
//     }
//   });
    // Function to Render Results
    function renderResults(data) {
        resultsContainer.innerHTML = "";
    
        // Example rendering for jobs
        if (data.jobs) {
          data.jobs.forEach((job) => {
            const resultItem = document.createElement("div");
            resultItem.classList.add("result-item");
            resultItem.innerHTML = `
            <i class="fas fa-file-alt file-icon"></i>
            <div>
              <h4>${job.title}</h4>
              <p>Added by ${job.creator} in <span class="location">${job.location}</span></p>
            </div>
          `;
            resultsContainer.appendChild(resultItem);
          });
        }
      }
    
      // Tab Switching Logic
      tabs.forEach((tab) => {
        tab.addEventListener("click", () => {
          document.querySelector(".tab.active").classList.remove("active");
          tab.classList.add("active");
    
          // Update results based on tab (e.g., filter logic)
          const tabType = tab.getAttribute("data-tab");
          filterResults(tabType);
        });
      });
    
      function filterResults(tabType) {
        // Implement filtering logic for different tabs (e.g., "all", "team", etc.)
        // This example assumes `renderResults` can take specific data.
        console.log(`Filter results by ${tabType}`);
      }