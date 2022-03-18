function updateButton(enrollment_id) {
    var grade = document.getElementById(enrollment_id).value
    if (grade < 0 || grade > 101) {
        alert('Only numbers between 0 and 100')
        location.reload();
    } else {
    
    fetch(`/api/grades/${enrollment_id}`,{
        method: 'PUT',
        headers: {
        'X-CSRFToken': CSRF_TOKEN,
        },
        body: JSON.stringify({
        enrollment_id: enrollment_id,
        grade: grade,
        })
        })
        .then(response => response.json())
        .then(result => {
            if ("message" in result) {
            // The grade saved successfully!
            myAlert = document.querySelector('#myAlert');
            const alert = document.createElement('div');
            alert.className="text-center alert alert-success";
            alert.innerHTML = result['message'];
            myAlert.appendChild(alert)
            }
            if ("error" in result) {
            myAlert = document.querySelector('#myAlert');
            const alert = document.createElement('div');
            alert.className="text-center alert alert-danger";
            alert.innerHTML = result['error'];
            myAlert.appendChild(alert)
            }
        });
        window.clearTimeout()
        /* location.reload(); */
    }

}