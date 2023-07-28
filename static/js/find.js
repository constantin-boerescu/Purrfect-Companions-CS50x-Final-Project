// let catsId = [];

function fetchData() {
  // Make an AJAX request to the Flask backend
  return fetch('/get_array_data')
    .then(response => response.json())
    .then(data => {
      // Update the catsId array with the fetched data
      catsId = data;
      console.log(catsId); // Now catsId is populated with the fetched data
    })
    .catch(error => {
      console.error('Error fetching data:', error);
    });
}
fetchData();

// // Add the cat to favourites

// function addToFavorites(catId){
//     catsId.push(catId);
//     console.log(catsId);
  
//     fetch('/process-data', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json'
//         },
//         body: JSON.stringify({catsId: catsId}),
//     });
// }



// document.addEventListener('click', function(event) {
//     if(event.target.classList.contains('fav_btn')){
//         const catId = event.target.getAttribute('value');
        
//         if (!catsId.includes(catId)){
//             addToFavorites(catId);
//         }
//     }
// 

function fetchData() {
    // Make an AJAX request to the Flask backend
    return fetch('/get_array_data')
      .then(response => response.json())
      .then(data => {
        // Update the catsId array with the fetched data
        favsId = data;
        console.log(favsId); // Now catsId is populated with the fetched data
      })
      .catch(error => {
        console.error('Error fetching data:', error);
      });
  }
  
fetchData();

function rmvFrmFavs(catId){
    if (favsId.includes(catId)){

        // Gets the value index
        const index = array.indexOf(catId);

        if (index !== -1) {
            array.splice(index, 1);
            console.log(favsId)
        }           
    }
}

function addToFavs(catId){

    if (!favsId.includes(catId)){
        favsId.push(catId)
        console.log(favsId)
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

// Listen for button press and gets cat id value
document.addEventListener('click', function(event){
    if (event.target.classList.contains('rmv_btn')){

        // Gets the value and coverts it to string
        var catId = event.target.getAttribute('value')
        catId = parseInt(catId)
        rmvFrmFavs(catId)
    }
})

function sendFavsToFlask() {
    // Make an AJAX request to send favsId back to Flask
    fetch('/update_favs', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ favsId: favsId }),
    })
      .then(response => response.json())
      .then(data => {
        console.log('Updated favsId sent to Flask:', data);
      })
      .catch(error => {
        console.error('Error sending favsId to Flask:', error);
      });
  }
  
  // Call the function to send favsId to Flask whenever you want to update it
