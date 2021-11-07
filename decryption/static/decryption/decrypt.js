// Upload image
const dragArea = document.querySelector(".drag-area");
const dragText = document.querySelector(".header");

var button  = document.querySelector(".button")
var input = document.querySelector("#input")



function displayFile(){
    let fileType = file.type;
    let validExtensions = ["image/jpeg","image/jpg", "image/png"];

//    if(validExtensions.includes(fileType)){
        let fileReader = new FileReader();

        fileReader.onload = () =>{
            let fileURL = fileReader.result;
            document.querySelector("#img").setAttribute('src', fileURL);
            document.querySelector(".img").style.display = "block";
        };
        fileReader.readAsDataURL(file);
//    } else{
//        alert("This file is not an Image!!!");
//        dragArea.classList.remove("active");
//        dragText.textContent = "Drag & Drop";
//    }
}

input.addEventListener("change", function(){
    file = this.files[0]
    dragArea.classList.add("active")
    displayFile();
})

dragArea.addEventListener("dragover", (event) =>{
    event.preventDefault();
    dragText.textContent = "Release to Upload";
    dragArea.classList.add("active");
})

dragArea.addEventListener("dragleave", (event) =>{
    event.preventDefault();
    dragText.textContent = "Drag & Drop";
    dragArea.classList.remove("active");
})

dragArea.addEventListener("drop", (event) =>{
    event.preventDefault();
    file = event.dataTransfer.files[0];
    displayFile();
})


// Delete image
function deleted(){
    let img = document.querySelector(".img")
    img.setAttribute('src',"")
    img.style.display ="none"
    dragArea.classList.remove("active");
    dragText.textContent = "Drag & Drop"
}