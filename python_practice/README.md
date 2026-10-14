# Python Practice - Test Cases

## Problem 4: Exception Handling

Neeche diye gaye table mein division function (`divide_numbers`) ke test cases aur unke expected results hain:

| Test Case | Input (`a`, `b`) |      Situation       |   Expected Output / Result    |  Status  |
| :-------- | :--------------- | :------------------- | :---------------------------- | :------- |
|   **1**   |     `10`, `2`    |    Normal division   |  `5.0` (Successful division)  | **Pass** |
|   **2**   |     `10`, `0`    |    Divide by Zero    | Error message, returns `None` | **Pass** |
|   **3**   |     `10`, `"a"`  |    Input letter      | Error message, returns `None` | **Pass** |

### Code Behavior:
- When we run **Test Case 1**, division will be successfull.
- When we run **Test Case 2** or **3**, the program will not crash, `try-except` block will print error message safely.