#with zoom 窗口闪烁
import tkinter as tk
from tkinter import messagebox
import pandas as pd
import time

# Load the exam data
file_path = r"D:\Data\123\py.xlsx"
df = pd.read_excel(file_path)

# Drop rows with NaN values in '序号' column
df = df.dropna(subset=['序号']).reset_index(drop=True)

# Define specific question numbers
choice_questions = [2, 9, 11, 13, 15, 18, 25, 26, 27, 32, 34, 35, 36, 42, 43, 49]  # 指定的单选和多选题号
true_false_questions = [2, 18, 19, 21, 22, 24, 47, 58, 59, 74, 75, 84, 90]  # 指定的判断题号

# Filter and remove duplicate questions from choice and true/false arrays
choice_questions = list(set(choice_questions) - set(true_false_questions))

# Initialize variables
current_question_index = 0
start_time = time.time()
correct_answers = 0
user_answers = {}
check_vars = []
wrong_count = {"单选": 0, "多选": 0, "判断": 0}  # 各题型的错题数统计
wrong_question_ids = []  # 记录错题号

# Function to determine if a question is 单选, 多选, or 判断
def get_choice_question_type(row):
    correct_answer = str(row['答案']).strip()
    options = [row['选项A'], row['选项B'], row['选项C'], row['选项D']]
    options = [o for o in options if pd.notna(o)]  # Remove NaN options

    if len(options) == 2 and all(opt in ['对', '错'] for opt in options):
        return '判断'
    elif ',' in correct_answer or len(correct_answer) > 1:
        return '多选'
    elif len(correct_answer) == 1:
        return '单选'
    else:
        return '未知'  # 处理未定义的情况

# Filter selected questions from the dataframe
df_selected = df[df['序号'].isin(choice_questions + true_false_questions)].reset_index(drop=True)
df_selected['题型'] = df_selected.apply(lambda row: get_choice_question_type(row), axis=1)

# Function to load a question by index
def load_question():
    global check_vars
    question_data = df_selected.iloc[current_question_index]

    # Set question text and question type
    question_text.set(f"题号 {int(question_data['序号'])}: {question_data['题干']}")
    question_type_label.set(f"题型: {question_data['题型']}")

    # Clear previous options
    for widget in options_frame.winfo_children():
        widget.destroy()

    # Display options based on question type
    question_type = question_data['题型']
    check_vars.clear()
    user_answer.set("")  # Clear previous single answer selection for 单选和 判断

    if question_type == '单选':
        for option_label in ['选项A', '选项B', '选项C', '选项D']:
            option = question_data.get(option_label)
            if pd.notna(option):
                rb = tk.Radiobutton(options_frame, text=option, variable=user_answer, value=option_label[-1])
                rb.pack(anchor='w')
    elif question_type == '多选':
        for option_label in ['选项A', '选项B', '选项C', '选项D']:
            option = question_data.get(option_label)
            if pd.notna(option):
                cb_var = tk.StringVar(value="0")
                cb = tk.Checkbutton(options_frame, text=option, variable=cb_var, onvalue=option_label[-1], offvalue="0")
                cb.pack(anchor='w')
                check_vars.append(cb_var)
    elif question_type == '判断':
        tk.Radiobutton(options_frame, text="对", variable=user_answer, value="对").pack(anchor='w')
        tk.Radiobutton(options_frame, text="错", variable=user_answer, value="错").pack(anchor='w')

    # Update answer card
    update_answer_card()

# Function to handle next question button
def next_question():
    global current_question_index, correct_answers
    record_answer()

    # Move to the next question if available
    if current_question_index + 1 < len(df_selected):
        current_question_index += 1
        load_question()
    else:
        messagebox.showinfo("提示", "已是最后一题")

# Function to record the answer for the current question
def record_answer():
    global correct_answers
    question_data = df_selected.iloc[current_question_index]
    correct_answer = str(question_data['答案']).strip()

    if question_data['题型'] == '多选':
        selected_answers = "".join([var.get() for var in check_vars if var.get() != "0"])
    else:
        selected_answers = user_answer.get()

    is_correct = selected_answers == correct_answer
    user_answers[current_question_index] = is_correct
    if is_correct:
        correct_answers += 1
    else:
        wrong_count[question_data['题型']] += 1
        wrong_question_ids.append(int(question_data['序号']))

# Function to display the answer card with clickable question numbers
def update_answer_card():
    answer_card_frame.delete("1.0", tk.END)
    for index, row in df_selected.iterrows():
        question_number = int(row['序号'])
        question_type = row['题型']
        status = "已做" if index in user_answers else "未做"

        # Create a clickable label for each question
        answer_card_frame.insert(tk.END, f"题号 {question_number} - {question_type} - {status}\n", f"question_{index}")
        answer_card_frame.tag_bind(f"question_{index}", "<Button-1>", lambda e, idx=index: jump_to_question(idx))

# Function to jump to a specific question by index
def jump_to_question(index):
    global current_question_index
    current_question_index = index
    load_question()

# Function to submit exam, calculate wrong answers, and show results
def submit_exam():
    elapsed_time = time.time() - start_time
    wrong_answers = len(df_selected) - correct_answers
    result_message = (
        f"你答对了 {correct_answers}/{len(df_selected)} 道题\n"
        f"错题数：{wrong_answers}\n"
        f"已用时间：{int(elapsed_time)} 秒\n"
        f"单选错题数：{wrong_count['单选']}\n"
        f"多选错题数：{wrong_count['多选']}\n"
        f"判断错题数：{wrong_count['判断']}\n"
        f"错题号：{', '.join(map(str, wrong_question_ids))}"
    )
    messagebox.showinfo("考试结果", result_message)

# Function to update the timer label
def update_timer():
    elapsed_time = int(time.time() - start_time)
    timer_label.config(text=f"已用时间: {elapsed_time} 秒")
    app.after(1000, update_timer)

# Function to resize text dynamically
def resize_text(event):
    new_size = min(event.width // 50, 12)  # Adjust scaling factor as needed
    question_text_label.config(font=("Arial", new_size))
    question_type_label_widget.config(font=("Arial", new_size))
    timer_label.config(font=("Arial", new_size))
    answer_card_frame.config(font=("Arial", new_size))

# Initialize GUI application
app = tk.Tk()
app.title("考试练习应用")

# Bind resize event
app.bind("<Configure>", resize_text)

# Layout setup with left and right frames
left_frame = tk.Frame(app)
left_frame.pack(side=tk.LEFT, padx=20, pady=20)

right_frame = tk.Frame(app)
right_frame.pack(side=tk.RIGHT, padx=20, pady=20)

# Track user responses and display question content
question_text = tk.StringVar()
question_type_label = tk.StringVar()
user_answer = tk.StringVar()

# Layout for question and options on the left
question_text_label = tk.Label(left_frame, textvariable=question_text, wraplength=400)
question_text_label.pack(pady=10)
question_type_label_widget = tk.Label(left_frame, textvariable=question_type_label)
question_type_label_widget.pack(pady=5)
options_frame = tk.Frame(left_frame)
options_frame.pack()

# Timer display
timer_label = tk.Label(left_frame, text="已用时间: 0 秒")
timer_label.pack()
update_timer()

# Next question button and Submit button
tk.Button(left_frame, text="下一题", command=next_question).pack(pady=10)
tk.Button(left_frame, text="提交", command=submit_exam).pack(pady=10)

# Answer card display on the right
tk.Label(right_frame, text="答题卡").pack()
answer_card_frame = tk.Text(right_frame, height=20, width=30)
answer_card_frame.pack()

# Load initial question
load_question()

# Run the app
app.mainloop()
