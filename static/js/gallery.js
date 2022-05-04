// convert base64 to image url
const getImageURL = (byteString) => {
    return 'data:image/jpeg;base64,' + byteString.split('\'')[1];
}

// to show the tooltips accross the page
const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
const tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
});

// gettting the searchbar 
const searchBar = document.getElementById('search-bar');

// getting the btns
const previousBtn = document.getElementById('previous-btn');
const nextBtn = document.getElementById('next-btn');
const pageNo = document.getElementById('page-number');
const totalPageNo = document.getElementById('total-page-number');

// getting all the delete and show images btns
const deleteBtnList = document.querySelectorAll('.deleteBtn');
const showBtnList = document.querySelectorAll('.showBtn');

// function to send request to the server for images using page no
var sendGetImagesRequest = (currentPageNo) => {
    var fd = new FormData()
    fd.append('page-no', currentPageNo)

    // sending request to the server to send the images
    fetch('/getUserImages', { method: 'POST', body: fd })
        .then(res => {
            return res.json();
        }).then(results => {
            console.log(results);

            // getting the content out of result
            let fileCount = results['fileCount'];
            let pageCount = results['pageCount'];
            let imageData = results['data'];

            renderImageGrid(cardViewList, imageData);

            renderPageNavigationBar(currentPageNo, pageCount);
        });
}

// getting the all cardview template
var cardViewList = document.querySelectorAll('div.cardView.m-4');

// function to render the cardview
var renderCardView = (cardView, imgList) => {
    let fileName = cardView.getElementsByTagName('span')[0];
    let grayImg = cardView.getElementsByTagName('img')[0];
    let colorImg = cardView.getElementsByTagName('img')[1];
    let imgId = cardView.getElementsByTagName('input')[0];
    let uDate = cardView.getElementsByTagName('span')[1];
    let utime = cardView.getElementsByTagName('span')[2];


    // updating dom
    $(fileName).html(imgList['filename']);
    $(grayImg).attr('src', getImageURL(imgList['grayImg']));
    $(colorImg).attr('src', getImageURL(imgList['colorImg']));
    $(imgId).val(imgList['uid']);
    $(uDate).html(imgList['upload-date']);
    $(utime).html(imgList['upload-time']);

    cardView.classList.remove('hide');
}

// function to clear the cardView data
var clearImageGrid = (cardViews) => {
    cardViews.forEach((card) => {
        let fileName = card.getElementsByTagName('span')[0];
        let grayImg = card.getElementsByTagName('img')[0];
        let colorImg = card.getElementsByTagName('img')[1];
        let imgId = card.getElementsByTagName('input')[0];
        let uDate = card.getElementsByTagName('span')[1];
        let utime = card.getElementsByTagName('span')[2];

        // setting the src to empty string
        $(fileName).html('Image Name')
        $(grayImg).attr('src', '');
        $(colorImg).attr('src', '');
        $(imgId).val(-99999999999);
        $(uDate).html('DD MM YYYY');
        $(utime).html('HH:MM AM');


        // hiding the card
        card.classList.add('hide');
    });
}

// function to render the image gird 
var renderImageGrid = (cards, images) => {
    clearImageGrid(cards);
    for (var i = 0; i < images.length; i++) {
        renderCardView(cards[i], images[i]);
    }
}


pageNo.addEventListener('focusout', () => {
    if (pageNo.value == "") {
        pageNo.value = (1).toString();
    }

    pageNo.dispatchEvent(new Event('change'));
});

// function to render the pagnavigation bar
var renderPageNavigationBar = (currentPageNo, totalPages) => {

    $(pageNo).val(currentPageNo);
    $(totalPageNo).val(totalPages);

    if (currentPageNo == 1) {
        $(previousBtn).hide();
    } else {
        $(previousBtn).show();
    }

    if (totalPages == 1 || currentPageNo >= totalPages) {
        $(nextBtn).hide();
    } else {
        $(nextBtn).show();
    }


}



$(document).ready(() => {

    searchBar.disabled = false;


    // rendering
    // renderImageGrid(cardViewList, imgList);


    pageNo.addEventListener('change', () => {

        let pageNum = parseInt(pageNo.value);
        let totalPages = parseInt(totalPageNo.value);

        // hiding the previous btn if page no is 1 or less than 1
        if (pageNum <= 1) {
            pageNo.value = (1).toString();
        }

        // hiding the previous btn if page no is total page
        if (pageNum >= parseInt(totalPageNo.value)) {
            pageNo.value = totalPageNo.value;
        }

        renderPageNavigationBar(pageNum, totalPages);

        sendGetImagesRequest(pageNum);

    });

    //  on click previous btn decrement the page no
    previousBtn.addEventListener('click', () => {

        let pageNum = parseInt(pageNo.value)

        if (pageNum <= 1) {
            pageNo.value = (1).toString();
        } else {
            pageNo.value = (pageNum - 1).toString();
        }

        // triggering the change event
        pageNo.dispatchEvent(new Event('change'));

    });

    //  on click next btn increment the page no
    nextBtn.addEventListener('click', () => {

        let pageNum = parseInt(pageNo.value);
        let totalPageNum = parseInt(totalPageNo.value);

        if (pageNum >= totalPageNum) {
            pageNo.value = (totalPageNum).toString();
        } else {
            pageNo.value = (pageNum + 1).toString();
        }

        // triggering the change event
        pageNo.dispatchEvent(new Event('change'));

    });


    sendGetImagesRequest(1);


    // for each item in the deleteBtnList
    deleteBtnList.forEach((btn) => {

        // if the btn is clicked
        btn.addEventListener('click', (event) => {

            // getting the image id within the parent
            imageId = btn.parentElement.getElementsByTagName('input')[0].value;
            console.log(imageId);
        });
    });


    // for each item in the showBtnList
    showBtnList.forEach((btn) => {

        // if the show btn is clicked
        btn.addEventListener('click', (event) => {

            // getting the image id within the parent
            imageId = btn.parentElement.getElementsByTagName('input')[0].value;
            console.log(imageId);
        });
    });


});