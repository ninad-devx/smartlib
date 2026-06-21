
function clearRFIDActivity(){

    if(!confirm(
        "Clear recent RFID activity?"
    )){
        return;
    }


    fetch(
        "/rfid/clear",
        {
            method:"POST",
            headers:{
                "Content-Type":"application/json"
            }
        }
    )
    .then(response => response.json())
    .then(data => {


        if(data.success){

            alert(
                "RFID activity cleared"
            );

            location.reload();

        }
        else{

            alert(
                "Failed to clear RFID activity"
            );

        }


    })
    .catch(error=>{

        console.log(error);

        alert(
            "RFID clear error"
        );

    });


}
