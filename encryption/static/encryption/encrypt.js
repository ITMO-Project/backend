// application/pdf

const dragArea = document.querySelector(".drag-area")
const dragText = document.querySelector(".header")

function displayFile(){
    fileName = file.name;
    let fileName_text = document.querySelector(".name-file");
    fileName_text.textContent = fileName;
    document.querySelector(".file-upload").style.display = "block";
}

var input = document.querySelector("#input")

input.addEventListener("change", function(){
    file = this.files[0];
    dragArea.classList.add("active");
    displayFile();
})

function deleted_file(){
    input.value = "";
    file = "";
    dragArea.classList.remove('active');
    document.querySelector(".file-upload").style.display = "none"
}

dragArea.addEventListener("dragover", (e)=>{
    e.preventDefault();
    dragArea.classList.add('active');
    dragText.textContent = "Release to Upload";
})

dragArea.addEventListener("dragleave", (e)=>{
    e.preventDefault();
    dragArea.classList.remove('active');
    dragText.textContent = "Drag & Drop";
})

dragArea.addEventListener("drop", (e)=>{
    e.preventDefault();
    file = e.dataTransfer.files[0];
    displayFile();
})

