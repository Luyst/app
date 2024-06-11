document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");

    form.addEventListener("submit", function (event) {
        event.preventDefault(); // Prevent the default form submission

        const formData = new FormData(form);

        // Validate form data
        const fields = [
            'Education', 'Marital_Status', 'Income', 'Age',
            'Children', 'Expenses', 'Wines', 'Fruits',
            'Meat', 'Fish', 'Sweet', 'Gold'
        ];

        for (const field of fields) {
            if (!formData.get(field)) {
                alert("Please fill out all fields before submitting.");
                return;
            }
        }

        const data = {
            Education: formData.get('Education'),
            Marital_Status: formData.get('Marital_Status'),
            Income: formData.get('Income'),
            Age: formData.get('Age'),
            Children: formData.get('Children'),
            Expenses: formData.get('Expenses'),
            Wines: formData.get('Wines'),
            Fruits: formData.get('Fruits'),
            Meat: formData.get('Meat'),
            Fish: formData.get('Fish'),
            Sweet: formData.get('Sweet'),
            Gold: formData.get('Gold')
        };

        fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
            .then(response => response.json())
            .then(result => {
                if (result.error) {
                    alert(result.error);
                } else {
                    displayResult(result);
                }
            })
            .catch(error => console.error('Error:', error));
    });

    function displayResult(result) {
        const resultContainer = document.querySelector(".result");
        resultContainer.innerHTML = `
            <h2>Cụm khách hàng số: ${result.cluster}</h2>
            <p><strong>Đặc điểm chung:</strong> ${result.cluster_infor.name}</p>
            <p><strong>Thu nhập và chi tiêu:</strong> ${result.cluster_infor.income_expenditure}</p>
            <p><strong>Học vấn:</strong> ${result.cluster_infor.education}</p>
            <p><strong>Tình trạng hôn nhân:</strong> ${result.cluster_infor.marital_status}</p>
            <p><strong>Tuổi:</strong> ${result.cluster_infor.age_range}</p>
            <p><strong>Số lượng con cái:</strong> ${result.cluster_infor.children_count}</p>
        `;
    }
});
