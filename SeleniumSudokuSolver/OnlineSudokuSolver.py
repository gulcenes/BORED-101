from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from shutil import which
import time
import keyboard
import numpy as np


def possible(board, y, x, val):
    # Check rows
    if val in board[y]:  
        return False
    
    # Check cols
    for v in range(9):  
        if board[v][x] == val:
            return False

    # Check Squares
    sqy = (y // 3) * 3 
    sqx = (x // 3) * 3 

    for r in range(sqy, sqy + 3):
        for c in range(sqx, sqx + 3):
            if board[r][c] == val:
                return False
    return True


def find_empty(board):
    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:
                return r, c

    return None


def solve(board):
    empty_cell = find_empty(board)

    if not empty_cell:
        return True
    else:
        row, col = empty_cell

    for i in range(1, 10):
        if possible(board, row, col, i):
            board[row][col] = i

            if solve(board):
                return True

            board[row][col] = 0

    return False

# Selenium Driver
chrome_path = which("chromedriver")
driver = webdriver.Chrome(executable_path=chrome_path)

# Target
driver.get("https://sudoku.com/expert/")

# Wait until Page loads
try:
    myElem = WebDriverWait(driver, 4).until(EC.presence_of_element_located((By.CLASS_NAME, 'game-table')))
    print("Ready!")
except TimeoutException:
    print("TIME OUT!")
    
## or time.sleep(4)

# Numpad
numpad_elements = driver.find_elements(By.XPATH, "//div[@class='numpad-item']/*[name()='svg']/*[name()='path']")
numpad_attributes = [i.get_attribute('d') for i in numpad_elements]
numpad = dict(zip(numpad_attributes, range(1,10)))

# Table
table = []

table_values = driver.find_elements(By.XPATH, "//tr[@class='game-row']/*/div[@class='cell-value']")

for cell in table_values:
        
    try:
        cell_value = cell.find_element_by_xpath(".//*[name()='svg']/*[name()='path']")
        if cell_value:
            table.append(numpad[cell_value.get_attribute('d')])
    except:
        table.append(0)

# Reshape Table (9,9)
table = [table[n:n+9] for n in range(0, len(table), 9)]

# Find Zeros
zeros = np.argwhere(np.matrix(table) == 0)

# Solve
solve(table)

# Get filled values
filled_values = [table[i[0]][i[1]] for i in zeros]

# Get empty cells positions
empty_cells = driver.find_elements_by_xpath("//div[@class='cell-value'][not(./*[name()='svg'])]/parent::td")

# Match empty cells and filled values
matched_cell_values = [(empty_cells[i], filled_values[i]) for i in range(0, len(filled_values))]

# And Action
for cell in matched_cell_values:
    cell[0].click()
    keyboard.press_and_release(str(cell[1]))

    


