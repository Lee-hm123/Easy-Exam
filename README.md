

# Easy-Exam

这是一个基于 **Tkinter** 图形界面和 **pandas** 数据处理库构建的 **考试练习应用程序**。它从 Excel 表格中读取题库数据，支持**单选题、多选题和判断题**，并提供**答题卡、计时器、错题统计、答题反馈**等功能。下面我将从整体结构、关键功能、变量解释三方面逐步说明。

------

## 🧱 一、整体结构概览

1. **数据导入与预处理**：
   - 通过 `pandas.read_excel()` 从 `py.xlsx` 读取试题数据。
   - 删除“序号”为空的行，确保每题都有编号。
   - 根据指定的题号数组选择要练习的题目。
   - 自动判断题型（单选、多选、判断）。
2. **界面布局（Tkinter GUI）**：
   - 左边区域显示：题干、题型、选项、计时器、按钮。
   - 右边区域显示：可点击跳转的“答题卡”列表。
3. **答题交互逻辑**：
   - 每题自动加载选项（不同题型用不同控件）。
   - 每次答题自动记录是否正确。
   - “提交”时统计正确数、错题数、答题时间，并显示结果。

------

## 🔑 二、关键功能说明

### 1. **题型自动识别**（get_choice_question_type）

```python
- 判断依据：
  - 判断题：只有“对”和“错”两个选项。
  - 多选题：答案中有多个字母（如 'AC'）或含有逗号。
  - 单选题：答案只有一个字母。
```

------

### 2. **题目加载与选项展示**（load_question）

```python
- 设置题干和题型提示文本。
- 根据题型显示：
  - 单选题：使用 Radiobutton（单选按钮）
  - 多选题：使用 Checkbutton（多选框）
  - 判断题：两个选项“对”和“错”
```

------

### 3. **记录答案与统计正确数**（record_answer）

```python
- 对于多选题，收集所有被选中的项，组合成字符串。
- 判断用户选项是否与正确答案一致。
- 若错误，记录题号并按题型分类计数。
```

------

### 4. **答题卡实时更新与跳题功能**（update_answer_card & jump_to_question）

```python
- 实时显示当前所有题的状态（已做/未做）。
- 点击答题卡上某一题号，可跳转至该题。
```

------

### 5. **提交与结果显示**（submit_exam）

```python
- 显示总答题数、答对数、各类题错题数、用时、错题号。
- 使用 messagebox 弹窗反馈。
```

------

### 6. **计时器**（update_timer）

```python
- 每秒自动更新一次“已用时间”标签。
```

------

### 7. **响应窗口大小自动调整文字大小**（resize_text）

```python
- 根据窗口宽度动态改变字体大小，保持良好的界面适应性。
```

------

## 📦 三、主要变量说明表

| 变量 / 函数名                                         | 类型      | 作用说明                                   |
| ----------------------------------------------------- | --------- | ------------------------------------------ |
| `df`                                                  | DataFrame | 从 Excel 读取的原始题库数据                |
| `df_selected`                                         | DataFrame | 从原题库中筛选出的指定题目                 |
| `choice_questions`                                    | list[int] | 练习的单选和多选题题号                     |
| `true_false_questions`                                | list[int] | 练习的判断题题号                           |
| `current_question_index`                              | int       | 当前显示的题目在 df_selected 中的下标      |
| `check_vars`                                          | list      | 多选题每个选项对应的变量列表               |
| `question_text`, `user_answer`, `question_type_label` | StringVar | 用于动态更新界面上的题干、选项、题型等标签 |
| `wrong_count`                                         | dict      | 错题统计，按题型分类                       |
| `wrong_question_ids`                                  | list[int] | 所有答错题目的“序号”                       |
| `answer_card_frame`                                   | Text      | 答题卡显示区域，支持跳题点击               |



------

## 数据原示例

| 序号 | 题干                           | 选项A | 选项B | 选项C  | 选项D    | 答案 | 题型   |
| ---- | ------------------------------ | ----- | ----- | ------ | -------- | ---- | ------ |
| 1    | Python 中的列表如何定义？      | []    | {}    | ()     | <>       | A    | 单选题 |
| 2    | 以下哪些是 Python 的数据类型？ | int   | float | tree   | str      | ABD  | 多选题 |
| 3    | Python 支持面向对象编程。      | 对    | 错    |        |          | 对   | 判断题 |
| 4    | 下面哪个语句可以定义函数？     | def   | let   | var    | function | A    | 单选题 |
| 5    | 以下哪些是合法变量名？         | _name | 1name | name_1 | for      | AC   | 多选题 |
| 6    | Python 是解释型语言。          | 对    | 错    |        |          | 对   | 判断题 |
