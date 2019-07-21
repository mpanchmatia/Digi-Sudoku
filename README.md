# Digi-Sudoku
Python Flask based application to solve Sudoku puzzle.
## Why name : “Digi-Sudoku” ?
* Root: Digital Electronics
* My github repository
  * https://github.com/mpanchmatia/TabulationMethod
  * Quine–McCluskey algorithm (‘Tabulation Method’)
  * To design digital circuit with AND and OR gates
* The candidate values are stored as bitmap for empty cells. Bitmaps and bitwise operators optimize memory utilization. 
## Overall Architecture
![Overall Architecture](/images/OverAllArch.gif)
### Future Scope
* The architecture can be expanded as full-fledged website / mobile app, with user authentication, competition, prizes, usage analytics etc. 
* The solution can be modified to deploy on micro-service based,  server-less architecture. 
* Sudoku puzzles can be stored in database with its various attributes like category (easy, medium, hard), comments, hints, popularity etc.
## Approach
### Algorithms for human
* There are some basic techniques, advance techniques and expert techniques to solve Sudoku
* Expert Techniques are more suitable for human with visual analysis of the Sudoku grid
  * The XWing  Techniques
  * The Swordfish Techniques 
  * etc.
### Algorithms for computer software
* Computer algorithm can use ‘burst force’ approach by evaluating all possible values for all empty solution. It will more CPU & memory intensive, due to its iterative process.  
* The best possible software approach can be combination of ‘burst force’ and other techniques
### Approach in this "Digi-Sudoku" application
* The ‘Digi-Sudoku’ application implements some of the basic techniques and advance techniques
  * Function Zero: SingleCandidate
  * Function One: ExplicitRegion
  * Function Two: ImplicitRegion
  * Function Three: CandidateLineTechnique
  * Function Four: MultipleLinesTechnique 
* These techniques are called in sequence as per FSM (Finite State Machine)
### Finite State Machine
![Finite State Machine](/images/FSM.gif)
### Future Scope
* The ‘Digi-Sudoku’ application can be extended with additional sophisticated algorithms
* Some heuristic rules can be also added to choose appropriate algorithm
* The FSM flow can be optimized. For example: every time, going back to ‘candidate algorithm’ can be avoided
## Use Cases
### For End-User
* Add new Sudoku puzzle
* Display randomly selected Sudoku puzzle
* Display specific Sudoku puzzle
* Solve Sudoku puzzle
### For Developer
* Display all Sudoku puzzles
* Test all Sudoku puzzles
  * Unit Testing
  * Performance Measurement
### Execution Flow : End-User
![Execution Flow : End-User](/images/ExecutionFlowEndUser.gif)
#### Future Scope
* The ‘Digi-Sudoku’ application can be enhanced with more UI and UX features
* The application can reveal value for specific empty cell, as per user’s request as hint
* The application can allow user to solve the Sudoku puzzle.
* The application can allow user to add candidate values for empty cell. 
* Better error handling and error reporting.
### Execution Flow : Developer
#### Unit Testing and Performance Measurement
* After uncommenting PrintOptions function: http://<host:port>/test_all can be invoked
* The test case pass / fail summary will be displayed in browser
* Further debugging is possible from console log
* The additional code can be instrumented for performance measurement.
#### Accessing all Sudoku Puzzles
![Execution Flow : Developer](/images/ExecutionFlowDeveloper.gif)
## Naming Conventions
### Variables
* Region is collection of cells
* Region = Block | Line
* Line = Row | Column
* Region is defined as list of cellIndex listCellIndexInRegion
* blockIndex, rowIndex and columnIndex range is 0 to 8
* cellIndex range is 0 to 80
* digit range is 1 to 9
* The member variable options is a dictionary with cellIndex as key and bitmap for all possible candidate values
* The member variable output is also a dictionary with cellIndex as key and final single value for that specific cell. 
* Some helper functions create a reverse map dicDigit with digit as key and list of all cellIndex having that digit.
### Class
* Sudoku is abstract base class
* It has abstract methods
  * Solve
  * Load
* ClassicSudoku is concreate class for 9 x 9 Classical Sudoku
* ClassicSudoku class has specific static variables
  * size = 9
  * invert = 1022 etc.
* ClassicSudoku class has specific static methods
  * GetRowIndex
  * GetColumnIndex
  * GetBlockIndex
* These method takes cellIndex as input parameter and return index for specific region
### Algorithm Methods
* Each algorithm is implemented as function Solve<Algorithm Name>
* Most of the algorithms has helper function to work on given region with name <Algorithm Name>SolveARegion
### Future Scope
* The abstract base class Sudoku can be extended for different size of Sudoku puzzles
  * Mini Sudoku for kids 4 x 4
  * Super Sudoku 12 x 12
  * Giant Sudoku 15 x 15
  * Monster Sudoku 25 x 25
* The GetBlockIndex method can be modified to support Irregular Sudoku
* The abstract base class Sudoku can be extended for different types of Sudoku puzzles
  * Trio Sudoku
  * Odd-Even Sudoku
  * Consecutive Sudoku
  * Diagonal Sudoku
  * Irregular Sudoku
  * Kakurofied Sudoku etc.
## Refernce
* Book : “A to Z of Sudoku. Science behind Sudoku” 
  * by Narendra Jussien 
  * ISBN: 8130908573
  * ISBN13: 9788130908571
* Book : “Times Book of Gen-X Sudoku” 
  * https://www.amazon.in/Times-Gen-X-Sudoku-Mohanlal-Naresh/dp/8189906046
  * ISBN-10: 8189906046
  * ISBN-13: 978-8189906047
