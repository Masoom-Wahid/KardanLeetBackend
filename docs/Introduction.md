# Introduction
<hr>

## This Is An Introduction , Api Documentation Of Each Part Are Below:
* ### [Auth](./Auth.md)
* ### [Contest](./Contest.md)
* ### [Question](./Question.md)
* ### [Competetion](./Competetion.md)

<hr>

### How Does It Work???
* #### It All has to do with how the files are structured, For example for Inputs
```shell
├── contest -RootDirectory
│   └── Autumn_2022 -ContestName
│       ├── Factorial_of_10_nums -QuestionName
│       │   ├── Autumn_2022__Factorial_of_10_nums__input10.txt -QuestionInputFiles
│       │   ├── Autumn_2022__Factorial_of_10_nums__input11.txt
│       │   ├── Autumn_2022__Factorial_of_10_nums__input12.txt
│       │   ├── Autumn_2022__Factorial_of_10_nums__input13.txt
│       │   ├── Autumn_2022__Factorial_of_10_nums__input14.txt
│       │   ├── Autumn_2022__Factorial_of_10_nums__input15.txt
│       │   ├── Autumn_2022__Factorial_of_10_nums__input16.txt
│       │   ├── Autumn_2022__Factorial_of_10_nums__input17.txt
│       │   ├── Autumn_2022__Factorial_of_10_nums__input18.txt
│       │   ├── Autumn_2022__Factorial_of_10_nums__input19.txt
│       │   ├── Autumn_2022__Factorial_of_10_nums__input1.txt
│       ├── Maze -QuestionName
│       │   ├── Autumn_2022__Maze__input1.txt -QuestionInputFiles
│       │   ├── Autumn_2022__Maze__input2.txt
│       │   ├── Autumn_2022__Maze__input3.txt
│       │   ├── Autumn_2022__Maze__input4.txt
│       │   ├── Autumn_2022__Maze__output1.txt
│       │   ├── Autumn_2022__Maze__output2.txt
│       │   ├── Autumn_2022__Maze__output3.txt
│       │   └── Autumn_2022__Maze__output4.txt
│       └── Powerof -QuestionName
│           ├── Autumn_2022__Powerof__input1.txt -QuestionInputFiles
│           ├── Autumn_2022__Powerof__input2.txt
│           ├── Autumn_2022__Powerof__output1.txt
│           └── Autumn_2022__Powerof__output2.txt
└── temp_files
```
<hr>

* #### The Folder are made like this So that when requiring the Inputs We Already know Where They Are At
<br>

* #### So Everytime Submit Or Run Your File we Compile the Given File and then run them on the number of testCases they have and their specific loactions
<br>

* #### It also has RealTime LeaderBoard which Ranks The Users Based On Their Point,Time and Penalty
<hr>

## :grey_exclamation: If Interested In Using The Api Start With Here [here](./Auth.md)