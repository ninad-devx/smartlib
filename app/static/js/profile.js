
async function startRFIDLink(alertMessage){

    try{

        const user_id =
            document.getElementById("user_id").value;

        const response = await fetch(
            `/api/rfid/start-link?user_id=${user_id}`,
            {
                method:"POST"
            }
        );

        const data =
            await response.json();

        if(response.ok){

            alert(alertMessage);

        }else{

            alert(
                data.message ||
                "Something went wrong"
            );

        }

    }catch(error){

        console.error(error);

        alert("Server Error");

    }

}

document
.getElementById("linkBtn")
.addEventListener("click", ()=>{

    startRFIDLink(
        "Scan RFID Card"
    );

});

document
.getElementById("replaceBtn")
.addEventListener("click", ()=>{

    startRFIDLink(
        "Scan New RFID Card"
    );

});

