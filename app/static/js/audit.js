

function clearLogs(){

    if(!confirm("Clear all audit logs?")){
        return;
    }

    fetch("/audit/clear", {
        method:"POST"
    })
    .then(response => response.json())
    .then(data => {

        if(data.success){
            alert("Audit logs cleared");
            location.reload();
        }

    })
    .catch(error=>{
        console.log(error);
        alert("Failed to clear logs");
    });

}
