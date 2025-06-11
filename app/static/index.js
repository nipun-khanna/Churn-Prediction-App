document.getElementById('prediction-form').addEventListener('submit', submitForm);

async function submitForm(event) {
    event.preventDefault();

    const genderVal = document.querySelector("input[name='gender']:checked").value;
    const gender = genderVal == "female" ? 1 : 0;
    const senCitVal = document.querySelector("input[name='senior-citizen']:checked").value;
    const seniorCitizen = senCitVal == "yes" ? 1 : 0;
    const partner = document.getElementById("partner").checked ? 1 : 0;
    const dependents = document.getElementById("dependents").checked ? 1 : 0;
    const phoneService = document.getElementById("phone-service").checked ? 1 : 0;
    const paperlessBilling = document.getElementById("paperless-billing").checked ? 1 : 0;

    const tenure = parseFloat(document.getElementById('tenure').value);
    const total_charges = parseFloat(document.getElementById('total-charges').value);
    const monthly_charges = parseFloat(document.getElementById('monthly-charges').value);

    const contract_type = document.getElementById('contract-type');
    const index = contract_type.selectedIndex;
    const contract_features = [false, false, false];
    contract_features[index] = true;

    const data = {
        "gender": gender,
        "SeniorCitizen": seniorCitizen,
        "Partner": partner,
        "Dependents": dependents,
        "PhoneService": phoneService,
        "PaperlessBilling": paperlessBilling,
        "tenure": tenure,
        "TotalCharges": total_charges,
        "MonthlyCharges": monthly_charges,
        "Contract_Month-to-month": contract_features[0],
        "Contract_One year": contract_features[1],
        "Contract_Two year": contract_features[2],
    };

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
            'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();
        const resultDiv = document.getElementById('result');

        if (response.ok) {
            let churnText = result.churn_prediction === 1 ? 'YES (likely to churn)' : 'NO (unlikely to churn)';
            resultDiv.innerHTML = `Prediction: <strong>${churnText}</strong><br>
                                           Probability of Churn: <strong>${(result.churn_probability * 100).toFixed(2)}%</strong>`;
            resultDiv.style.color = result.churn_prediction === 1 ? 'red' : 'green';
        } else {
            resultDiv.innerHTML = `Error: ${result.error || 'Unknown error'}`;
            resultDiv.style.color = 'red';
        }
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('result').innerHTML = `Network Error: ${error}`;
        document.getElementById('result').style.color = 'red';
    }
}