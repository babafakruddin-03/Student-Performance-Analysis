import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt

# Connect to MySQL
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="39257",
    database="student_performance"
)

# Retrieve student records from MySQL
query = "SELECT * FROM students"
students = pd.read_sql(query, connection)

# Close the database connection
connection.close()

print("\n===== STUDENT PERFORMANCE ANALYSIS =====")
print("Total students:", len(students))

# Calculate average marks
subjects = ["python_marks", "sql_marks", "maths_marks"]
students["average_marks"] = students[subjects].mean(axis=1)

print("\n===== STUDENT AVERAGES =====")
print(students[["name", "average_marks"]].round(2))

# Identify the top-performing student
top_student = students.loc[students["average_marks"].idxmax()]

print("\n===== TOP-PERFORMING STUDENT =====")
print("Name:", top_student["name"])
print("Average marks:", round(top_student["average_marks"], 2))

# Calculate pass/fail results
students["result"] = students[subjects].ge(40).all(axis=1)
students["result"] = students["result"].map({
    True: "Pass",
    False: "Fail"
})

passed = (students["result"] == "Pass").sum()
failed = (students["result"] == "Fail").sum()

print("\n===== PASS/FAIL SUMMARY =====")
print("Passed students:", passed)
print("Failed students:", failed)

# Create reports folder if it doesn't exist
import os
os.makedirs("reports", exist_ok=True)

# Chart 1: Student average marks
plt.figure(figsize=(12, 6))
plt.bar(students["name"], students["average_marks"])
plt.title("Student Average Marks")
plt.xlabel("Student Name")
plt.ylabel("Average Marks")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("reports/average_marks.png")
plt.show()
plt.close()

# Chart 2: Pass/fail distribution
result_counts = students["result"].value_counts()

plt.figure(figsize=(7, 7))
plt.pie(
    result_counts,
    labels=result_counts.index,
    autopct="%1.1f%%",
    startangle=90
)
plt.title("Student Pass/Fail Distribution")
plt.savefig("reports/pass_fail_chart.png")
plt.show()
plt.close()

print("\nAnalysis completed successfully!")