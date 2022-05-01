//selecting all required elements
const dropArea = document.getElementById("drag_Area");
const dragText = document.getElementById("drag_Text");
const browse_btn = document.getElementById("browse-button");
const inputFile = document.getElementById("input-file");
const upload_form_wrapper = document.getElementById("upload-form-wrapper");
const fileName = document.getElementById("filename");
const upload_btn = document.getElementById("grey-submit");
const reset_btn = document.getElementById("grey-reset");
const img_container = document.getElementById("image-container");
const fileSize = document.getElementById("file-size");
const imageId = document.getElementById('image-id');
const sumbitId = document.getElementById('image-id-submit');

let imageFile = null; // variable to hold the imageFile information
let imageDataName = 'image-file'; // variable to hold the identifier of the image file
let formData = new FormData(); // this is global variable to hold the form data

let debug = true // for debugging 

// default image id value 
imageId.value = "";


// function to popup the alertModal 
export var popupModal = (modalTitle, modalMsg) => {
    $('#modal-title').html(modalTitle);
    $('#modal-body').html(modalMsg);
    $('#alertModal').modal('show');
}


// * Drag and drop utility

// when user drag file into the drag-drop aread
dropArea.addEventListener('dragover', (event) => {
    event.preventDefault();
    dropArea.classList.add('active');
    dragText.innerHTML = "Release to Upload File";
});

// when user leave the drag-drop aread without dropping file
dropArea.addEventListener('dragleave', (event) => {
    event.preventDefault();
    dropArea.classList.remove('active');
    dragText.innerHTML = "Drag & Drop to Upload File";
});

// when user drop the drop the file into the drag-drop aread
dropArea.addEventListener('drop', (event) => {
    event.preventDefault();
    // if user drop multiple files selecting the first file only
    var fileData = event.dataTransfer.files[0];
    if (debug) {
        console.log('dropArea onChange() => ')
        console.log('dropArea drop : ', fileData);
        console.log('gray-image : ', formData.get(imageDataName))
    }
    showImageFile(fileData);
});


// function to format bytes for size of the file
var formatBytes = (bytes, decimals = 2) => {
    if (bytes === 0) return '0 Bytes';

    const k = 1024;
    const dm = decimals < 0 ? 0 : decimals;
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];

    const i = Math.floor(Math.log(bytes) / Math.log(k));

    return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
}

// inputFile when selected the file 
inputFile.addEventListener('change', () => {

    // getting the first file selected from the input files
    imageFile = inputFile.files[0];

    // setting the FormData
    showImageFile(imageFile);

    if (debug) {
        console.log('inputFile onChange() => ')
        console.log('inputFile change : ', imageFile);
        console.log('gray-image : ', formData.get(imageDataName))
    }
});

// on click browse btn 
browse_btn.addEventListener('click', (event) => {
    inputFile.click();
});

// on clicking the reset btn 
reset_btn.addEventListener('click', () => {
    if (formData.has(imageDataName)) {
        formData.delete(imageDataName);
        showImageUploadBar(false);
    }
    if (debug) {
        console.log('reset-btn onChange() => ');
        console.log('FormData : ', formData.has(imageDataName));
    }
    imageId.value = "";
    dragText.innerHTML = "Drag & Drop to Upload File";
    dropArea.classList.remove('active');
});


// function to show the image upload bar
var showImageUploadBar = (flag) => {

    if (!flag) { // hiding the image upload bar
        dropArea.style.display = "flex";
        dragText.innerHTML = "Drag & Drop to Upload File";
        img_container.style.display = "none";
        img_container.classList.remove('active');
        dropArea.classList.remove('active');
        upload_form_wrapper.style.display = "none";
    } else { // showing the image upload bar
        dropArea.style.display = "none";
        img_container.style.display = "block";
        img_container.classList.add('active');
        upload_form_wrapper.style.display = "block";
    }
}

// function to check whether the file is of image supported image types or not
var isValidImageFile = (file) => {
    if (file == null) return false; // checking the file is null or not

    let validExtensions = ["image/jpeg", "image/jpg", "image/png"];
    let imageExtension = file.type;

    if (validExtensions.includes(imageExtension))
        return true;
    return false;
}

// function to show the image 
var displayImage = (imgFile) => {
    let fileReader = new FileReader();
    fileReader.onload = () => {
        let fileURL = fileReader.result;
        //creating an img tag and passing user selected file source inside src attribute
        let imgTag = `<img src="${fileURL}" alt="image" style="width:100%;height:300px;object-fit: contain">`;
        img_container.innerHTML = imgTag;
    }
    fileReader.readAsDataURL(imgFile);
}

// function to display the selected file 
var showImageFile = (imageFile = null) => {
    if (imageFile == null) {
        // hiding the image upload bar
        showImageUploadBar(false);

        if (debug)
            console.log('There is no Image selected');
    } else {

        if (isValidImageFile(imageFile)) {
            //showing the image upload bar
            displayImage(imageFile);
            fileName.innerHTML = imageFile.name;
            fileSize.innerHTML = formatBytes(imageFile.size);

            // adding image to the formdata
            if (formData.has(imageDataName)) {
                if (debug)
                    console.log('Updating the imageData')
                formData.set(imageDataName, imageFile);
            } else {
                if (debug)
                    console.log('Adding the imageData')
                formData.append(imageDataName, imageFile);
            }

            // showing the image info
            showImageUploadBar(true);

            if (debug) {
                console.log('Image has been selected');
                console.log('imageFile size : ', imageFile.size);
            }

        } else {
            popupModal('Uploaded file is not a valid image', 'Only JPG, PNG and GIF files are allowed.');
        }
    }
}

// function to show the loading tag
var showLoading = (flag) => {

    if (flag) { // if true then show the loading 
        $(reset_btn).hide();
        $(upload_btn).hide();
        $('#loading-tag').show();

    } else { // else hide the loading
        $(reset_btn).show();
        $(upload_btn).show();
        $('#loading-tag').hide();
    }

}

// onclick the file upload button
upload_btn.addEventListener('click', (event) => {
    event.preventDefault();

    if (formData.has(imageDataName)) {
        showLoading(true);
        // sending request to the server to colorize the image 
        fetch('/colorize', { method: 'POST', body: formData })
            .then(res => {
                if (debug) {
                    // console.log('response : ', res.status);
                    return res.json();
                }
            })
            .then(result => {
                console.log(result.body);
                console.log('status : ', result['status']);
                if (result['status'] < 0) {
                    popupModal('Invalid Image', 'Given is the Color Image, Please upload a B/W Image');
                    formData.delete(imageDataName);
                    showImageFile();
                    showLoading(false);
                } else {
                    // popupModal('Success', 'Image has been uploaded successfully');
                    imageId.value = result['uid'];
                    sumbitId.click();
                }
            });

    } else {
        popupModal('No Image is Selected', 'Please Select the Image')
    }

    if (debug) {
        console.log('Upload Btn : Clicked');
    }
});