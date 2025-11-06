// This file provides the logic for opening and closing the sidebar on the campaign page

document.addEventListener("DOMContentLoaded", function () {

    // Get all the elements we need
    const mainContent = document.getElementById("main-content");
    const sidebar = document.getElementById("sidebar");
    const closeBtn = document.getElementById("close-sidebar-btn");
    const clickableItems = document.querySelectorAll(".clickable-item");

    // Get the text elements in the sidebar
    const sidebarTitle = document.getElementById("sidebar-title");
    const sidebarContent = document.getElementById("sidebar-content");

    // This variable will track which item is currently active
    let activeItem = null;

    // This function now *only* handles opening the layout
    function openSidebar() {
        mainContent.classList.remove("offset-lg-2", "col-lg-8");
        mainContent.classList.add("col-lg-8");
        sidebar.classList.remove("d-none");
    }

    // This function just updates the sidebar's text
    function updateSidebarContent(title, subtitle) {
        sidebarTitle.innerText = title;
        sidebarContent.innerText = `System: ${subtitle}`;
    }

    // This function handles closing the layout AND resetting the active item
    function closeSidebar() {
        mainContent.classList.remove("col-lg-8");
        mainContent.classList.add("col-lg-8", "offset-lg-2");
        sidebar.classList.add("d-none");
        
        // Reset text
        sidebarTitle.innerText = "Character Details";
        sidebarContent.innerText = "Click a character to see their details here.";

        // If an item was active, un-highlight it and untrack it
        if (activeItem) {
            // "active" is a built-in Bootstrap class that highlights list-group-items
            activeItem.classList.remove("active"); 
            activeItem = null;
        }
    }

    // --- Event Listeners ---

    // This listener now has all the new toggle logic
    clickableItems.forEach(item => {
        item.addEventListener("click", function (event) {
            
            // Stop the link (href) from navigating to a new page
            event.preventDefault();

            const clickedItem = event.currentTarget; // Get the link that was clicked
            const isSidebarHidden = sidebar.classList.contains('d-none');
            
            // Get data from the clicked item
            const title = clickedItem.getAttribute("data-name");
            const subtitle = clickedItem.getAttribute("data-system");

            if (isSidebarHidden) {
                // --- CASE 1: Sidebar is closed ---
                // Open it, update the text, and set this item as active
                openSidebar();
                updateSidebarContent(title, subtitle);
                activeItem = clickedItem;
                activeItem.classList.add("active");
            
            } else {
                // --- CASE 2: Sidebar is already open ---
                if (clickedItem === activeItem) {
                    // A) Clicked the *same item* that is already active: Close the sidebar
                    closeSidebar(); // This function will reset activeItem to null
                
                } else {
                    // B) Clicked a *different item*: Just swap the content
                    updateSidebarContent(title, subtitle);
                    
                    // Swap the 'active' highlight from the old item to the new one
                    if (activeItem) {
                        activeItem.classList.remove("active");
                    }
                    activeItem = clickedItem;
                    activeItem.classList.add("active");
                }
            }
        });
    });

    closeBtn.addEventListener("click", closeSidebar);
});