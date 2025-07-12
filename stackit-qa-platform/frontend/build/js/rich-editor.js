/**
 * Rich Text Editor Component
 * Implements a full-featured editor with formatting options
 */

class RichTextEditor {
    constructor(elementId, placeholderText = 'Start typing here...') {
        this.elementId = elementId;
        this.placeholderText = placeholderText;
        this.editor = null;
        this.toolbarOptions = [
            ['bold', 'italic', 'strike'],                     // text formatting
            [{ 'list': 'ordered'}, { 'list': 'bullet' }],     // lists
            ['link', 'image'],                                // media
            [{ 'align': ['', 'center', 'right', 'justify'] }] // text alignment
        ];
        
        this.init();
    }
    
    init() {
        // Initialize Quill editor with toolbar options
        this.editor = new Quill(`#${this.elementId}`, {
            modules: {
                toolbar: this.toolbarOptions
            },
            placeholder: this.placeholderText,
            theme: 'snow'
        });
        
        // Setup image handler
        const toolbar = this.editor.getModule('toolbar');
        toolbar.addHandler('image', this.imageHandler.bind(this));
        
        // Add editor instance to global registry for access
        window.editors = window.editors || {};
        window.editors[this.elementId] = this;
    }
    
    imageHandler() {
        const input = document.createElement('input');
        input.setAttribute('type', 'file');
        input.setAttribute('accept', 'image/*');
        input.click();
        
        input.onchange = async () => {
            const file = input.files[0];
            if (file) {
                try {
                    const imageUrl = await this.uploadImage(file);
                    // Insert image at current cursor position
                    const range = this.editor.getSelection(true);
                    this.editor.insertEmbed(range.index, 'image', imageUrl);
                } catch (error) {
                    console.error('Image upload failed:', error);
                    alert('Failed to upload image. Please try again.');
                }
            }
        };
    }
    
    async uploadImage(file) {
        // Create form data for image upload
        const formData = new FormData();
        formData.append('image', file);
        
        // Send to backend
        const response = await fetch('/api/upload-image', {
            method: 'POST',
            body: formData,
            credentials: 'same-origin'
        });
        
        if (!response.ok) {
            throw new Error('Image upload failed');
        }
        
        const data = await response.json();
        return data.imageUrl;
    }
    
    getContent() {
        // Returns the HTML content of the editor
        return this.editor.root.innerHTML;
    }
    
    setContent(html) {
        // Sets the HTML content of the editor
        this.editor.root.innerHTML = html;
    }
    
    getText() {
        // Returns the plain text content
        return this.editor.getText();
    }
    
    isEmpty() {
        return this.getText().trim().length === 0;
    }
    
    focus() {
        this.editor.focus();
    }
    
    // Clean the editor content for submission
    getSanitizedContent() {
        // This uses DOMPurify which should be included in your project
        return DOMPurify.sanitize(this.getContent());
    }
}

// Usage: 
// const questionEditor = new RichTextEditor('question-editor', 'Describe your question in detail...');
// const answerEditor = new RichTextEditor('answer-editor', 'Write your answer here...');