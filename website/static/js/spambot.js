$(document).ready(function(){
    
    $("#place_call_button").click(function(e){
	$(this).addClass("disabled")
	var number = $(this).attr("data-number")
	var emotion = $(this).attr("data-emotion")
	var spam_id = $(this).attr("data-spam-id")

	$.post('/call',
	       {"to_number" : number, "emotion" : emotion, "spam_id": spam_id},
	       function(data) {
		   $("#place_call_button").text("Call back request placed")
	       }
	      );
    });
})