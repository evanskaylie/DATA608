import pandas as pd
import matplotlib.pyplot as plt


# Import the csv from github
raw_csv = pd.read_csv('https://raw.githubusercontent.com/evanskaylie/DATA608/refs/heads/main/DataJobs.csv')


## DATA CLEANING/ PREPROCESSING

# Clean the 'Area Name' column to remove the parentheses and everything within
raw_csv['Area Name'] = raw_csv['Area Name'].str.replace(r'\s*\(.*?\)', '', regex=True)

# Rename the columns
raw_csv.rename(columns={
    'Job': 'job',
    'Area Name': 'state',
    'Annual mean wage(2)': 'salary'
}, inplace=True)

# Ensure the 'salary' column is numeric
raw_csv['salary'] = pd.to_numeric(raw_csv['salary'], errors='coerce')

# List of columns to filter
columns_to_keep = ['job', 'state', 'salary']

# Create the new filtered DataFrame
jobs_df = raw_csv[columns_to_keep]



'''
There will be 4 sets of visualizations
1. Average salary by state (average for all jobs)
2. Average salary by state (4 visuals, highest 4 avg salaries)
3. Average salary by job (average for all states)
4. Average salary by job (4 visuals, highest 4 avg salaries)
'''

## 1. Average salary by state (average for all jobs)
# Group by 'state' and calculate the average salary
average_salary_by_state = (
    raw_csv.groupby('state')['salary']
    .mean()
    .round(2)
    .reset_index()
)


## 2. Average salary by state (4 visuals, highest 4 avg salaries)
# Get the top 4 states by average salary
top_4_salaries = average_salary_by_state.nlargest(4, 'salary')
top_4_states = top_4_salaries['state'].tolist()

# Create a new DataFrame for each top state
filtered_jobs_dfs = {}
for state in top_4_states:
    filtered_jobs_dfs[state] = jobs_df[jobs_df['state'] == state]

## 3. Average salary by job (average for all states)
# Group by 'job', then calculate the average salary
average_salary_by_job = (
    jobs_df.groupby('job')['salary']
    .mean()
    .round(2)
    .reset_index()
)

# Rename the resulting columns for clarity
average_salary_by_job.rename(columns={'salary': 'average_salary'}, inplace=True)


## 4. Average salary by job (4 visuals, highest 4 avg salaries)
# Get the top 4 highest average salaries
top_4_jobs = average_salary_by_job.nlargest(4, 'average_salary')
top_4_job_titles = top_4_jobs['job'].tolist()

# Create a new DataFrame for each top job
filtered_jobs_dfs = {}
for job in top_4_job_titles:
    filtered_jobs_dfs[job] = jobs_df[jobs_df['job'] == job]






## VISUALIZATION TIME
# Sort the data by salary in descending order
average_salary_by_state_sorted = average_salary_by_state.sort_values(by='salary', ascending=True)

# Visualization for Average Salary by State with salary values in 'K' format next to each bar and no black outline
plt.figure(figsize=(8, 8))
bars = plt.barh(average_salary_by_state_sorted['state'], average_salary_by_state_sorted['salary'], color='skyblue')

# Annotate each bar with the salary value in 'K' format
for bar in bars:
    # Format the salary value as 'X.XXK'
    salary_in_k = bar.get_width() / 1000  # Convert to 'K'
    formatted_salary = f'{salary_in_k:.1f}K'  # Format the number to one decimal place and add 'K'

    # Place the formatted salary next to the bar
    plt.text(
        bar.get_width(),  # X position of the text (end of the bar)
        bar.get_y() + bar.get_height() / 2,  # Y position of the text (center of the bar)
        formatted_salary,  # Display the formatted salary
        va='center',  # Vertically center the text
        ha='left',  # Horizontally align the text to the left of the bar
        color='black'  # Text color
    )

# Remove the black outline (spines)
for spine in plt.gca().spines.values():
    spine.set_visible(False)

# Remove x-axis ticks
plt.xticks([])

plt.title('Average Salary by State (All Jobs)')
plt.xlabel('Average Salary ($)')
plt.tight_layout()
plt.show()



## 2. Average salary by state (4 visuals, highest 4 avg salaries)

# Get the top 4 states by average salary
top_4_salaries = average_salary_by_state.nlargest(4, 'salary')
top_4_states = top_4_salaries['state'].tolist()

# Create a new DataFrame for each top state
filtered_jobs_dfs = {}
for state in top_4_states:
    filtered_jobs_dfs[state] = jobs_df[jobs_df['state'] == state]

# Create individual visualizations for each of the top 4 states
for state in top_4_states:
    # Calculate the average salary by job for the current state
    state_data = filtered_jobs_dfs[state].groupby('job')['salary'].mean().reset_index()

    # Sort the data by salary in descending order
    state_data = state_data.sort_values(by='salary', ascending=True)

    # Visualization for Average Salary by Job in the state with salary values in 'K' format next to each bar
    plt.figure(figsize=(10, 6))
    bars = plt.barh(state_data['job'], state_data['salary'], color='skyblue')

    # Annotate each bar with the salary value in 'K' format
    for bar in bars:
        # Format the salary value as 'X.XXK'
        salary_in_k = bar.get_width() / 1000  # Convert to 'K'
        formatted_salary = f'{salary_in_k:.1f}K'  # Format the number to one decimal place and add 'K'

        # Place the formatted salary next to the bar
        plt.text(
            bar.get_width(),  # X position of the text (end of the bar)
            bar.get_y() + bar.get_height() / 2,  # Y position of the text (center of the bar)
            formatted_salary,  # Display the formatted salary
            va='center',  # Vertically center the text
            ha='left',  # Horizontally align the text to the left of the bar
            color='black'  # Text color
        )

    # Remove the black outline (spines)
    for spine in plt.gca().spines.values():
        spine.set_visible(False)

    # Remove x-axis ticks
    plt.xticks([])

    plt.title(f'Average Salary by Job in {state}')
    plt.xlabel('Average Salary ($)')
    plt.tight_layout()
    plt.show()


## 3. Average salary by job (average for all states)

# Sort the data by average salary in descending order
average_salary_by_job_sorted = average_salary_by_job.sort_values(by='average_salary', ascending=True)

# Visualization for Average Salary by Job (for all states) with salary values in 'K' format next to each bar
plt.figure(figsize=(10, 6))
bars = plt.barh(average_salary_by_job_sorted['job'], average_salary_by_job_sorted['average_salary'], color='skyblue')

# Annotate each bar with the salary value in 'K' format
for bar in bars:
    # Format the salary value as 'X.XXK'
    salary_in_k = bar.get_width() / 1000  # Convert to 'K'
    formatted_salary = f'{salary_in_k:.1f}K'  # Format the number to one decimal place and add 'K'

    # Place the formatted salary next to the bar
    plt.text(
        bar.get_width(),  # X position of the text (end of the bar)
        bar.get_y() + bar.get_height() / 2,  # Y position of the text (center of the bar)
        formatted_salary,  # Display the formatted salary
        va='center',  # Vertically center the text
        ha='left',  # Horizontally align the text to the left of the bar
        color='black'  # Text color
    )

# Remove the black outline (spines)
for spine in plt.gca().spines.values():
    spine.set_visible(False)

# Remove x-axis ticks
plt.xticks([])

plt.title('Average Salary by Job (All States)')
plt.xlabel('Average Salary ($)')
plt.tight_layout()
plt.show()



## 4. Average salary by job (4 visuals, highest 4 avg salaries)

# Get the top 4 highest average salaries
top_4_jobs = average_salary_by_job.nlargest(4, 'average_salary')
top_4_job_titles = top_4_jobs['job'].tolist()

# Create a new DataFrame for each top job
filtered_jobs_dfs = {}
for job in top_4_job_titles:
    filtered_jobs_dfs[job] = jobs_df[jobs_df['job'] == job]

# Create individual visualizations for each of the top 4 jobs
for job in top_4_job_titles:
    # Calculate the average salary by state for the current job
    job_data = filtered_jobs_dfs[job].groupby('state')['salary'].mean().reset_index()

    # Sort the data by salary in descending order
    job_data = job_data.sort_values(by='salary', ascending=True)

    # Visualization for Average Salary by State in the job with salary values in 'K' format next to each bar
    plt.figure(figsize=(10, 8))
    bars = plt.barh(job_data['state'], job_data['salary'], color='skyblue')

    # Annotate each bar with the salary value in 'K' format
    for bar in bars:
        # Format the salary value as 'X.XXK'
        salary_in_k = bar.get_width() / 1000  # Convert to 'K'
        formatted_salary = f'{salary_in_k:.1f}K'  # Format the number to one decimal place and add 'K'

        # Place the formatted salary next to the bar
        plt.text(
            bar.get_width(),  # X position of the text (end of the bar)
            bar.get_y() + bar.get_height() / 2,  # Y position of the text (center of the bar)
            formatted_salary,  # Display the formatted salary
            va='center',  # Vertically center the text
            ha='left',  # Horizontally align the text to the left of the bar
            color='black'  # Text color
        )

    # Remove the black outline (spines)
    for spine in plt.gca().spines.values():
        spine.set_visible(False)

    # Remove x-axis ticks
    plt.xticks([])

    plt.title(f'Average Salary by State for {job}')
    plt.xlabel('Average Salary ($)')
    plt.tight_layout()
    plt.show()