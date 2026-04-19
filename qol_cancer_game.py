import random
import statistics
import matplotlib.pyplot as plt


def generate_patient_data(n_patients=60, missing_rate=0.08):
    """Simulate a patient dataset with demographics, clinical variables, and QoL scores."""
    data = []
    for patient_id in range(1, n_patients + 1):
        age = random.randint(35, 85)
        sex = random.choice(["Male", "Female"])
        stage = random.choice(["I", "II", "III", "IV"])
        treatment = random.choice(["Surgery", "Radiation", "Hormone", "Combined"])

        global_qol = random.randint(40, 100)
        physical = random.randint(30, 100)
        emotional = random.randint(30, 100)
        fatigue = random.randint(0, 60)
        pain = random.randint(0, 60)
        urinary = random.randint(0, 40)
        sexual = random.randint(0, 40)

        patient = {
            "id": patient_id,
            "age": age,
            "sex": sex,
            "stage": stage,
            "treatment": treatment,
            "global_qol": global_qol,
            "physical": physical,
            "emotional": emotional,
            "fatigue": fatigue,
            "pain": pain,
            "urinary": urinary,
            "sexual": sexual,
        }

        if random.random() < missing_rate:
            patient[random.choice(["physical", "emotional", "fatigue", "pain"])] = None
        if random.random() < missing_rate:
            patient[random.choice(["urinary", "sexual", "global_qol"])] = None

        data.append(patient)
    return data


def print_intro():
    print("\nWelcome to the Cancer QoL Data Analyst Game!")
    print("In this game, you will explore a simulated dataset inspired by QLQ-C30 and PR25 questionnaires.")
    print("You act as a junior epidemiologist who must clean data, choose visualizations, and interpret findings.\n")


def display_patient_summary(data):
    complete = sum(1 for row in data if None not in row.values())
    print(f"Dataset size: {len(data)} patients")
    print(f"Complete records: {complete}")
    print("Missing values appear in QoL and symptom fields.")
    print("Common tasks include identifying missing values, summarizing group differences, and interpreting quality of life scores.\n")


def find_missing_values(data):
    missing_counts = {}
    for row in data:
        for key, value in row.items():
            if value is None:
                missing_counts[key] = missing_counts.get(key, 0) + 1
    return missing_counts


def simple_cleaning(data):
    """Clean the dataset by dropping records with missing QoL values."""
    cleaned = [row for row in data if None not in row.values()]
    return cleaned


def summarize_scale(data, scale_name):
    values = [row[scale_name] for row in data if row[scale_name] is not None]
    return {
        "n": len(values),
        "mean": statistics.mean(values) if values else 0,
        "median": statistics.median(values) if values else 0,
        "min": min(values) if values else 0,
        "max": max(values) if values else 0,
    }


def score_question(question, options, correct_index):
    print(question)
    for idx, option in enumerate(options, start=1):
        print(f"  {idx}. {option}")
    while True:
        try:
            answer = int(input("Your choice: "))
            if 1 <= answer <= len(options):
                return answer == correct_index
            print("Please choose one of the listed options.")
        except ValueError:
            print("Enter a number corresponding to your answer.")


def show_histogram(data, field_name, title):
    values = [row[field_name] for row in data if row[field_name] is not None]
    plt.figure(figsize=(6, 3))
    plt.hist(values, bins=8, color="#4c72b0", edgecolor="black")
    plt.title(title)
    plt.xlabel(field_name.replace("_", " ").title())
    plt.ylabel("Patients")
    plt.tight_layout()
    plt.show()


def show_boxplot(data, field_name, title):
    values = [row[field_name] for row in data if row[field_name] is not None]
    plt.figure(figsize=(4, 4))
    plt.boxplot(values, patch_artist=True, boxprops={"facecolor": "#55a868"})
    plt.title(title)
    plt.ylabel(field_name.replace("_", " ").title())
    plt.tight_layout()
    plt.show()


def average_by_group(data, group_field, value_field):
    groups = {}
    for row in data:
        if row[value_field] is None:
            continue
        key = row[group_field]
        groups.setdefault(key, []).append(row[value_field])
    return {group: statistics.mean(values) for group, values in groups.items()}


def analyze_factor(data):
    global_by_stage = average_by_group(data, "stage", "global_qol")
    pain_by_treatment = average_by_group(data, "treatment", "pain")
    return global_by_stage, pain_by_treatment


def play_level_one(data):
    print("\n[Level 1] Data Cleaning")
    print("Your first task is to inspect missing information in the dataset.")
    missing_counts = find_missing_values(data)
    print("Missing values per field:")
    for field, count in missing_counts.items():
        print(f"  {field}: {count}")

    question = (
        "Which strategy is the safest first step for handling missing QoL scale values in a small simulated dataset?"
    )
    options = [
        "Drop records with missing QoL values.",
        "Impute missing QoL values with zeros.",
        "Replace missing values with the highest possible score.",
    ]
    correct = 1
    correct_answer = score_question(question, options, correct)
    if correct_answer:
        print("Correct! Removing incomplete records is a conservative and transparent first step.")
        score = 10
    else:
        print("Not ideal: zero or maximum imputation may distort QoL meaning.")
        score = 5
    return score


def play_level_two(data):
    print("\n[Level 2] Visualization")
    print("Choose a plot that best helps understand global quality of life distribution.")
    options = [
        "Histogram of global QoL.",
        "Boxplot of urinary symptoms.",
        "Scatter plot of age vs. treatment type.",
    ]
    correct = 1
    correct_answer = score_question("Which visualization is best for this task?", options, correct)
    if correct_answer:
        print("Great! A histogram shows how QoL scores spread across patients.")
        score = 10
    else:
        print("A histogram is the most direct way to inspect a single scale distribution.")
        score = 5

    show_histogram(data, "global_qol", "Global QoL Distribution")
    return score


def play_level_three(data):
    print("\n[Level 3] Interpretation")
    stats = summarize_scale(data, "global_qol")
    print("Global QoL summary:")
    for key, value in stats.items():
        if isinstance(value, float):
            print(f"  {key.title()}: {value:.1f}")
        else:
            print(f"  {key.title()}: {value}")
    print("In QoL studies, higher global scores generally mean better overall health quality.")

    question = (
        "If the average global QoL is 68 and the average pain score is 24, what is the most plausible interpretation?"
    )
    options = [
        "Overall quality of life is relatively good, but pain is a noticeable issue.",
        "Patients feel very poor overall and have no pain concerns.",
        "High pain scores mean excellent quality of life.",
    ]
    correct = 1
    correct_answer = score_question(question, options, correct)
    if correct_answer:
        print("Correct. Both score direction and symptom interpretation matter.")
        score = 10
    else:
        print("Remember: symptoms like pain are worse when they are higher, while global QoL is better when higher.")
        score = 5
    return score


def play_level_four(data):
    print("\n[Level 4] Factors Associated with Poor QoL")
    global_by_stage, pain_by_treatment = analyze_factor(data)
    print("Average global QoL by stage:")
    for stage, mean_value in sorted(global_by_stage.items()):
        print(f"  Stage {stage}: {mean_value:.1f}")
    print("Average pain by treatment:")
    for treatment, mean_value in sorted(pain_by_treatment.items()):
        print(f"  {treatment}: {mean_value:.1f}")

    show_boxplot(data, "pain", "Pain Score Distribution")

    question = (
        "Which factor is most likely associated with poorer quality of life based on the group summaries?"
    )
    options = [
        "Higher stage tends to have lower global QoL.",
        "Radiation always improves pain scores dramatically.",
        "Younger patients have the worst urinary symptoms.",
    ]
    correct = 1
    correct_answer = score_question(question, options, correct)
    if correct_answer:
        print("Right. Advanced stage often correlates with lower overall QoL.")
        score = 15
    else:
        print("Stage is typically a strong predictor; the other statements are not guaranteed by the summary.")
        score = 7
    return score


def main():
    random.seed(14)
    print_intro()
    data = generate_patient_data(n_patients=60, missing_rate=0.1)
    display_patient_summary(data)

    total_score = 0
    total_score += play_level_one(data)
    total_score += play_level_two(data)
    total_score += play_level_three(data)

    cleaned_data = simple_cleaning(data)
    if len(cleaned_data) < len(data):
        print("\nYou also completed a cleaning step: incomplete records were removed.")
    total_score += play_level_four(cleaned_data)

    print("\nGame complete!")
    print(f"Your final score: {total_score}/45")
    if total_score >= 35:
        print("Excellent work — you understand QoL data concepts well.")
    elif total_score >= 25:
        print("Good job — you are on the right track.")
    else:
        print("Keep practicing your epidemiology and QoL interpretation skills.")

    print("\nOptional improvement ideas:")
    print("- Add a questionnaire scoring function to mimic QLQ-C30 item aggregation.")
    print("- Use pandas to build and inspect a DataFrame.")
    print("- Add a final recommendation step to suggest which patient groups need supportive care.")


if __name__ == "__main__":
    main()