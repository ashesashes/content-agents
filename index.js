//select the result containers and initially set them to be hidden

const resultContainer = document.getElementById("result");
resultContainer.style.display = "none"; 
const tweetResultContainer = document.getElementById("tweet-result");
tweetResultContainer.style.display="none"; 
const newsletterResultContainer = document.getElementById("newsletter-result");
newsletterResultContainer.style.display="none"; 

// add a click event listner to the "runTask" btn

document.getElementById("runTask").addEventListener("click", function() {
    //select the loader and taskDescription elements from the DOM 

   const loader = document.getElementById("loader"); 
   const taskDescriptionInput = document.getElementById("task-description"); 
   const taskDescription = taskDescriptionInput.value; 

    //show the loader and set up the initial innerHTML for the result containers 

    loader.style.display = "block";
    resultContainer.innerHTML = `<img src="/images/engineer-woman.png" alt="Character" class="pixel-character" />
    <p class="result-text">Researching the topic...</p>`
    //clear previous text 
    tweetResultContainer.textContent = '';
    newsletterResultContainer.textContent = '';
    //display the result Container 
    resultContainer.style.display = "block"; 
    //initially hide the tweet results container 
    tweetResultContainer.style.display = "none"; 

    //make a POST request to the /run-task endpoint 
    fetch('http://localhost:8000/run-task', {
        method: 'POST', 
        headers: {
            'Content-Type': 'application/json'
        }, 
        body: JSON.stringify({ description: taskDescription })
    })
    //parse the json response from the server 
    .then(response => response.json())
    //handle the data from the endpoint 
    .then(data => {
        loader.style.display = "none"; //hide the loader since data has been fetched 

        const linkedinResult = formatTextWithLineBreaks(data.result.linkedin); 
        const tweetResult = formatTextWithLineBreaks(data.result.tweet); 
        const newsletterResult = formatTextWithLineBreaks(data.result.newsletter); 

        //check if the data returned for lInkedIn and tweet is a string and update containers accordingly 

        
            resultContainer.innerHTML = `<p class="result-text"> ${linkedinResult}  </p>`; 
       
            //show tweet result container 
            tweetResultContainer.style.display = "block";
        
            tweetResultContainer.innerHTML = `<p class="result-text"> ${tweetResult} </p>`; 

            //show newsletter result container
            newsletterResultContainer.style.display = "block";
        
            newsletterResultContainer.innerHTML = `<p class="result-text"> ${newsletterResult} </p>`; 
        

        console.log("returning data: ", data);
        console.log("LinkedIn results:", data.result.linkedin); 
        console.log("Tweet results", data.result.tweet); 
        console.log("Newsletter results", data.result.newsletter); 
    })
    .catch(error => {
        console.error("Error: ", error);
        loader.style.display = "none"; 
        //update containers with an error message and make them visible
        resultContainer.innerHTML = "Error fetching data "; 
        tweetResultContainer.innerHTML = "Error fetching data"; 
        newsletterResultContainer.innerHTML = "Error fetching data"; 
        resultContainer.style.dispaly = "block";
        tweetResultContainer.style.display = "block"; 
        newsletterResultContainer.style.display = "block"; 
    }); 

    function formatTextWithLineBreaks(text) {
        //Replace newlien characters with <br> elements
        return text.replace(/\n/g, '<br>');
    }

}); 