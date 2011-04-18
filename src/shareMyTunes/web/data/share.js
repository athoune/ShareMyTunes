$(
function() {
	var soundReady = false;
	var playing = null;
	// console.log("q", $("#q").val());
	$('#query').submit(function() {
		$.ajax({
			url     : 'query',
			data    : {q: $("#q").val()},
			dataType: 'json',
			success : function(data, textStatus, jqXHR) {
				// console.log(data);
				$('#responses').empty();
				for(var a=0; a < data.length; a++) {
					var link = $('<a>');
					console.log(data[a]);
					link.data('album', data[a].album);
					link.data('name', data[a].name);
					link.attr('href', 'track/' + data[a].docNum + '/music/' + data[a].clean_path + '.mp3');
					link.attr('id', 'track_' + data[a].docNum);
					link.click(function() {
						var that = $(this);
						var id = that.attr('id');
						if(playing != null) {
							console.debug(playing);
							if(playing.sID == id) {
								playing.togglePause();
								return false;
							} else {
								playing.stop();
								playing == null;
							}
						}
						console.log("play " + id);
						playing = soundManager.createSound({
							id      :id,
							url     :that.attr('href'),
							onfinish:function() {
								playing = null;
								console.log("finishing " + id);
							}
						});
						playing.play({volume:50});
						return false;
					});
					link.mouseover(function(e) {
						var that = $(this);
						$('#hover')
							.empty()
							.append($('<div class="album">').text(that.data('album')))
							.append($('<div class="name">').text(that.data('name')))
							.show()
							.css('position', 'absolute')
							.css('background-color', 'gray')
							.css('font-size', '0.75em')
							.css('z-index', '500')
							.css('left',e.pageX)
							.css('top',e.pageY);
					}).mouseout(function() {
						$('#hover').hide();
					});
					link.text(data[a].name + ' [' + data[a].album + ']');
					var song = $('<li class="jewel">');
					song.append(link);
					if(data[a].artwork == "1") {
						song.append($('<img/>')
							.attr('src', 'track/' + data[a].docNum + '/artwork'));
					}
					$('#responses').append(song);
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
	};
}
);