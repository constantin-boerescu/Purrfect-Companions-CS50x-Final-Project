function fetchData() {
    // Make an AJAX request to the Flask
    return fetch('/get_array_data')
    
      .then(response => response.json())
      .then(data => {
        // Update the catsId array with the data
        favsId = data;
      })
  }
  
fetchData();

function addToFavs(catId){
  // Adds the cats id to the favourites
    if (!favsId.includes(catId)){
        favsId.push(catId)
    }

}
// Listen for button press and gets cat id value
document.addEventListener('click', function(event){
    if (event.target.classList.contains('fav_btn')){

        // Gets the value and coverts it to string
        var catId = event.target.getAttribute('value')
        catId = parseInt(catId)
        addToFavs(catId)
        sendFavsToFlask();
    }
})

function sendFavsToFlask() {
// Sends the data to flask
    fetch('/update_favs', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ favsId: favsId }),
    })
      .then(response => response.json())
  }
  
 
