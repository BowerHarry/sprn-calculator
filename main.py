# This program is a calculator that can handle postfix and infix notation.
import operator

# Initialising global lists and dictionaries.
stack = []
randomCount = 0
operatorStack = []
# Pairs operators in the form of strings to the operator's functionality. Uses the operator library for add(), sub(), mul(), truediv(), mod() and pow()
operatorDict = { "+": operator.add, "-": operator.sub, '*': operator.mul, '/': operator.truediv, '%': operator.mod, '^': operator.pow}

# This procedure checks to see if a character is an integer.
def intCheck(userInput):
  # Checks if the stack has reached maximum capacity.
  if stackErrorCheck("integer") != True:
    # If no error when converting the str to an int it must be an integer.
    try:
      userInput = int (userInput)
      stack.append(maxMinValue(userInput))
    except ValueError:
      print('Unrecognised operator or operand "' + str(userInput) + '".')

# This procedure evaluates the top two integers on the stack with an operand.  
def calcResult(operand):
  # Checks if there are at least two integers on the stack.
  if stackErrorCheck("operator") != True:
    # Chooses the top two integers on the stack.
    x = stack[len(stack)-1]
    y = stack[len(stack)-2]
    # Checks for potential maths errors
    if calcErrorCheck(x, y, operand) != True:
      # Evaluates the integers with the operand and accounts for saturation
      result = maxMinValue(operatorDict[operand](y, x))
      stack.remove(x)
      stack.remove(y)
      stack.append(result)
  
# This function returns True for maths errors that crash the program.
def calcErrorCheck(x, y, operand):
  # Checks for dividing by 0 eg. x/0.
  if operand == "/":
    if x == 0:
      print("Divide by 0.")
      return True
  # Checks for xmod0 and 0mody.
  elif operand == "%":
    if y == 0:
      print("Divide by 0.")
      return True
    # Emulates the original program which crashes under 0mody.
    elif x == 0:
      exit()
  # Checks for trying to raise a number to a negative power.
  elif operand == "^":
    if x < 0:
      print("Negative power.")
      return True

# This function handles integer saturation and returns an integer between the saturation limits.  . 
def maxMinValue(value):
  maxValue = 2147483647
  if value > maxValue:
    # Maximum value is 2147483647.
    value = maxValue
  elif value < -maxValue:
    # Minimum value is -2147483648.
    value = -maxValue - 1
  return value

# This procedure prints the contents of the stack.
def printStack():
  # For every element in the stack it prints the element.
  for i in range (len(stack)):
    print(int(stack[i]))
  # Emulating original program.
  if len(stack) == 0:
    print(-2147483648)

# This function returns True for stack underflow/overflow/empty errors.
def stackErrorCheck(identifier):
  stackLen = len(stack)
  # When trying to evaluate two integers with an operand, it checks there are at least two integers on the stack.
  if (stackLen < 2) and identifier == "operator":
    print ("Stack underflow.")
    return True
  # When trying to add an integer to the stack, it checks for room on the stack. Maximum capacity is 23.
  elif stackLen == 23:
    print("Stack overflow.")
    return True
  # When trying to print the result, checks that there is at least one element on the stack.
  elif (stackLen == 0) and identifier == "result":
    print("Stack empty.") 

# This procedure adds a 'random' number to the stack.
def randomInt(randomCount):
  # List of potential 'random' numbers from the original program
  randomNumbers = [1804289383, 846930886, 1681692777, 1714636915, 1957747793, 424238335, 719885386, 1649760492, 596516649, 1189641421, 1025202362, 1350490027, 783368690, 1102520059, 2044897763, 1967513926, 1365180540, 1540383426, 304089172, 1303455736, 35005211, 521595368]
  # Checks that there is room on the stack
  if stackErrorCheck("integer") != True:
    # Everytime a random number is needed it takes the next number from the list.
    if randomCount == 22:
      # When at the end of the list it returns to the start.
      randomCount = randomCount - 22
      stack.append(randomNumbers[randomCount])
    else:
      stack.append(randomNumbers[randomCount])

# This procedure prints the integer at the top of the stack.
def printResult():
  # Checks that the stack isnt empty.
  if stackErrorCheck("result") != True:
    print(int(stack[len(stack)-1]))

# This procedure converts octal to decimal and then adds it to the stack.
def octal(octalNumber):
  # Checks that there are no 8's or 9's, these are not in base 8.
  if octalNumber.find("8") != -1 and octalNumber.find("9") != -1:
    # Emulating original program, if the length > 20 and it is positive it evaluates to -1.
    if len(str(octalNumber)) > 20 and octalNumber > 0:
      decimalNumber = -1
    # Emulating original program, if the length > 20 and it is negative it evaluates to -1.
    elif len(str(octalNumber)) > 20 and octalNumber < 0:
      decimalNumber = 0
    else:
      # Converts from base 8 to base 10 and accounts for saturation.
      decimalNumber = maxMinValue(int(octalNumber, 8))
    stack.append(decimalNumber)
  else:
    stack.append(maxMinValue(int(octalNumber)))

# This procedure handles operators under infix notation and adds them to operatorStack.
def operatorHandler(operator):
  # Dictionary maps each operator to its precedance over other operators.
  operatorPrecedence = {"^": 3, "*": 2, "/": 2, "%": 2, "+": 1, "-": 1}
  # Will loop until the right position for the operator in the stack is found.
  while True:
    i=0
    # If the stack is empty then add the operator to the stack.
    if len(operatorStack) == 0:
      operatorStack.append(operator)
      break
    # If the new operator has priority over the operator in position i of the list, then insert it into this position.
    elif operatorPrecedence[operator] > operatorPrecedence[operatorStack[i]]:
      operatorStack.insert(i, operator)
      break
    # If they have the same priority then evaluate the operator already on the list with the top two integers on the stack.
    elif operatorPrecedence[operator] == operatorPrecedence[operatorStack[i]]:
      calcResult(operatorStack[i])
      operatorStack.pop(i)
      # Then replace the old operator in the list with the new operator.
      operatorStack.insert(i, operator)
      break
    # If the end of the list has been reached then add the operator to the end of the list.
    elif i == len(operatorStack):
      operatorStack.append(operator) 
    i+=1

# This procedure clears the operatorStack.
def clearOperatorStack():
  # For every operator on the stack, evaluate the top two integers on the main stack.
  for i in range (len(operatorStack)):
    calcResult(operatorStack[i])
  # Clears the operatorStack
  operatorStack.clear()

# This function returns a list after userInput has been interpreted to include int > 9 and int < 0.
def interpreter(userInput):
  inputList = list(userInput)
  intString = ""
  newList = []
  i = 0
  # For every element in the list...
  for token in inputList:
    # If that element is an integer...
    if (token.isdigit() == True):
      # Check if the element that precedes the integer is "-"
      if inputList[i-1] == "-":
        # If there is not an element that preceds the "-" or if it is a space or an operator...
        if inputList[i-2] == " " or inputList[i-2] in operatorDict or i==1:
          # Then the integer is negative.
          intString = '-' + intString[0:]
          newList.pop()
      # Succesive integers without interruption are added to create numbers of larger magnitude.
      intString = intString + token
    # If there is an interruption in the digits then the integer has 'finished'.
    else:
      # Assuming the string is not empty, add it to the 'interpreted userInput list'.
      if intString != "":
        newList.append(intString)
        intString = ""
      newList.append(token)
    i += 1
  if intString != "":
    newList.append(intString)
  return newList 

# This function returns True/False depending on whether userInput is infix/postfix notation.
def infixOrSPRN(userInput):
  tokenCount = len(interpreter(userInput))
  userInput = interpreter(userInput)
  i = 0
  # If " " and then "=" is contained in the list, we remove it as it has no affect on infix/postfix.
  while True:
    if userInput[i] == " ":
      if userInput[i+1] == "=":
        userInput.pop(i+1)
        userInput.pop(i)
        break
      else:
        pass
    elif (i+1) >= len(userInput):
      break
    i+=1  
  # If there is more than one element in the interpreted list and it contains no spaces...
  if (tokenCount > 1) and (" " not in userInput):
    # Return True as infix notation.
    return True
  # Otherwise it is postfix.
  else:
    return False

# This procedure links the interpretating and calculating of userInput.
def calculator(userInput, infixOn):
  global randomCount
  # If the element is an operator...
  if userInput in operatorDict:
    # If using infix notation call the function for handling infix operators.
    if infixOn == True:
      operatorHandler(userInput)
    #If using postfix then evaluate the top two integers on the stack with the operator.
    else:
      calcResult(userInput)
  # If the element is "d" then print the stack.
  elif userInput == "d":
    printStack()
  # If the element is "r" then add a 'random' integer to the stack.
  elif userInput == "r":
    randomInt(randomCount)
    randomCount += 1
  elif (userInput == " ") or (userInput == ""):
    pass
  # If the element is "=" then clear operatorStack and print the integer on top of the stack.
  elif userInput == "=":
    clearOperatorStack()
    printResult()
  # If the element begins with "0" it should be treated as an octal number and added to the stack.
  elif (userInput.startswith("0")) or (userInput.startswith("-0")):
    octal(userInput)
  # If the element is an integer, add it to the stack.
  else:
    intCheck(userInput)

# This function returns False when there is comments in userInput.
def commentCheck(userInput, commentStart, commentEnd, calculatorOn):
  for i in range(len(userInput)):
    # If in userInput a # is followed by a space then return False. This turns the calculator 'off'.
    if (userInput[i] == "#") and (calculatorOn == True):
      if userInput[i+1] == " ":
        calculatorOn = False
        commentStart = i
    # If the calculator is 'off' then a # will end the comment and turn it back on.
    elif (userInput[i] == "#") and (calculatorOn == False):
      calculatorOn = True
      commentEnd = i+1
  # Everything between the #'s is removed from userInput.
  userInput = userInput[:commentStart] + userInput[commentEnd:]
  return userInput, calculatorOn

def main():
  print ("You can now start interacting with the SRPN calculator")
  calculatorOn = True
  while (True):
    # Input from user stored in userInput.
    userInput = input()
    # infixOn is True when userInput is infix notation.
    infixOn = infixOrSPRN(userInput)
    # Prevents comments from being read by the calculator.
    userInput, calculatorOn = commentCheck(userInput, 0, 0, calculatorOn)
    if calculatorOn == True:
      # Turns userInput into a list that now also includes int<0 and int>9.
      userInput = interpreter(userInput)
      # Evaluates userInput.
      for token in userInput:
        calculator(token, infixOn)
        
      clearOperatorStack()
     


main()