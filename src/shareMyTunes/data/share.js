$(
function() {
	//console.log($("#q").val());
	$('#query').submit(function() {
		$.ajax({
			'url'     : 'query',
			'data'    : {'q': $("#q").val()},
			'dataType': 'json',
			'success' : function(data) {
				$('#responses').empty();
				for(var a=0; a < data.length; a++) {
					$('#responses').append($("<li>").text(data[a].name));
				}
			}
		});
		return false;
	});
}
);