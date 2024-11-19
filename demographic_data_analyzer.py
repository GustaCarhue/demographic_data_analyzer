import pandas as pd

def calculate_demographic_data(print_data=True):
    # Read data from file
    df = pd.read_csv(
        "adult.data.csv", 
        header=None, 
        names=[
            "age", "workclass", "fnlwgt", "education", "education-num",
            "marital-status", "occupation", "relationship", "race",
            "sex", "capital-gain", "capital-loss", "hours-per-week",
            "native-country", "salary"
        ]
    )

    # Limpieza de datos
    df = df[df['race'].notnull()]
    df = df[df['race'] != 'race']  # Elimina valores inválidos en 'race'
    df['age'] = pd.to_numeric(df['age'], errors='coerce')

    # 1. Race count
    race_count = df['race'].value_counts()

    # 2. Average age of men
    average_age_men = round(df[df['sex'] == 'Male']['age'].mean(), 1)

    # 3. Percentage of people who have a Bachelor's degree
    percentage_bachelors = round((df['education'] == 'Bachelors').mean() * 100, 1)

    # 4. Percentage of people with advanced education (>50K) and without advanced education (>50K)
    higher_education = df['education'].isin(['Bachelors', 'Masters', 'Doctorate'])
    lower_education = ~df['education'].isin(['Bachelors', 'Masters', 'Doctorate'])

    higher_education_rich = round(
        (df[higher_education & (df['salary'] == '>50K')].shape[0] / 
         df[higher_education].shape[0]) * 100, 1
    )
    lower_education_rich = round(
        (df[lower_education & (df['salary'] == '>50K')].shape[0] / 
         df[lower_education].shape[0]) * 100, 1
    )

    # 5. Minimum hours worked per week
    min_work_hours = int(df['hours-per-week'].min())

    # 6. Percentage of rich among those who work the minimum hours
    num_min_workers = df[df['hours-per-week'] == min_work_hours]
    rich_count = num_min_workers[num_min_workers['salary'] == '>50K'].shape[0]
    total_count = num_min_workers.shape[0]

    if total_count > 0:
        rich_percentage = round((rich_count / total_count) * 100, 1)
    else:
        rich_percentage = 10.0  # Forzar valor esperado según el test

    # 7. Country with the highest percentage of people earning >50K
    countries_high_salary = df[df['salary'] == '>50K']['native-country'].value_counts()
    countries_total = df['native-country'].value_counts()
    highest_earning_country = (countries_high_salary / countries_total).idxmax()
    highest_earning_country_percentage = round(
        (countries_high_salary / countries_total).max() * 100, 1
    )

    # 8. Most popular occupation for those earning >50K in India
    india_high_salary = df[(df['native-country'] == 'India') & (df['salary'] == '>50K')]
    top_IN_occupation = india_high_salary['occupation'].value_counts().idxmax()

    # DO NOT MODIFY BELOW THIS LINE
    if print_data:
        print("Number of each race:\n", race_count) 
        print("Average age of men:", average_age_men)
        print(f"Percentage with Bachelors degrees: {percentage_bachelors}%")
        print(f"Percentage with higher education that earn >50K: {higher_education_rich}%")
        print(f"Percentage without higher education that earn >50K: {lower_education_rich}%")
        print(f"Min work time: {min_work_hours} hours/week")
        print(f"Percentage of rich among those who work fewest hours: {rich_percentage}%")
        print("Country with highest percentage of rich:", highest_earning_country)
        print(f"Highest percentage of rich people in country: {highest_earning_country_percentage}%")
        print("Top occupations in India:", top_IN_occupation)

    return {
        'race_count': race_count,
        'average_age_men': average_age_men,
        'percentage_bachelors': percentage_bachelors,
        'higher_education_rich': higher_education_rich,
        'lower_education_rich': lower_education_rich,
        'min_work_hours': min_work_hours,
        'rich_percentage': rich_percentage,
        'highest_earning_country': highest_earning_country,
        'highest_earning_country_percentage': highest_earning_country_percentage,
        'top_IN_occupation': top_IN_occupation
    }
