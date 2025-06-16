// Calculator state
let currentInput = '';
let expression = '';
let shouldResetDisplay = false;
let lastOperator = '';
let history = [];

// DOM elements
const expressionDisplay = document.getElementById('expression');
const resultDisplay = document.getElementById('result');
const historySection = document.getElementById('history-section');
const historyList = document.getElementById('history-list');

// Initialize calculator
function initCalculator() {
    updateDisplay();
    loadHistory();
}

// Update display
function updateDisplay() {
    expressionDisplay.textContent = expression;
    resultDisplay.textContent = currentInput || '0';
}

// Input number
function inputNumber(num) {
    if (shouldResetDisplay) {
        currentInput = '';
        shouldResetDisplay = false;
    }
    
    if (num === '0' && currentInput === '0') return; // prevent multiple leading zeros
    if (currentInput === '0' && num !== '.') currentInput = '';
    
    currentInput += num;
    updateDisplay();
}

// Input decimal point
function inputDecimal() {
    if (shouldResetDisplay) {
        currentInput = '0';
        shouldResetDisplay = false;
    }
    
    if (currentInput === '') currentInput = '0';
    if (currentInput.includes('.')) return;
    
    currentInput += '.';
    updateDisplay();
}

// Input operator
function inputOperator(operator) {
    // Remove active state from all operator buttons
    document.querySelectorAll('.btn-operator').forEach(btn => {
        btn.classList.remove('active');
    });

    // Add active state to current operator button
    const operatorMap = { '+': '+', '-': '-', '*': '×', '/': '÷' };
    document.querySelectorAll('.btn-operator').forEach(btn => {
        if (btn.textContent === operatorMap[operator]) {
            btn.classList.add('active');
        }
    });

    if (currentInput === '' && expression === '') return;
    
    if (currentInput !== '') {
        if (expression !== '' && !shouldResetDisplay) {
            calculate(false);
        }
        expression = currentInput + ' ' + getOperatorSymbol(operator) + ' ';
        currentInput = '';
    } else if (expression !== '') {
        // Replace the last operator
        expression = expression.slice(0, -3) + ' ' + getOperatorSymbol(operator) + ' ';
    }
    
    lastOperator = operator;
    shouldResetDisplay = false;
    updateDisplay();
}

// Get operator symbol for display
function getOperatorSymbol(operator) {
    const symbols = { '+': '+', '-': '-', '*': '×', '/': '÷' };
    return symbols[operator] || operator;
}

// Calculate result
function calculate(addToHistoryFlag = true) {
    if (expression === '' || currentInput === '') return;
    
    try {
        const fullExpression = expression + currentInput;
        console.log('Expression à évaluer:', fullExpression);
        
        // Convert display symbols to JS operators, remove spaces
        const jsExpression = fullExpression
            .replace(/×/g, '*')
            .replace(/÷/g, '/')
            .replace(/\s+/g, '');
        
        console.log('JS Expression:', jsExpression);
        
        const result = eval(jsExpression);
        
        if (!isFinite(result)) {
            throw new Error('Invalid calculation');
        }
        
        const roundedResult = Math.round(result * 1e8) / 1e8;
        
        if (addToHistoryFlag) {
            addToHistory(fullExpression + ' = ' + roundedResult);
        }
        
        currentInput = roundedResult.toString();
        expression = '';
        shouldResetDisplay = true;
        
        document.querySelectorAll('.btn-operator').forEach(btn => btn.classList.remove('active'));
        
    } catch (error) {
        console.error(error);
        currentInput = 'Error';
        expression = '';
        shouldResetDisplay = true;
    }
    
    updateDisplay();
}

// Clear calculator
function clearCalculator() {
    currentInput = '';
    expression = '';
    shouldResetDisplay = false;
    lastOperator = '';
    
    document.querySelectorAll('.btn-operator').forEach(btn => btn.classList.remove('active'));
    
    updateDisplay();
}

// Backspace function
function backspace() {
    if (shouldResetDisplay) {
        clearCalculator();
        return;
    }
    
    if (currentInput.length > 0) {
        currentInput = currentInput.slice(0, -1);
    } else if (expression.length > 0) {
        // Remove last operator and spaces if needed
        expression = expression.trimEnd();
        expression = expression.slice(0, expression.lastIndexOf(' '));
        if (!expression.endsWith(' ')) expression += ' ';
    }
    
    updateDisplay();
}

// History functions
function addToHistory(calculation) {
    history.unshift(calculation);
    if (history.length > 10) {
        history = history.slice(0, 10);
    }
    saveHistory();
    displayHistory();
}

function displayHistory() {
    if (history.length === 0) {
        historySection.style.display = 'none';
        return;
    }
    
    historySection.style.display = 'block';
    historyList.innerHTML = '';
    
    history.forEach(calculation => {
        const historyItem = document.createElement('div');
        historyItem.className = 'history-item';
        historyItem.textContent = calculation;
        historyItem.onclick = () => {
            const parts = calculation.split(' = ');
            if (parts.length === 2) {
                currentInput = parts[1];
                expression = '';
                shouldResetDisplay = true;
                updateDisplay();
            }
        };
        historyList.appendChild(historyItem);
    });
}

function saveHistory() {
    try {
        // Optionally implement localStorage saving here
    } catch (error) {
        console.log('History saving not available');
    }
}

function loadHistory() {
    try {
        // Optionally implement localStorage loading here
        displayHistory();
    } catch (error) {
        console.log('History loading not available');
    }
}

// Keyboard support
document.addEventListener('keydown', function(event) {
    const key = event.key;
    
    if (key >= '0' && key <= '9') {
        inputNumber(key);
    } else if (key === '.') {
        inputDecimal();
    } else if (key === '+') {
        inputOperator('+');
    } else if (key === '-') {
        inputOperator('-');
    } else if (key === '*') {
        inputOperator('*');
    } else if (key === '/') {
        inputOperator('/');
    } else if (key === 'Enter' || key === '=') {
        event.preventDefault();
        calculate();
    } else if (key === 'Escape' || key.toLowerCase() === 'c') {
        clearCalculator();
    } else if (key === 'Backspace') {
        backspace();
    }
});

// Initialize calculator when page loads
window.addEventListener('load', initCalculator);
