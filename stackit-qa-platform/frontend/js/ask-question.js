// Initialize Quill
const quill = new Quill('#questionEditor', {
    theme: 'snow',
    modules: {
        toolbar: [
            ['bold', 'italic', 'underline', 'strike'],
            [{ list: 'ordered' }, { list: 'bullet' }],
            ['link', 'image', 'code-block'],
            ['clean']
        ]
    },
    placeholder: 'Provide all the details for your question...'
});

// Form submission handler
document.getElementById('submitQuestionForm').addEventListener('submit', function(e) {
    e.preventDefault();

    const title = document.getElementById('questionTitle').value.trim();
    const description = quill.root.innerHTML.trim();
    const textContent = quill.getText().trim(); // plain text check
    const tags = document.getElementById('questionTags').value.trim();

    if (title && textContent) {
        // Show success message
        const successMessage = document.getElementById('successMessage');
        successMessage.classList.add('show');

        // Reset form
        document.getElementById('questionTitle').value = '';
        quill.setContents([]);
        document.getElementById('questionTags').value = '';
        document.getElementById('tagContainer').innerHTML = '';

        setTimeout(() => {
            successMessage.classList.remove('show');
        }, 3000);
    }
});

// Tag preview functionality
document.getElementById('questionTags').addEventListener('input', function() {
    const tags = this.value.split(',').map(tag => tag.trim()).filter(tag => tag);
    const tagContainer = document.getElementById('tagContainer');
    tagContainer.innerHTML = '';
    tags.forEach(tag => {
        const tagElement = document.createElement('span');
        tagElement.className = 'tag';
        tagElement.textContent = tag;
        tagContainer.appendChild(tagElement);
    });
});

// Floating animation
document.querySelectorAll('.form-group input').forEach(element => {
    element.addEventListener('focus', function() {
        this.style.transform = 'translateY(-2px)';
    });
    element.addEventListener('blur', function() {
        this.style.transform = 'translateY(0)';
    });
});
