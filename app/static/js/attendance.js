
function filterTable(){

    const value =
        document
        .getElementById("search")
        .value
        .toLowerCase();


    const rows =
        document.querySelectorAll(
            "#attendanceTable tbody tr"
        );


    rows.forEach(row=>{

        const text =
            row.innerText.toLowerCase();


        row.style.display =
            text.includes(value)
            ? ""
            : "none";

    });

}



function clearAttendance(){

    if(!confirm(
        "Clear all attendance logs?"
    )){
        return;
    }


    fetch(
        "/attendance/clear",
        {
            method:"POST",
            headers:{
                "Content-Type":"application/json"
            }
        }
    )
    .then(response=>response.json())
    .then(data=>{


        if(data.success){

            alert(
                "Attendance logs cleared"
            );


            location.reload();

        }
        else{

            alert(
                "Clear failed"
            );

        }

    })
    .catch(error=>{

        console.log(error);

        alert(
            "Failed to clear attendance"
        );

    });

}


