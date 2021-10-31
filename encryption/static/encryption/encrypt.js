// application/pdf

const dragArea = document.querySelector(".drag-area")
const dragText = document.querySelector(".header")

function displayFile(){
    let fileType = file.type;
    let validExtensions = ["application/vnd.ms-excel","application/pdf",
                            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"];

    if(validExtensions.includes(fileType)){
        fileName = file.name;
        let fileName_text = document.querySelector(".name-file");
        fileName_text.textContent = fileName;
        document.querySelector(".file-upload").style.display = "block";
    } else{
        alert("Invalid file!!!")
        dragArea.classList.remove("active");
        dragText.textContent = "Drag & Drop";
    }
}

var input = document.querySelector("#input")

input.addEventListener("change", function(){
    file = this.files[0];
    dragArea.classList.add("active");
    displayFile();
})

function deleted_file(){
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

