// to show the tooltip
var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
var tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl)
});

var getImageURL = (byteString) => {
    image = byteString.split('\'')[1]
    return 'data:image/jpeg;base64,' + image
}

// function to send request to server for download files
var sendDownloadRequest = (id, imgType) => {
    var fd = new FormData();
    fd.append('image-id', id);
    fd.append('mode', imgType);

    fetch('/download', { method: 'POST', body: fd })
        .then((res) => {
            return res.blob()
        }).then((results) => {
            console.log(results)

            var file = window.URL.createObjectURL(results);
            console.log(file)
            var a = document.createElement('a');
            a.href = file;
            if (imgType == 'g') {
                a.download = $('#image-filename').html();
            } else {
                a.download = 'c_' + $('#image-filename').html();
            }

            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
        })
}

// on document load getting the image id
$(document).ready(() => {

    var imgId = document.getElementById('image-id').value;

    var formData = new FormData();
    formData.append('image-id', imgId);

    fetch('/getImageData', { method: 'POST', body: formData })
        .then((res) => {
            return res.json()
        })
        .then((result) => {
            console.log(result);

            // getting the values out of results
            fileName = result['file-name'];
            grayImage = result['gray-image'];
            colorImage = result['color-image'];
            timeStamp = result['timeStamp'];

            // rendering the dom
            $("#gray-image").attr('src', getImageURL(grayImage));
            $("#color-image").attr('src', getImageURL(colorImage));
            $('#image-filename').html(fileName);

        });


    // on clickingth

    $("#gray-download").click(() => {
        sendDownloadRequest(imgId, 'g');
    });

    $("#color-download").click(() => {
        sendDownloadRequest(imgId, 'c');
    });

})