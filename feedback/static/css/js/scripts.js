function showFeedbackForm(type) {
    window.location.href = `/feedback/?type=${type}`;
}

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('css-form');
    if (form) {
        form.addEventListener('submit', function(event) {
            event.preventDefault();
            if (confirm('Are you sure you want to submit this css?')) {
                form.submit();
            }
        });
    }

    const messages = document.querySelectorAll('.messages li');
    if (messages.length > 0) {
        messages.forEach(function(message) {
            alert(message.textContent);
        });
    }
});
