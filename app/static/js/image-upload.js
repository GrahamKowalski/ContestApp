document.addEventListener('DOMContentLoaded', function() {
    const uploadContainer = document.getElementById('upload-container');
    const fileInput = document.getElementById('file-input');
    const previewContainer = document.getElementById('preview-container');
    const imagePreview = document.getElementById('image-preview');
    const removeButton = document.getElementById('remove-image');

    function handleFile(file) {
        if (file.type.startsWith('image/')) {
            const reader = new FileReader();
            reader.onload = function(e) {
                imagePreview.src = e.target.result;
                previewContainer.style.display = 'block';
                uploadContainer.style.display = 'none';
            };
            reader.readAsDataURL(file);
        } else {
            alert('Please upload an image file.');
        }
    }

    uploadContainer.addEventListener('dragover', function(e) {
        e.preventDefault();
        uploadContainer.style.borderColor = 'var(--primary-color)';
    });

    uploadContainer.addEventListener('dragleave', function(e) {
        e.preventDefault();
        uploadContainer.style.borderColor = 'var(--border-color)';
    });

    uploadContainer.addEventListener('drop', function(e) {
        e.preventDefault();
        uploadContainer.style.borderColor = 'var(--border-color)';
        const file = e.dataTransfer.files[0];
        fileInput.files = e.dataTransfer.files;
        handleFile(file);
    });

    fileInput.addEventListener('change', function(e) {
        const file = e.target.files[0];
        handleFile(file);
    });

    removeButton.addEventListener('click', function() {
        fileInput.value = '';
        previewContainer.style.display = 'none';
        uploadContainer.style.display = 'block';
    });
});