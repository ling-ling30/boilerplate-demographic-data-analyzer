import pandas as pd


def calculate_demographic_data(print_data=True):
  # Read data from file
  df = pd.read_csv('adult.data.csv')

  # How many of each race are represented in this dataset? This should be a Pandas series with race names as the index labels.
  age_sex = pd.pivot_table(df, index='race', aggfunc='size')
  race_count = age_sex

  # What is the average age of men?
  man = df[df["sex"] == 'Male']

  average_age_men = (man["age"].mean().round(1))

  # What is the percentage of people who have a Bachelor's degree?
  edu = df.pivot_table(index='education', aggfunc='size')

  percentage_bachelors = (edu['Bachelors'] / edu.sum() * 100).round(1)

  # What percentage of people with advanced education (`Bachelors`, `Masters`, or `Doctorate`) make more than 50K?
  # What percentage of people without advanced education make more than 50K?
  df_rich = df.loc[df['salary'] == '>50K']
  rich = df_rich.pivot_table(index='education', aggfunc='size')
  # with and without `Bachelors`, `Masters`, or `Doctorate`
  higher_education = edu[['Bachelors', 'Masters', 'Doctorate']].sum()

  lower_education = edu.sum() - edu[['Bachelors', 'Masters', 'Doctorate'
                                     ]].sum()

  # percentage with salary >50K

  higher_education_rich = (rich[['Bachelors', 'Masters', 'Doctorate']].sum() /
                           higher_education * 100).round(1)
  lower_education_rich = (
    (rich.sum() - rich[['Bachelors', 'Masters', 'Doctorate']].sum()) /
    lower_education * 100).round(1)

  # What is the minimum number of hours a person works per week (hours-per-week feature)?
  min_work_hours = df['hours-per-week'].min()

  # What percentage of the people who work the minimum number of hours per week have a salary of >50K?
  num_min_workers = df.loc[(df['hours-per-week'] == 1)]
  num_min_workers = num_min_workers.pivot_table(index='hours-per-week',
                                                aggfunc='size')[1]

  min_worker_rich = df.loc[(df['hours-per-week'] == 1)
                           & (df['salary'] == '>50K')]
  rich_percentage = min_worker_rich.pivot_table(
    index='hours-per-week', aggfunc='size')[1] / num_min_workers * 100

  # What country has the highest percentage of people that earn >50K?
  country_all = df.pivot_table(index='native-country',
                               aggfunc='size').sort_values(ascending=False)
  country_rich = df_rich.pivot_table(
    index='native-country', aggfunc='size').sort_values(ascending=False)
  dt_country_rich = pd.concat([country_all, country_rich], axis=1)
  dt_country_rich['percentage'] = ((dt_country_rich[1] / dt_country_rich[0]) *
                                   100).round(1)
  dt_country_rich = dt_country_rich.sort_values(by='percentage',
                                                ascending=False)

  highest_earning_country = dt_country_rich.index[0]

  highest_earning_country_percentage = dt_country_rich.iloc[0]['percentage']

  # Identify the most popular occupation for those who earn >50K in India.
  india_rich = df_rich.loc[(df['native-country'] == 'India')]
  top_IN_occupation = india_rich.pivot_table(
    index='occupation', aggfunc='size').sort_values(ascending=False).keys()[0]

  # DO NOT MODIFY BELOW THIS LINE

  if print_data:
    print("Number of each race:\n", race_count)
    print("Average age of men:", average_age_men)
    print(f"Percentage with Bachelors degrees: {percentage_bachelors}%")
    print(
      f"Percentage with higher education that earn >50K: {higher_education_rich}%"
    )
    print(
      f"Percentage without higher education that earn >50K: {lower_education_rich}%"
    )
    print(f"Min work time: {min_work_hours} hours/week")
    print(
      f"Percentage of rich among those who work fewest hours: {rich_percentage}%"
    )
    print("Country with highest percentage of rich:", highest_earning_country)
    print(
      f"Highest percentage of rich people in country: {highest_earning_country_percentage}%"
    )
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
