
// Get the record button element
const recordButton = document.getElementById('recordButton');

// Declare necessary variables for recording
let isRecording = false;
let recorder;
let audioChunks = [];
let can_record = false

function speakText(text) {
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = 'ro-RO';  
    utterance.rate = 1.5
    window.speechSynthesis.speak(utterance);
}

toggleMic = () => {
    if (!can_record) return;
    isRecording = !isRecording
    if(isRecording) {
        recorder.start()
        recordButton.textContent = '🔴'; 
    }
    else {
        recorder.stop()
        recordButton.textContent = '🎤';
    }
}

recordButton.addEventListener('click', toggleMic)
function sendAudioToServer(audioBlob) {
    const formData = new FormData();
    formData.append('file', audioBlob, 'audio.mp3');

    fetch("http://localhost:8000/upload-audio", {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        console.log('Audio file uploaded successfully:', data);

        // Populate response box
        
        document.getElementById("problem").textContent = data.problem;
        document.getElementById('problem').textContent += ' '
        if(data.problem == 'personal_loans'){
            document.getElementById('problem').innerHTML += `<a href = "https://www.raiffeisen.ro/ro/persoane-fizice/produsele-noastre/credite/credite-de-nevoi-personale.html">Click pentru mai multe detalii</a>`
        } else if (data.problem == 'withdrawals')
            document.getElementById('problem').innerHTML += `<a href = "https://www.raiffeisen.ro/ro/imm/produse-si-servicii/servicii-electronice/atm-si-multifunctionale.html">Click pentru mai multe detalii</a>`
        else if (data.problem == 'transactions')
            document.getElementById('problem').innerHTML += `<a href = "https://www.raiffeisen.ro/ro/imm/in-sprijinul-tau/asistenta/tranzactii-bancare-online.html">Click pentru mai multe detalii</a>`
        else if (data.problem == 'credit_cards')
            document.getElementById('problem').innerHTML += `<a href = "https://www.raiffeisen.ro/ro/imm/produse-si-servicii/carduri-de-credit.html">Click pentru mai multe detalii</a>`
        else if (data.problem == 'mobile_banking')
            document.getElementById('problem').innerHTML += `<a href = "https://www.raiffeisen.ro/ro/persoane-fizice/produsele-noastre/digital-banking/mobile-banking.html">Click pentru mai multe detalii</a>`
        else if (data.problem == 'saving_accounts')
            document.getElementById('problem').innerHTML += `<a href = "https://www.raiffeisen.ro/ro/persoane-fizice/produsele-noastre/economii.html">Click pentru mai multe detalii</a>`
        document.getElementById("suggestedReading").textContent = data.suggested_reading;
        document.getElementById("sentimentSuggestion").textContent = data.sentiment_and_suggestion;
        document.getElementById("calmDownResponse").textContent = data.calm_down_response;
        sent_sugg_data = data.sentiment_and_suggestion;
        if (sent_sugg_data) {
            let svgIcon = ''; // Placeholder for the SVG icon
            
            if (sent_sugg_data.slice(0, 7) === 'Negativ') {
      
                svgIcon = '<i class="fa-solid fa-face-angry"></i>'
            } else if (sent_sugg_data.slice(0, 6) === 'Neutru') {

                svgIcon = '<i class="fa-solid fa-face-meh"></i>'
            } else {
                svgIcon = '<i class="fa-solid fa-face-smile"></i>'
            }
        
            // Insert the SVG icon into the HTML (assuming an element with ID 'sentiment-icon')
            document.getElementById("sentiment-result").innerHTML = svgIcon;
        }
        // Show the response box
        document.getElementById("responseBox").style.display = "block";
        
        speakText(data['calm_down_response']);
    })
    .catch(error => {
        console.error('Error uploading audio:', error);
    });
}


SetupStream = (stream) => {
    recorder = new MediaRecorder(stream);
    recorder.ondataavailable = e => {
        audioChunks.push(e.data)
    }
   recorder.onstop = e => {
        const blob = new Blob(audioChunks, {type: "audio/wav"})
        audioChunks = []
        const audioURL = window.URL.createObjectURL(blob);
        const messageElement = document.createElement('div');
        messageElement.classList.add('message');

        // Create an audio element
        const audioElement = document.createElement('audio');
        audioElement.controls = true; 
        audioElement.src = audioURL; 
        console.log(blob)
        sendAudioToServer(blob)
        // Append the audio element to the message
        messageElement.appendChild(audioElement);
    
        // Append the message to the chat messages container
        document.getElementById('chatMessages').appendChild(messageElement);

   }
   can_record = true;
}







let SetupAudio = () => {
    console.log("Setting up audio...")
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({
            audio: true
        })
        .then(SetupStream)
        .catch(err => console.error(err))
    }
    console.log("Done")
}

SetupAudio();


SetupStream = (stream) => {
    recorder = new MediaRecorder(stream);
    recorder.ondataavailable = e => {
        audioChunks.push(e.data)
    }
   recorder.onstop = e => {
        const blob = new Blob(chunks, {type: "audio/ogg; codecs=opus"})
        chunks = []
        const audioURL = window.URL.createObjectURL(blob);
        const messageElement = document.createElement('div');
        messageElement.classList.add('message');
    
        // Create an audio element
        const audioElement = document.createElement('audio');
        audioElement.controls = true; 
        audioElement.src = audioURL; 
    
        // Append the audio element to the message
        messageElement.appendChild(audioElement);
    
        // Append the message to the chat messages container
        document.getElementById('chatMessages').appendChild(messageElement);

   }
   can_record = true;
}


toggleMic = () => {
    if (!can_record) return;
    isRecording = !isRecording
    if(isRecording) {
        recorder.start()
        recordButton.textContent = '🔴'; 
    }
    else {
        recorder.stop()
        recordButton.textContent = '🎤';
    }
}
 
// Check if the browser supports the MediaRecorder API
// if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
//     // Set up the audio recording process when the record button is clicked
//     recordButton.addEventListener('click', async function() {
//         if (isRecording) {
//             // Stop the recording if already recording
//             mediaRecorder.stop();
//             recordButton.textContent = '🎤'; // Reset button to microphone icon
//         } else {
//             try {
//                 // Start a new recording session
//                 const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
//                 mediaRecorder = new MediaRecorder(stream);

//                 mediaRecorder.ondataavailable = function(event) {
//                     audioChunks.push(event.data); // Collect audio data
//                 };

//                 mediaRecorder.onstop = async function() {
//                     // When the recording is stopped, process the audio data
//                     const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
//                     const audioUrl = URL.createObjectURL(audioBlob);

//                     // Convert WAV to MP3 using libmp3lame.js
//                     const mp3Blob = await convertWavToMp3(audioBlob);
//                     const mp3Url = URL.createObjectURL(mp3Blob);

//                     // Create an anchor to download the MP3 file
//                     const downloadLink = document.createElement('a');
//                     downloadLink.href = mp3Url;
//                     downloadLink.download = 'recording.mp3';
//                     downloadLink.textContent = 'Download MP3';
//                     document.getElementById('chatMessages').appendChild(downloadLink); // Append link to chat messages

//                     // Reset the audio chunks for the next recording
//                     audioChunks = [];
//                 };

//                 // Start recording
//                 mediaRecorder.start();
//                 recordButton.textContent = '🔴'; // Change button to indicate recording in progress
//             } catch (error) {
//                 console.error('Error accessing audio device:', error);
//                 alert('Could not access the microphone. Please check permissions.');
//             }
//         }

//         // Toggle the recording state
//         isRecording = !isRecording;
//     });
// } else {
//     alert('Your browser does not support audio recording!');
// }

// Function to convert WAV Blob to MP3 using libmp3lame.js

