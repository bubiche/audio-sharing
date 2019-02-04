URL = window.URL;

// stream from getUserMedia()
var gumStream;

// WebAudioRecorder object
var recorder;

// MediaStreamAudioSourceNode we'll be recording
var input;

// selected encoding for result file
var encodingType;

var AudioContext = window.AudioContext || window.webkitAudioContext;
// new audio context to help us record
var audioContext;

var encodingTypeSelect = document.getElementById("encodingSelect");
var recordButton = document.getElementById("recordButton");
var stopButton = document.getElementById("stopButton");

recordButton.addEventListener("click", startRecording);
stopButton.addEventListener("click", stopRecording);

var logDump = document.getElementById("logDump");

//helper log function, show the log inside the 
function __log(e, data) {
  logDump.innerHTML += `\n${e} ${data || ''}`;
}


function startRecording() {

  // See https://addpipe.com/blog/audio-constraints-getusermedia/ for more contraints
  var constraints = { audio: true, video:false }

  navigator.mediaDevices.getUserMedia(constraints).then(function(stream) {
    audioContext = new AudioContext();

    // update format
    document.getElementById("formats").innerHTML = `Format: 2 channel ${encodingTypeSelect.options[encodingTypeSelect.selectedIndex].value} @ ${audioContext.sampleRate/1000}kHz`;

    // assign to gumStream for later use
    gumStream = stream;

    // use the stream for recording
    input = audioContext.createMediaStreamSource(stream);

    encodingType = encodingTypeSelect.options[encodingTypeSelect.selectedIndex].value;

    // we are recording, no more changing encoding type
    encodingTypeSelect.disabled = true;

    recorder = new WebAudioRecorder(input, {
      workerDir: audioRecordLibWorkerPath || '/',
      encoding: encodingType,
      numChannels: 2, //2 is the default, mp3 encoding supports only 2
      onEncoderLoading: function(recorder, encoding) {
        __log(`Loading ${encoding} encoder...`);
      },
      onEncoderLoaded: function(recorder, encoding) {
        __log(`${encoding} encoder loaded`);
      }
    });

    recorder.onComplete = function(recorder, blob) { 
      __log("Encoding complete");
      createDownloadLink(blob, recorder.encoding);
      // Done with record => allow choosing encoding again
      encodingTypeSelect.disabled = false;
    }

    recorder.setOptions({
      timeLimit: 120,
      encodeAfterRecord: true,
      ogg: { quality: 0.5 },
      mp3: { bitRate: 160 }
    });

    __log("Recording started");
    recorder.startRecording();
  }).catch(function(err) {
    // something went wrong => enable record button + disable stop button again
    recordButton.disabled = false;
    stopButton.disabled = true;
  });

  // recording => disable record button + enable stop button
  recordButton.disabled = true;
  stopButton.disabled = false;
}


function stopRecording() {
  // stop microphone access
  gumStream.getAudioTracks()[0].stop();

  // enable record button + disable stop button
  stopButton.disabled = true;
  recordButton.disabled = false;

  // tell the recorder to recording has stop (encode, do its onComplete)
  recorder.finishRecording();
  __log('Recording stopped');
}


function createDownloadLink(blob,encoding) {
  var url = URL.createObjectURL(blob);
  var audio_playback = document.createElement('audio');
  var audio_link = document.createElement('a');
  var li = document.createElement('li');

  //add controls to the <audio> element
  audio_playback.controls = true;
  audio_playback.src = url;

  //link the a element to the blob
  audio_link.href = url;
  audio_link.download = `audio_record (${new Date().toISOString()}).${encoding}`;
  audio_link.innerHTML = audio_link.download;

  //add the new audio and a elements to the li element
  li.appendChild(audio_playback);
  li.appendChild(audio_link);

  //add the li element to the ordered list
  recordingsList.appendChild(li);
}