//selecting all required elements
const dropArea = document.getElementById("drag_Area");
console.log(dropArea);
const dragText = document.getElementById("drag_Text");
const button = document.getElementById("browse-button");
const input = document.getElementById("input-file");
const upload_form_wrapper = document.getElementById("upload-form-wrapper");
const fileName = document.getElementById("filename");
const submit_btn = document.getElementById("grey-submit");
const reset_btn = document.getElementById("grey-reset");
const input_reset = document.getElementById("reset-hidden");
const img_container = document.getElementById("image-container");
//const input_img = document.getElementById("input-img");
console.log(fileName);
let file; //this is a global variable and we'll use it inside multiple functions

console.log(dragText);
console.log(button);
console.log(input);

console.log(dropArea);

button.onclick = ()=>{
  input.click(); //if user click on the button then the input also clicked
}

reset_btn.onclick = ()=>{
  input_reset.click(); //if user click on the button then reset form
  file = null;
  showFile();
  upload_form_wrapper.style.display="none";
  //dropArea.innerHTML = null;
  console.log(document.querySelector("#drag_Area"))
}

input.addEventListener("change", function(){
  //getting user select file and [0] this means if user select multiple files then we'll select only the first one
  file = this.files[0];
  dropArea.classList.add("active");
  showFile(); //calling function
});


//If user Drag File Over DropArea
dropArea.addEventListener("dragover", (event)=>{
  event.preventDefault(); //preventing from default behaviour
  dropArea.classList.add("active");
  dragText.textContent = "Release to Upload File";
});

//If user leave dragged File from DropArea
dropArea.addEventListener("dragleave", ()=>{
  dropArea.classList.remove("active");
  dragText.textContent = "Drag & Drop to Upload File";
});

//If user drop File on DropArea
dropArea.addEventListener("drop", (event)=>{
  event.preventDefault(); //preventing from default behaviour
  //getting user select file and [0] this means if user select multiple files then we'll select only the first one
  file = event.dataTransfer.files[0];
  showFile(); //calling function
});

function showFile(){
  if(file == null){
    dropArea.classList.remove("active");
    fileName.innerHTML = "this contain filename";
    dropArea.style.display = "flex";
    img_container.innerHTML = null;
    img_container.style.display = "none";
  }
  else{
    let fileType = file.type; //getting selected file type
    let validExtensions = ["image/jpeg", "image/jpg", "image/png"]; //adding some valid image extensions in array
    if(validExtensions.includes(fileType)){ //if user selected file is an image file
      upload_form_wrapper.style.display="block";
      let fileReader = new FileReader(); //creating new FileReader object
      fileReader.onload = ()=>{
        let fileURL = fileReader.result; //passing user file source in fileURL variable
          // UNCOMMENT THIS BELOW LINE. I GOT AN ERROR WHILE UPLOADING THIS POST SO I COMMENTED IT
        let imgTag = `<img src="${fileURL}" alt="image" style="width:300px;height:300px">`; //creating an img tag and passing user selected file source inside src attribute
        //dropArea.innerHTML = imgTag; //adding that created img tag inside dropArea container
        dropArea.style.display = "none";
        img_container.innerHTML = imgTag;
        img_container.style.display = "flex";
      }
      fileName.innerHTML = file.name;
      fileReader.readAsDataURL(file);
    }else{
      alert("This is not an Image File!");
      dropArea.classList.remove("active");
      dragText.textContent = "Drag & Drop to Upload File";
    }
  }
}