document.addEventListener('DOMContentLoaded', function() {
    // Auto-expand image preview sections
    const imagePreviewFields = document.querySelectorAll('.field-image_preview');
    imagePreviewFields.forEach(field => {
        const fieldset = field.closest('fieldset');
        if (fieldset && fieldset.classList.contains('collapse')) {
            fieldset.classList.remove('collapse');
            fieldset.classList.add('collapse-open');
        }
    });

    // Add file name display for file inputs
    const fileInputs = document.querySelectorAll('input[type="file"]');
    fileInputs.forEach(input => {
        input.addEventListener('change', function(e) {
            const fileName = e.target.files[0]?.name;
            if (fileName) {
                const fileNameDisplay = document.createElement('span');
                fileNameDisplay.className = 'file-name-display';
                fileNameDisplay.textContent = `Selected file: ${fileName}`;
                
                // Remove previous display if exists
                const previousDisplay = input.parentElement.querySelector('.file-name-display');
                if (previousDisplay) {
                    previousDisplay.remove();
                }
                
                input.parentElement.appendChild(fileNameDisplay);
            }
        });
    });

    // Add preview for image uploads
    const imageInputs = document.querySelectorAll('input[type="file"][accept*="image"]');
    imageInputs.forEach(input => {
        input.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    let preview = input.parentElement.querySelector('.image-upload-preview');
                    if (!preview) {
                        preview = document.createElement('div');
                        preview.className = 'image-upload-preview';
                        input.parentElement.appendChild(preview);
                    }
                    preview.innerHTML = `<img src="${e.target.result}" style="max-height: 200px; margin-top: 10px;">`;
                }
                reader.readAsDataURL(file);
            }
        });
    });

    // Add character count for text fields
    const textareas = document.querySelectorAll('textarea:not(.ckeditor)');
    textareas.forEach(textarea => {
        const counter = document.createElement('div');
        counter.className = 'char-counter';
        counter.style.cssText = 'text-align: right; color: #666; font-size: 0.8em;';
        textarea.parentElement.appendChild(counter);

        function updateCounter() {
            counter.textContent = `${textarea.value.length} characters`;
        }

        textarea.addEventListener('input', updateCounter);
        updateCounter();
    });

    // Enhance collapsible sections
    const collapsibleHeaders = document.querySelectorAll('h2.collapse-handler');
    collapsibleHeaders.forEach(header => {
        header.style.cursor = 'pointer';
        header.addEventListener('click', function() {
            const content = this.nextElementSibling;
            if (content.style.display === 'none') {
                content.style.display = 'block';
                this.classList.add('expanded');
            } else {
                content.style.display = 'none';
                this.classList.remove('expanded');
            }
        });
    });

    // Add tooltips for help text
    const helpTexts = document.querySelectorAll('.help');
    helpTexts.forEach(help => {
        help.style.cursor = 'help';
        help.setAttribute('title', help.textContent);
    });

    // Enhance related lookup popup
    const relatedLookups = document.querySelectorAll('.related-lookup');
    relatedLookups.forEach(lookup => {
        lookup.addEventListener('click', function(e) {
            e.preventDefault();
            const href = this.href;
            window.open(href, 'Related', 'height=600,width=800,resizable=yes,scrollbars=yes');
        });
    });
}); 