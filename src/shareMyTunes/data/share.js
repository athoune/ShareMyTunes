$(
function() {
	var soundReady = false;
	var playing = null;
	//console.log($("#q").val());
	$('#query').submit(function() {
		$.ajax({
			'url'     : 'query',
			'data'    : {'q': $("#q").val()},
			'dataType': 'json',
			'success' : function(data) {
				$('#responses').empty();
				for(var a=0; a < data.length; a++) {
					var link = $('<a class="music">');
					link.attr('href', 'track/' + data[a].docNum + '/music');
					link.attr('id', 'track_' + data[a].docNum)
					link.click(function() {
						var that = $(this);
						var id = that.attr('id');
						if(playing != null){
							soundManager.stop(playing);
							playing == null;
						}
						if (playing != id) {
							console.log("play " + id);
							soundManager.play(id, that.attr('href'));
							playing = id;
						}
						return false;
					});
					$('#responses')
						.append($("<li>")
							.text(data[a].name).append(
								link.append($('<img class="artwork"/>')
									.attr('src', 'track/' + data[a].docNum + '/artwork'))));
				}
			}
		});
		return false;
	});
	soundManager.url = '/data/soundmanager2.swf';
	soundManager.debugMode = false;
	soundManager.onload = function() {
		soundReady = true;
	  // SM2 is ready to go!
	  /*var mySound = soundManager.createSound({
	    id: 'aSound',
	    url: '/path/to/an.mp3',
	    volume: 50
	  });
	  mySound.play();*/
	};
	soundManager.onerror = function() {
	  // Oh no! No sound support.
	  // Maybe configure your app to ignore sound calls.
	  // (SM2 calls will silently return false after this point.)
	console.log("oups");
	}
}
);