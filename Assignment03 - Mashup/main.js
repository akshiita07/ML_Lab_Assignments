document.querySelector('form').addEventListener('submit', function (e) {
    e.preventDefault();  // Prevent the default form submission behavior
  
    // Gather the form inputs
    const singer = document.querySelector('input[type="text"]').value;
    const numVideos = document.querySelector('input[type="number"]:nth-of-type(1)').value;
    const duration = document.querySelector('input[type="number"]:nth-of-type(2)').value;
    const email = document.querySelector('input[type="email"]').value;
  
    // Check if all fields are filled
    if (!singer || !numVideos || !duration || !email) {
      alert('Please fill in all fields!');
      return;
    }
  
    // Create an object with the form data
    const formData = {
      singer: singer,
      num_videos: parseInt(numVideos),
      audio_duration: parseInt(duration),
      email: email
    };
  
    // Send the data to the server
    fetch('http://localhost:8080/mashup', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(formData),  // Convert the form data to JSON
    })
    .then(response => response.json())
    .then(data => {
      // Provide feedback to the user
      if (data.message) {
        alert(data.message);
      } else {
        alert('Mashup creation failed.');
      }
    })
    .catch(error => {
      console.error('Error:', error);
      alert('An error occurred while generating the mashup.');
    });
  });
  