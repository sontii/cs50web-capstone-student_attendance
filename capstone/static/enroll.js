document.addEventListener('DOMContentLoaded', function() {
    
    // create button group  
    document.querySelector('#button_group').style.display = 'block';
    document.querySelector("#button_group").innerHTML = "";
    const notesbutton = document.createElement('button');
    notesbutton.id = 'notes_button';
    notesbutton.className="btn btn-success";
    notesbutton.innerHTML = 'Notes';
    notesbutton.onclick = function(){notes(id)};
    const spaceChar = document.createTextNode (" ");
    const enrollbutton = document.createElement('button');
    enrollbutton.id = 'enroll_button';
    enrollbutton.className="btn btn-secondary";
    enrollbutton.innerHTML = 'enrolled';
    enrollbutton.addEventListener('click', () => enroll(id));
    document.querySelector('#button_group').append(notesbutton, spaceChar, enrollbutton);

    // vars
    const user_id = JSON.parse(document.getElementById('user_id').textContent);
    const id = JSON.parse(document.getElementById('course_id').textContent);
    const enrollment_id = JSON.parse(document.getElementById('enrollment_id').textContent);
    let enrolled = false;
    const sapce_left = JSON.parse(document.getElementById('space_left_id').textContent);
    var space = parseInt(sapce_left)
    if (space < 1){
      space = 0
    }

    if (course_id){
      if (user_id){       
        if (enrollment_id){
          fetch(`/api/enrollment/${enrollment_id}`)
          .then(response => response.json())
          .then(enrollment => {
            enrollment.forEach(enrollment => {
              // check if user enrolled
              if (enrollment.student_id === user_id){ 
                enrolled = true;
              }

              if (enrolled === true){
                //user already enrolled 
                enrollbutton.className="btn btn-secondary";
                enrollbutton.innerHTML = 'enrolled';
                
              } else {
                // not enrolled
                notesbutton.parentNode.removeChild(notesbutton);
                enrollbutton.innerHTML = 'enroll';
                enrollbutton.className = "btn btn-success";
              }
            });
          });

          } else {
            if (space > 0) {
              // let enroll user
              notesbutton.parentNode.removeChild(notesbutton);
              enrollbutton.className="btn btn-success";
              enrollbutton.innerHTML = 'enroll';
            } else {
              // full course
              notesbutton.parentNode.removeChild(notesbutton);
              enrollbutton.className="btn btn-secondary";
              enrollbutton.innerHTML = 'Course is full';
            }  
         }
      
      } else {
        // no login
        notesbutton.parentNode.removeChild(notesbutton);
        enrollbutton.className="btn btn-info";
        enrollbutton.innerHTML = 'Log in to enroll';
        enrollbutton.addEventListener('click', () => login_form());
      } 
      
    }
});

function notes(id) {
  window.location.href = '../notes/' + id;
}

function login_form() {
  window.location.href = '../login';
}


function enroll(course_id) {
  // store request user
  let enrolled = false
  const user_id = JSON.parse(document.getElementById('user_id').textContent);
  //if user logged?
  if (user_id){
    const enrollment_id = JSON.parse(document.getElementById('enrollment_id').textContent);
    const sapce_left = JSON.parse(document.getElementById('space_left_id').textContent);
    //if enrollment exist?
    if (enrollment_id){
      //exist enrollment id, check user is in enrolled
      fetch(`/api/enrollment/${enrollment_id}`)
        .then(response => response.json())
        .then(enrollment => {
          enrollment.forEach(enrollment => {
            if (enrollment.student_id === user_id){ 
              enrolled = true;
            }
            if (enrolled === true){
              // already enrolled 
              alert('already in this course')
            } else {
              // if no space
              if (sapce_left < 1){
                alert('No space left in this course')
              } else {
                // not enrolled -> put user in enrollment
                fetch(`/api/enrollment/${enrollment_id}`, {
                method: 'PUT',
                headers: {
                  'X-CSRFToken': CSRF_TOKEN,
                },
                  body: JSON.stringify({
                  course_id: course_id,
                  student_id: user_id,
                  })
                })}
              alert('enrolled this course')
              location.reload();
            }
          });
        });

    } else {
      // if no space
      if (sapce_left < 1){
        alert('No space left in this course')
      } else {
      
        //no enroll id so create
      fetch(`/api/enrollment`, {
        method: 'PUT',
        headers: {
          'X-CSRFToken': CSRF_TOKEN,
        },
        body: JSON.stringify({
        course_id: course_id,
        student_id: user_id,
        })
      })
      alert('enrolled this course')
      location.reload();
    }}
    
    } else {
      //user not logged in. redirect log on screen
      window.location.href = '../login';
    }

}
