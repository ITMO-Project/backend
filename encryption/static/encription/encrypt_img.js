// Add modal
var modal = document.getElementById("myModal");
var span = document.getElementsByClassName("close")[0];

span.onclick = function() {          
    modal.style.display = "none";
}

window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}

function changeImage(id){
    modal.style.display ="block";
    let img = document.getElementById(id);
    let srcImg = img.getAttribute("src");
    let nameImg = img.getAttribute("name")
    let imgMain = document.getElementById("main");

    imgMain.setAttribute("src", srcImg);
    imgMain.setAttribute("name", nameImg);
}


function choise(){
    let srcImgMain = document.getElementById("main").getAttribute("src");
    modal.style.display = "none";
    dragArea.classList.add("active"); 
    img = document.querySelector("#img")
    img.setAttribute('src',srcImgMain) 
    document.querySelector(".img").style.display = "block";             
}

// Delete image

function deleted(){
    let img = document.querySelector(".img")
    img.setAttribute('src', "")
    img.style.display ="none"
    dragArea.classList.remove("active");
    dragText.textContent = "Drag & Drop"
}

// Upload image
const dragArea = document.querySelector(".drag-area");
const dragText = document.querySelector(".header");

var button  = document.querySelector(".button")
var input = document.querySelector("#input")



function displayFile(){
    let fileType = file.type;
    let validExtensions = ["image/jpeg","image/jpg", "image/png"];

    if(validExtensions.includes(fileType)){
        let fileReader = new FileReader();

        fileReader.onload = () =>{
            let fileURL = fileReader.result;
            document.querySelector("#img").setAttribute('src', fileURL);
            document.querySelector(".img").style.display = "block";
        };
        fileReader.readAsDataURL(file);
    } else{
        alert("This file is not an Image!!!");
        dragArea.classList.remove("active");
        dragText.textContent = "Drag & Drop";
    }
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


// Slideshow

function plusSlides(n) {
    let nameDir = {"one":1, "two":2, "three":3, "four":4, "five":5, "six":6, "seven":7, "eight":8}
    let imgName = document.getElementById("main").getAttribute("name");
    let slideIndex = nameDir[imgName];

    showSlides(slideIndex += n);
}

function showSlides(n){
    let slideIndex;

    if(n==9){
        slideIndex = 1;
        slidecurrent = 8;
    }else if(n==0){
        slideIndex = 8;
    } else{
        slideIndex = n;
    }
    let idDir = {1:"one", 2: "two", 3:"three", 4:"four", 5:"five", 6:"six", 7:"seven", 8:"eight"}
    let idImg = idDir[slideIndex];
    let srcImg = document.getElementById(idImg).getAttribute('src');
    let nameImg = document.getElementById(idImg).getAttribute('name');
    let imgMain = document.getElementById("main");

    imgMain.setAttribute('src', srcImg);
    imgMain.setAttribute('name', nameImg);
}