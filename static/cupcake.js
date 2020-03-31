const URL = "http://localhost:5000/api";

let $cupcakeList = $("#cupcake-list");

// On page load, run our start function
$(start)

// Startup function that assigns event handler(s) and runs the displayCupcakeList function
async function start() {
    $("#new-cupcake-button").on("click", submitNewCupcake)
    $("#search-submit").on("click", submitSearch)

    await displayCupcakeList();
}

// Creates object from the form data and sends it to our API to create a new cupcake, 
// reloads the cupcake list to show it.
async function submitNewCupcake (event)  {
    event.preventDefault();

    let newCupcake = {
        "flavor": $("#form-flavor").val(),
        "size": $("#form-size").val(),
        "rating": $("#form-rating").val(),
        "image": $("#form-image").val(),
    };

    await axios.post(`${URL}/cupcakes`, newCupcake);

    $cupcakeList.append(generateCupcakeHTML(newCupcake));
}

// Queries the API for list of cupcakes, uses helper function to turn into html and appends to page.
async function displayCupcakeList() {
    response = await axios.get(`${URL}/cupcakes`);

    for (let cupcake of response.data.cupcakes) {
        html = generateCupcakeHTML(cupcake);
        $cupcakeList.append(html);
    }
}

// Helper function that takes a cupcake object and makes HTML to display on page.
function generateCupcakeHTML(cupcake) {
    return `<div class='cupcake'>
                <img src='${cupcake.image}'>
                <h3>${cupcake.flavor}</h3>
                <h4>Rating: ${cupcake.rating}</h4>
                <h4>${cupcake.size}</h4>
            </div>
    `
}

// Takes value from search field, sends to /search API, 
// renders the resulting cupcakes on page or displays error message.
async function submitSearch(event){
    event.preventDefault();

    //only searches flavor and size
    searchTerms = $("#search-field").val();

    $("#search-message").empty();

    searchResponse = await axios.get(`${URL}/search/${searchTerms}`);

    if (searchResponse.data === "No cupcakes found.") {
        $("#search-message").text(searchResponse.data);
    } else {

        $cupcakeList.empty();

        for (let cupcake of searchResponse.data.cupcakes) {
            html = generateCupcakeHTML(cupcake);
            $cupcakeList.append(html);
        }
    }
}

