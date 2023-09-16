<script>
    let audioStream;
    let isRecording = false;
    let mediaRecorder;
    let audioChunks = [];
    let audioBlob;

    export let onMicStop;


    async function startMic() {
      try {

        audioChunks = [];
        
        audioStream = await navigator.mediaDevices.getUserMedia({ audio: true });
  
        // Setup the MediaRecorder and its event listeners
        mediaRecorder = new MediaRecorder(audioStream);
        mediaRecorder.ondataavailable = event => {
          audioChunks.push(event.data);
        };
  
        mediaRecorder.onstop = () => {
          audioBlob = new Blob(audioChunks, { type: 'audio/wav' });

          onMicStop(audioBlob);
        };

        // Start recording
              
        mediaRecorder.start();
        isRecording = true;

        

      } catch (error) {
        console.error("Error accessing the microphone:", error);
      }
    }
  
    function stopMic() {
      if (mediaRecorder && mediaRecorder.state !== 'inactive') {
        mediaRecorder.stop();
        isRecording = false;
  

        if (audioStream) {
          let tracks = audioStream.getTracks();
          tracks.forEach(track => track.stop());
        }

        

      }
    }
  </script>
  
  <button on:click={isRecording ? stopMic : startMic}>
    {isRecording ? 'Stop Mic' : 'Start Mic'}
  </button>
  
  