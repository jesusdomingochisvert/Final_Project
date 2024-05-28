// const dropZone = document.getElementById('drop-zone');
// const fileUpload = document.getElementById('fileUpload');
// let isProcessing = false;

// document.body.addEventListener('dragover', (event) => {
//     event.preventDefault();
//     dropZone.classList.add('dragging');
// });

// document.body.addEventListener('dragleave', (event) => {
//     if (!event.relatedTarget || !dropZone.contains(event.relatedTarget)) {
//         dropZone.classList.remove('dragging');
//     }
// });

// document.body.addEventListener('drop', (event) => {
//     event.preventDefault();
//     dropZone.classList.remove('dragging');
//     if (dropZone.contains(event.target)) {
//         const files = event.dataTransfer.files;
//         handleFiles(files);
//     }
// });

// dropZone.addEventListener('dragover', (event) => {
//     event.preventDefault();
//     dropZone.classList.add('dragging');
// });

// dropZone.addEventListener('dragleave', (event) => {
//     dropZone.classList.remove('dragging');
// });

// dropZone.addEventListener('drop', (event) => {
//     event.preventDefault();
//     dropZone.classList.remove('dragging');
//     const files = event.dataTransfer.files;
//     handleFiles(files);
// });

// fileUpload.addEventListener('change', () => {
//     const files = fileUpload.files;
//     handleFiles(files);
// });

// function handleFiles(files) {
//     if (isProcessing) return; // limitar a un proceso

//     for (const file of files) {
//         if (file.type === 'image/jpeg' || file.type === 'image/png') {
//             isProcessing = true;
//             uploadAndProcessImage(file);
//         } else {
//             alert('Formato no admitido. Por favor, selecciona una imagen JPG o PNG.');
//         }
//     }
// }

// function uploadAndProcessImage(file) {
//     const formData = new FormData();
//     formData.append('image', file);

//     fetch('/api/process_images', {
//         method: 'POST',
//         body: formData
//     })
//     .then(response => response.json())
//     .then(data => {
//         if (data.error) {
//             alert('Error: ' + data.error);
//         } else {
//             const processedImagePath = data.processed_image_path;
//             const prcesedTotal_time = data.total_time;
//             openImageInPopup(processedImagePath, prcesedTotal_time);
//         }
//     })
//     .catch(error => {
//         console.error('Error:', error);
//         alert('Error al procesar la imagen.');
//     })
//     .finally(() => {
//         isProcessing = false; // dejar uploads nuevos
//     });
// }

// function openImageInPopup(imagePath, ttime) {
//     const popup = window.open('', '_blank', 'width=800,height=600');
//     popup.document.write(`<h2>Tiempo ejecución: "${ttime}"</h2><br><img src="${imagePath}" alt="Imagen Procesada" style="max-width: 100%; height: auto;">`);
// }


const dropZone = document.getElementById('drop-zone');
const fileUpload = document.getElementById('fileUpload');
let isProcessing = false;

document.body.addEventListener('dragover', (event) => {
    event.preventDefault();
    dropZone.classList.add('dragging');
});

document.body.addEventListener('dragleave', (event) => {
    if (!event.relatedTarget || !dropZone.contains(event.relatedTarget)) {
        dropZone.classList.remove('dragging');
    }
});

document.body.addEventListener('drop', (event) => {
    event.preventDefault();
    dropZone.classList.remove('dragging');
    if (dropZone.contains(event.target)) {
        const files = event.dataTransfer.files;
        handleFiles(files);
    }
});

dropZone.addEventListener('dragover', (event) => {
    event.preventDefault();
    dropZone.classList.add('dragging');
});

dropZone.addEventListener('dragleave', (event) => {
    dropZone.classList.remove('dragging');
});

dropZone.addEventListener('drop', (event) => {
    event.preventDefault();
    dropZone.classList.remove('dragging');
    const files = event.dataTransfer.files;
    handleFiles(files);
});

fileUpload.addEventListener('change', () => {
    const files = fileUpload.files;
    handleFiles(files);
});

function handleFiles(files) {
    if (isProcessing) return; // Limitar a un proceso

    for (const file of files) {
        if (file.type === 'image/jpeg' || file.type === 'image/png') {
            isProcessing = true;
            uploadAndProcessImage(file);
        } else {
            alert('Formato no admitido. Por favor, selecciona una imagen JPG o PNG.');
        }
    }
}

function uploadAndProcessImage(file) {
    const formData = new FormData();
    formData.append('image', file);

    fetch('/api/process_images', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert('Error: ' + data.error);
        } else {
            const processedImagePath = data.processed_image_path;
            const processedTotalTime = data.total_time;
            openImageInPopup(processedImagePath, processedTotalTime);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error al procesar la imagen.');
    })
    .finally(() => {
        isProcessing = false; // Dejar subir nuevos
    });
}

function openImageInPopup(imagePath, totalTime) {
    const popup = window.open('', '_blank', 'width=800,height=600');
    popup.document.write(`<h2>Tiempo de ejecución: ${totalTime} segundos</h2><br><img src="${imagePath}" alt="Imagen Procesada" style="max-width: 100%; height: auto;">`);
}