function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) {
        return parts.pop().split(';').shift();
    }
    return null;
}

function handleToggle(event) {
    const checkbox = event.currentTarget;
    const noteId = checkbox.dataset.noteId;
    if (!noteId) {
        return;
    }

    const csrftoken = getCookie('csrftoken');
    if (!csrftoken) {
        checkbox.checked = !checkbox.checked;
        return;
    }

    fetch(`/note/toggle/${noteId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
        },
        body: JSON.stringify({ is_done: checkbox.checked }),
    })
        .then(async (response) => {
            if (!response.ok) {
                throw new Error('Unable to update note');
            }
            return response.json();
        })
        .then((data) => {
            const label = checkbox.closest('.note-item');
            const text = label ? label.querySelector('.note-text') : null;
            if (text) {
                text.classList.toggle('done', Boolean(data.is_done));
            }
        })
        .catch(() => {
            checkbox.checked = !checkbox.checked;
        });
}

document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.note-check').forEach((checkbox) => {
        checkbox.addEventListener('change', handleToggle);
    });
});
