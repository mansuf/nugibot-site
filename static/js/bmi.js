function calculateBMI() {
    const height = document.getElementById('height').value / 100;
    const weight = document.getElementById('weight').value;
    const bmi = (weight / (height * height)).toFixed(2);
    const gender = document.getElementById('gender').value;

    document.getElementById('bmi').textContent = bmi;

    let category = '';
    let recommendations = [];
    let idealWeightRange = '';

    // Calculate the ideal weight range based on height
    const lowerWeightLimit = (18.5 * height * height).toFixed(2);
    const upperWeightLimit = (25.0 * height * height).toFixed(2);
    idealWeightRange = `${lowerWeightLimit}kg - ${upperWeightLimit}kg`;

    if (bmi < 18.5) {
        category = 'Underweight';
        recommendations = [
            'Increase calorie intake with healthy foods', 
            'Add more protein-rich foods like beans, lentils, and tofu',
            'Include healthy fats like avocados, nuts, and seeds',
            'Eat calorie-dense fruits like bananas, mangoes, and avocados',
            'Consume starchy vegetables like sweet potatoes and peas'
        ];
    } else if (bmi >= 18.5 && bmi <= 25.0) {
        category = 'Ideal weight';
        recommendations = [
            'Maintain a balanced diet', 
            'Continue regular physical activity', 
            'Eat a variety of fruits like apples, oranges, and berries',
            'Include leafy greens and colorful vegetables like spinach, kale, and bell peppers',
            'Choose whole grains like brown rice, oats, and quinoa',
            'Incorporate lean proteins like chicken, fish, and legumes'
        ];
    } else if (bmi > 25.0 && bmi <= 27.0) {
        category = 'Overweight';
        recommendations = [
            'Reduce calorie intake with portion control', 
            'Increase physical activity', 
            'Limit sugar and refined carbs', 
            'Eat more fruits like pears, apples, and berries',
            'Choose vegetables like broccoli, cauliflower, and zucchini',
            'Opt for legumes like lentils and beans',
            'Select low-fat dairy products like yogurt and skim milk'
        ];
    } else {
        category = 'Obese';
        recommendations = [
            'Adopt a low-calorie diet', 
            'Increase physical activity', 
            'Seek advice from a healthcare provider',
            'Eat fruits like grapefruit, watermelon, and kiwi',
            'Choose vegetables like cabbage, Brussels sprouts, and cucumber',
            'Include whole grains like barley and quinoa',
            'Opt for plant-based proteins like legumes and tofu'
        ];
    }

    document.getElementById('category').textContent = category;
    document.getElementById('idealWeightRange').textContent = `  ${idealWeightRange}`;

    const foodList = document.getElementById('foodRecommendations');
    foodList.innerHTML = '';

    // Display the food recommendations
    recommendations.forEach(rec => {
        const li = document.createElement('li');
        li.textContent = rec;
        foodList.appendChild(li);
    });
}
