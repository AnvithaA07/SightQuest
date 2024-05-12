function handleFileSelect(event) {
    const files = event.target.files;
    if (files.length > 0) {
        const file = files[0];
        // Here you can do something with the selected file
    }
}

function handleDrop(event) {
    event.preventDefault();
    const files = event.dataTransfer.files;
    if (files.length > 0) {
        const file = files[0];
        // Here you can do something with the dropped file
    }
}

document.getElementById('uploadForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const formData = new FormData(this);
    const option = document.querySelector('input[name="option"]:checked').value;
    fetch('/process', {
        method: 'POST',
        body: formData
    })
    .then(response => response.text())
    .then(result => {
        document.getElementById('output').value = result;
    })
    .catch(error => console.error('Error:', error));
});

// This function prevents the default behavior of dragging files onto the browser window
function handleDragOver(event) {
    event.preventDefault();
}
