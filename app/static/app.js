document.addEventListener("DOMContentLoaded", function() {
    const universityInput = document.getElementById("university-input");
    const exploreUniversityBtn = document.getElementById("explore-university");
    const universityPrompt = document.getElementById("university-prompt");

    const programSection = document.getElementById("program-section");
    const programSelect = document.getElementById("program-select");
    const exploreProgramBtn = document.getElementById("explore-program");

    const universityDetailsSection = document.getElementById("university-details-section");
    const overviewElement = document.getElementById("overview");
    const deadlineElement = document.getElementById("deadline");
    const reviewsElement = document.getElementById("reviews");
    const careerPathsElement = document.getElementById("career-paths");

    // Fetch prompt from the backend
    fetch("/").then(response => response.json()).then(data => {
        universityPrompt.textContent = data.ai_prompt;
    });

    // Handle university exploration
    exploreUniversityBtn.addEventListener("click", function() {
        const universityName = universityInput.value.trim();
        if (universityName) {
            fetch("/explore", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ university_name: universityName })
            }).then(response => response.json()).then(data => {
                if (data.ai_prompt) {
                    // Display program selection
                    programSection.style.display = "block";
                    programSelect.innerHTML = "";
                    data.programs.forEach(program => {
                        const option = document.createElement("option");
                        option.value = program;
                        option.textContent = program;
                        programSelect.appendChild(option);
                    });
                    document.getElementById("program-prompt").textContent = data.ai_prompt;
                    // Hide university exploration section
                    document.getElementById("university-section").style.display = "none";
                } else {
                    alert(data.error || "University not found.");
                }
            });
        }
    });

    // Handle program exploration
    exploreProgramBtn.addEventListener("click", function() {
        const selectedProgram = programSelect.value;
        const universityName = universityInput.value.trim();

        if (selectedProgram) {
            fetch("/university-details", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ university_name: universityName, program_name: selectedProgram })
            }).then(response => response.json()).then(data => {
                if (data.ai_overview) {
                    // Display university details
                    universityDetailsSection.style.display = "block";
                    overviewElement.textContent = data.ai_overview;
                    deadlineElement.textContent = data.deadline;
                    reviewsElement.textContent = data.reviews.join(", ");
                    careerPathsElement.textContent = data.career_paths.join(", ");
                    // Hide program selection section
                    programSection.style.display = "none";
                } else {
                    alert(data.error || "Program not found.");
                }
            });
        }
    });
});
