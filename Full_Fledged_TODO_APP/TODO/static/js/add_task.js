document.addEventListener("DOMContentLoaded", function () {
    const taskTypeSelect = document.getElementById("id_task_type");
    const dateField = document.getElementById("date-field");
    const dateInput = document.getElementById("id_start_date");

    function toggleDateField() {
        if (taskTypeSelect.value === "FUTURE") {
            dateField.style.display = "flex";
            dateInput.required = true;
            
        } else {
            dateField.style.display = "none";
            dateInput.required = false;
        }
    }

    taskTypeSelect.addEventListener("change", toggleDateField);
    toggleDateField(); // run on page load
});
