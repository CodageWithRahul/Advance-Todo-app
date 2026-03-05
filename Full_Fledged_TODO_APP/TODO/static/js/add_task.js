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


function showConflictModal(){
    document.getElementById("conflictModal").style.display="flex";
}

function closeConflictModal(){
    document.getElementById("conflictModal").style.display="none";
}

function forceSubmit() {
    const form = document.getElementById("taskForm");

    let input = document.createElement("input");
    input.type = "hidden";
    input.name = "force_save";
    input.value = "1";

    form.appendChild(input);

    form.submit();
}