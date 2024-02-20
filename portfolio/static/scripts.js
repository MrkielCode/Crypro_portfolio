function getCryptoData() {
    $.ajax({
        url: "http://127.0.0.1:5000/get_crypto_data",
        type: "GET",
        dataType: "json",
        success: function (data) {
            displayData(data);
            displaySingleData(data);
        },
        error: function (error) {
            // Handle the error case
            console.error("Error fetching crypto data:", error);
            // You might want to add some user-friendly error handling here
        }
    });
}

function displayData(data) {
    var table = $('#price-info tbody');
    table.empty();
    $.each(data, function (index, crypto) {
        var row = '<tr>' +
            '<th scope="row">' + (index + 1) + '</th>' +
            '<td>' + crypto.name + ' (' + crypto.symbol + ')' + '</td>' +
            '<td>$' + crypto.price.toFixed(2) + '</td>' +
            '<td>$' + crypto.market_cap.toLocaleString() + '</td>' +
            '</tr>';
        table.append(row);
    });
}

function displaySingleData(data) {
    let section = $('#general-info .row');
    section.empty();
    $.each(data, function (index, crypto) {
        if (crypto.name == 'Bitcoin' || crypto.name == 'Ethereum' || crypto.name == 'BNB') {
            var div = `<div class="col-md text-center box-container mt-5">
                <p class="marketcap-info">$${crypto.market_cap.toLocaleString()}</p>
                <h4>${crypto.name}</h4>
            </div>`;
            section.append(div);
        }
    });
}

 // Function to get and append portfolio data
 function getPortfolioData(user_id) {
    $.ajax({
        url: "http://127.0.0.1:5000/calculate_user_portfolio/"+user_id,
        type: "GET",
        dataType: "json",
        success: function (data) {
            appendPortfolioData(data);
        },
        error: function (error) {
            // Handle the error case
            console.error("Error fetching portfolio data:", error);
            // You might want to add some user-friendly error handling here
        }
    });
}

// Function to append portfolio data
function appendPortfolioData(data) {
    let table = $('#portfolio-info tbody');
    table.empty();
    $.each(data, function (index, crypto) { 
        let row = `<tr>
        <th scope="row">${index + 1}</th>
        <td>${crypto.asset_name}</td>
        <td>${crypto.current_value}</td>
        <td>${crypto.pnl_percentage}</td>
        <td>${crypto.total_cost}</td>
        </tr>`;
        table.append(row);   
    });
}


$(function () {
    getCryptoData()
});
