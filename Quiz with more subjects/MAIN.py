import os

# File paths
USER_DATA_FILE = "user_data.txt"
RESULTS_FILE = "quiz_results.txt"

# Quiz files for different subjects
QUIZ_FILES = {
    "DBMS": "DBMS_quiz.txt",
    "Operating System": "Operating_System_quiz.txt",
    "Python": "Python_quiz.txt",
    "Machine Learning": "Machine_Learning_quiz.txt"
}

# Ensure all necessary files exist
for file in [USER_DATA_FILE, RESULTS_FILE] + list(QUIZ_FILES.values()):
    if not os.path.exists(file):
        open(file, 'w').close()

# Register function
def register():
    with open(USER_DATA_FILE, "a+") as file:
        name = input("Enter your name: ").strip()
        password = input("Enter a 4-digit password: ").strip()
        
        if len(password) != 4 or not password.isdigit():
            print("Password must be a 4-digit number.")
            return
        
        # Check if username already exists
        file.seek(0)
        for line in file:
            stored_name, _ = line.strip().split(":")
            if stored_name == name:
                print("Username already exists. Try logging in.")
                return
        
        file.write(f"{name}:{password}\n")
        print("Registration successful!")

# Login function
def login():
    name = input("Enter your name: ").strip()
    password = input("Enter your 4-digit password: ").strip()
    
    with open(USER_DATA_FILE, "r") as file:
        for line in file:
            stored_name, stored_password = line.strip().split(":")
            if stored_name == name and stored_password == password:
                print("Login successful!")
                return name
    print("Invalid username or password.")
    return None

# Load questions from the selected quiz file
def load_quiz(subject):
    questions = []
    with open(QUIZ_FILES[subject], "r") as file:
        for line in file:
            parts = line.strip().split(":")
            question = parts[0]
            correct_answer = parts[1]
            options = parts[2:]
            questions.append((question, correct_answer, options))
    return questions

# Attempt Quiz
def attempt_quiz(user):
    # Select quiz subject
    print("\nSelect a quiz subject:")
    for i, subject in enumerate(QUIZ_FILES.keys(), 1):
        print(f"{i}. {subject}")
    
    try:
        subject_choice = int(input("Enter your choice (1-4): ").strip())
        subject = list(QUIZ_FILES.keys())[subject_choice - 1]
    except (IndexError, ValueError):
        print("Invalid choice. Please try again.")
        return
    
    questions = load_quiz(subject)
    score = 0
    
    for q, correct_answer, options in questions:
        print(f"\n{q}")
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")
        
        # Get user's answer and validate it
        while True:
            try:
                answer_index = int(input("Enter the option number (1-4): ").strip())
                if 1 <= answer_index <= 4:
                    answer = options[answer_index - 1]
                    break
                else:
                    print("Invalid option. Please choose between 1 and 4.")
            except ValueError:
                print("Please enter a valid number (1-4).")
        
        if answer.lower() == correct_answer.lower():
            score += 1
    
    # Update or add the user's score in the results file
    update_result(user, score, subject)

# Update user result
def update_result(user, score, subject):
    results = {}
    
    # Load existing results
    with open(RESULTS_FILE, "r") as file:
        for line in file:
            name, subject_stored, user_score = line.strip().split(":")
            results[(name, subject_stored)] = int(user_score)
    
    # Update score if user and subject entry exists, otherwise add new entry
    results[(user, subject)] = score
    
    # Write updated results to file
    with open(RESULTS_FILE, "w") as file:
        for (name, subject_stored), user_score in results.items():
            file.write(f"{name}:{subject_stored}:{user_score}\n")
    print(f"Your score for {subject}: {score}")

# View quiz results
def get_results(user):
    print(f"\nQuiz Results for {user}:")
    found = False
    with open(RESULTS_FILE, "r") as file:
        for line in file:
            name, subject, score = line.strip().split(":")
            if name == user:
                print(f"{subject} Score: {score}")
                found = True
    if not found:
        print("No scores found for this user.")

# Main Program Loop
def main():
    print("Welcome to the Quiz Application!")
    while True:
        choice = input("\nChoose an option:\n1. Register\n2. Login\n3. Quit\n> ").strip()
        
        if choice == "1":
            register()
        elif choice == "2":
            user = login()
            if user:
                while True:
                    action = input("\nChoose an action:\n1. Attempt Quiz\n2. Get Result\n3. Logout\n> ").strip()
                    if action == "1":
                        attempt_quiz(user)
                    elif action == "2":
                        get_results(user)
                    elif action == "3":
                        print("Logged out.")
                        break
                    else:
                        print("Invalid choice. Try again.")
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
