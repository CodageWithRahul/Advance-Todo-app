const modal = document.getElementById("deleteModal");
const modalTitle = document.getElementById("modal-title");
const deleteForm = document.getElementById("deleteForm");
const cancelBtn = document.getElementById("cancelBtn");

document.querySelectorAll(".delete-btn").forEach(btn => {
    btn.addEventListener("click", function (e) {
        e.preventDefault();

        const taskId = this.dataset.taskId;

        modalTitle.innerText = `Are you sure you want to delete ?`;
        deleteForm.action = `/task/delete/${taskId}/`;
        modal.style.display = "flex";
    });
});

cancelBtn.addEventListener("click", () => {
    modal.style.display = "none";
});
