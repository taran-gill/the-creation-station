navigator.getUserMedia = navigator.getUserMedia ||
						 navigator.webkitGetUserMedia ||
						 navigator.mozGetUserMedia ||
                         navigator.msGetUserMedia;

const MediaStream = window.MediaStream || window.webkitMediaStream;

if (MediaStream && !Reflect.has(MediaStream.prototype, 'stop')) {
    MediaStream.prototype.stop = function() {
        this.getAudioTracks().forEach(function(track) { track.stop(); });
        this.getVideoTracks().forEach(function(track) { track.stop(); });
    };
}