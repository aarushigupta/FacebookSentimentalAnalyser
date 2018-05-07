
document.addEventListener('DOMNodeInserted', function () {
		var arr = document.getElementsByTagName("p");

		for(var i = 0; i < arr.length; i++) {
			var txt = arr[i].innerText;
			var toColor = arr[i];
			// var sentiment = analyseSentiment(txt);
			// var scoreOfSentiment = sentiment.score;
			
			var sentiment = analyseSentimentPerceptron(txt);
			if (sentiment == -1){
				toColor.style.color = "red";
			}
			else{
				toColor.style.color = "green";
			}

			// if (scoreOfSentiment < 0){
			// 	toColor.style.color = "red";
			// }
			// else if(scoreOfSentiment > 0){
			// 	toColor.style.color = "green";
			// }
			// else{
			// 	toColor.style.color = "blue";
			// }


			//console.log(txt);
			//console.log(sentiment.score);
		}
});

// function makeRequest(){
// 	console.log("Making request");
// 	$.ajax({
//     url: 'http://localhost:8000',
//     type: 'GET',
//     dataType:'json',
//     data: JSON.stringify({'key1':'value1'}),
//     success: function(response){alert('hi');},
//     error: function(){console.log("Error occurred");}}
// )};

// window.onload = function() {
//   console.log("skjhdb fksjdbf ksjdbf");
//   makeRequest();
// };
