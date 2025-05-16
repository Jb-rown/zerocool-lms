// Toggle mobile menu
document.addEventListener('DOMContentLoaded', function() {
    // Mark lesson as completed
    document.querySelectorAll('.complete-lesson').forEach(button => {
        button.addEventListener('click', function() {
            const lessonId = this.dataset.lessonId;
            fetch(`/courses/complete-lesson/${lessonId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({completed: true})
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    this.textContent = '✓ Completed';
                    this.classList.remove('bg-blue-600');
                    this.classList.add('bg-green-500', 'cursor-default');
                    this.disabled = true;
                    
                    // Update progress bar
                    const progressBar = document.querySelector('.progress-fill');
                    if (progressBar) {
                        progressBar.style.width = `${data.progress}%`;
                    }
                }
            });
        });
    });
    
    // Code editor for coding assignments
    if (document.getElementById('code-editor')) {
        const editor = CodeMirror.fromTextArea(document.getElementById('code-editor'), {
            lineNumbers: true,
            mode: 'python',
            theme: 'dracula',
            indentUnit: 4
        });
        
        // Save code periodically
        setInterval(() => {
            const code = editor.getValue();
            localStorage.setItem('draft-code', code);
        }, 3000);
    }
});

// Helper function to get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}