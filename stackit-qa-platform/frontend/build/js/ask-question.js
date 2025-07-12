// Form submission handler
        document.getElementById('submitQuestionForm').addEventListener('submit', function(e) {
            e.preventDefault();
            
            const title = document.getElementById('questionTitle').value;
            const description = document.getElementById('questionDescription').value;
            const tags = document.getElementById('questionTags').value;
            
            if (title && description) {
                // Show success message
                const successMessage = document.getElementById('successMessage');
                successMessage.classList.add('show');
                
                // Clear form
                this.reset();
                document.getElementById('tagContainer').innerHTML = '';
                
                // Hide success message after 3 seconds
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
                if (tag) {
                    const tagElement = document.createElement('span');
                    tagElement.className = 'tag';
                    tagElement.textContent = tag;
                    tagContainer.appendChild(tagElement);
                }
            });
        });

        // Add floating animation to form elements
        document.querySelectorAll('.form-group input, .form-group textarea').forEach(element => {
            element.addEventListener('focus', function() {
                this.style.transform = 'translateY(-2px)';
            });
            
            element.addEventListener('blur', function() {
                this.style.transform = 'translateY(0)';
            });
        });