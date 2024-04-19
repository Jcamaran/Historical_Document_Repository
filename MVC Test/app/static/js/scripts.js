document.addEventListener('DOMContentLoaded', function() {
    const files = document.querySelectorAll('.file');
    let delay = 0;
    files.forEach(file => {
        file.style.opacity = 0;
        file.style.transition = 'opacity 0.5s ease-out';
        setTimeout(() => {
            file.style.opacity = 1;
        }, delay);
        delay += 100; // Each file fades in 100ms after the previous one
    });
});

document.querySelectorAll('.gallery img').forEach(img => {
    img.addEventListener('click', function() {
        const modal = document.createElement('div');
        modal.style.position = 'fixed';
        modal.style.left = '0';
        modal.style.top = '0';
        modal.style.width = '100%';
        modal.style.height = '100%';
        modal.style.backgroundColor = 'rgba(0, 0, 0, 0.8)';
        modal.style.display = 'flex';
        modal.style.justifyContent = 'center';
        modal.style.alignItems = 'center';
        modal.style.zIndex = '1000';

        const modalImg = document.createElement('img');
        modalImg.src = this.src;
        modalImg.style.maxHeight = '80%';
        modalImg.style.maxWidth = '80%';
        modal.style.cursor = 'pointer';

        modal.appendChild(modalImg);
        document.body.appendChild(modal);

        modal.addEventListener('click', function() {
            this.parentElement.removeChild(this);
        });
    });
});

document.querySelector('form').addEventListener('submit', function(e) {
    e.preventDefault(); // Prevent the actual form submission
    const loadingText = document.createElement('div');
    loadingText.textContent = 'Uploading... Please wait.';
    this.appendChild(loadingText);
    
    setTimeout(() => {
        loadingText.textContent = 'Uploaded Successfully!';
    }, 1500); // Simulate upload time
});
