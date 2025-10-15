import tkinter as tk
from tkinter import scrolledtext, messagebox
import random
import re

class ProgrammingQuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Programming Quiz Master")
        self.root.geometry("950x750")
        self.root.configure(bg="#6366f1")
        
        # Quiz state
        self.mode = None
        self.difficulty = None
        self.selected_language = None
        self.language_display_name = None
        self.notes = ""
        self.questions = []
        self.current_question = 0
        self.score = 0
        self.time_left = 0
        self.timer_id = None
        self.selected_answer = None
        
        # Language-specific question banks
        self.language_questions = {
            'python': {
                'easy': [
                    {
                        'question': "Which symbol is used for single-line comments in Python?",
                        'options': ["//", "#", "/*", "<!--"],
                        'correct': 1
                    },
                    {
                        'question': "What is the output of: print(type([]))?",
                        'options': ["<class 'array'>", "<class 'list'>", "<class 'tuple'>", "<class 'dict'>"],
                        'correct': 1
                    },
                    {
                        'question': "How do you create a variable in Python?",
                        'options': ["x = 5", "int x = 5", "var x = 5", "let x = 5"],
                        'correct': 0
                    },
                    {
                        'question': "Which keyword is used to define a function in Python?",
                        'options': ["function", "def", "func", "define"],
                        'correct': 1
                    }
                ],
                'medium': [
                    {
                        'question': "In Python, what is a decorator?",
                        'options': ["A design pattern", "A function that modifies another function", 
                                   "A class method", "A variable type"],
                        'correct': 1
                    },
                    {
                        'question': "What is a list comprehension in Python?",
                        'options': ["A loop structure", "A concise way to create lists", 
                                   "A function type", "A data structure"],
                        'correct': 1
                    },
                    {
                        'question': "What does the 'self' parameter represent in Python classes?",
                        'options': ["The class itself", "The instance of the class", 
                                   "A global variable", "The parent class"],
                        'correct': 1
                    },
                    {
                        'question': "What is the difference between a list and a tuple in Python?",
                        'options': ["No difference", "Tuples are immutable, lists are mutable", 
                                   "Lists are faster", "Tuples can't store numbers"],
                        'correct': 1
                    }
                ],
                'hard': [
                    {
                        'question': "In Python, what is the difference between deepcopy and shallow copy?",
                        'options': ["No difference", "Deepcopy copies nested objects, shallow doesn't", 
                                   "Shallow is faster", "Deepcopy is deprecated"],
                        'correct': 1
                    },
                    {
                        'question': "What is a generator in Python?",
                        'options': ["A random number creator", "A function that returns an iterator using yield", 
                                   "A class type", "A module"],
                        'correct': 1
                    },
                    {
                        'question': "What is the Global Interpreter Lock (GIL) in Python?",
                        'options': ["A security feature", "A mutex preventing multiple threads from executing Python bytecode", 
                                   "A compiler optimization", "A memory manager"],
                        'correct': 1
                    },
                    {
                        'question': "What are metaclasses in Python?",
                        'options': ["Parent classes", "Classes of classes", "Abstract classes", "Static classes"],
                        'correct': 1
                    }
                ]
            },
            'java': {
                'easy': [
                    {
                        'question': "Which of these is NOT a primitive data type in Java?",
                        'options': ["int", "boolean", "string", "char"],
                        'correct': 2
                    },
                    {
                        'question': "What is the entry point of a Java program?",
                        'options': ["start()", "main()", "run()", "execute()"],
                        'correct': 1
                    },
                    {
                        'question': "Which keyword is used to inherit a class in Java?",
                        'options': ["inherits", "extends", "implements", "inherit"],
                        'correct': 1
                    },
                    {
                        'question': "How do you create an object in Java?",
                        'options': ["new ClassName()", "create ClassName()", "ClassName.new()", "object ClassName()"],
                        'correct': 0
                    }
                ],
                'medium': [
                    {
                        'question': "What is method overloading in Java?",
                        'options': ["Multiple methods with same name but different parameters", 
                                   "Overriding parent class method", "Creating too many methods", 
                                   "Method with multiple return types"],
                        'correct': 0
                    },
                    {
                        'question': "What is the difference between abstract class and interface?",
                        'options': ["No difference", "Abstract class can have implementation, interface cannot (before Java 8)", 
                                   "Interface is faster", "Abstract class is deprecated"],
                        'correct': 1
                    },
                    {
                        'question': "What is autoboxing in Java?",
                        'options': ["Automatic garbage collection", "Automatic conversion between primitive and wrapper types", 
                                   "Automatic method calling", "Automatic inheritance"],
                        'correct': 1
                    },
                    {
                        'question': "What is the purpose of the 'final' keyword in Java?",
                        'options': ["To end a program", "To make variables constant, methods non-overridable, classes non-inheritable", 
                                   "To finalize objects", "To create final results"],
                        'correct': 1
                    }
                ],
                'hard': [
                    {
                        'question': "What is the purpose of 'volatile' keyword in Java?",
                        'options': ["Makes variable constant", "Ensures visibility across threads", 
                                   "Speeds up access", "Prevents inheritance"],
                        'correct': 1
                    },
                    {
                        'question': "What is the difference between HashMap and ConcurrentHashMap?",
                        'options': ["No difference", "ConcurrentHashMap is thread-safe", 
                                   "HashMap is faster", "ConcurrentHashMap is deprecated"],
                        'correct': 1
                    },
                    {
                        'question': "What is the Java Memory Model?",
                        'options': ["A design pattern", "Specification defining how threads interact through memory", 
                                   "A garbage collector", "A memory allocation strategy"],
                        'correct': 1
                    },
                    {
                        'question': "What are lambda expressions in Java 8?",
                        'options': ["Greek letters", "Anonymous functions implementing functional interfaces", 
                                   "Design patterns", "Class types"],
                        'correct': 1
                    }
                ]
            },
            'cpp': {
                'easy': [
                    {
                        'question': "In C++, which operator is used to access a member of a class?",
                        'options': [".", "->", "::", "All of the above"],
                        'correct': 3
                    },
                    {
                        'question': "What is the correct syntax to output 'Hello World' in C++?",
                        'options': ["cout << 'Hello World';", "System.out.println('Hello World');", 
                                   "print('Hello World')", "printf('Hello World');"],
                        'correct': 0
                    },
                    {
                        'question': "Which header file is needed for input/output in C++?",
                        'options': ["<stdio.h>", "<iostream>", "<input.h>", "<output.h>"],
                        'correct': 1
                    },
                    {
                        'question': "What is the size of 'int' in C++ (typically)?",
                        'options': ["2 bytes", "4 bytes", "8 bytes", "Depends on system"],
                        'correct': 3
                    }
                ],
                'medium': [
                    {
                        'question': "What is a pointer in C++?",
                        'options': ["A variable that stores memory address", "A function", "A data type", "An operator"],
                        'correct': 0
                    },
                    {
                        'question': "What is the difference between struct and class in C++?",
                        'options': ["No difference", "Default access: struct is public, class is private", 
                                   "Struct can't have methods", "Class is faster"],
                        'correct': 1
                    },
                    {
                        'question': "What is constructor overloading in C++?",
                        'options': ["Having multiple constructors with different parameters", "Having too many constructors", 
                                   "Overriding parent constructor", "Creating constructor functions"],
                        'correct': 0
                    },
                    {
                        'question': "What is the purpose of 'const' keyword in C++?",
                        'options': ["To create constants only", "To prevent modification of variables, parameters, or return values", 
                                   "To speed up code", "To define constructors"],
                        'correct': 1
                    }
                ],
                'hard': [
                    {
                        'question': "What is virtual function in C++?",
                        'options': ["A function without body", "Function for runtime polymorphism", 
                                   "A static function", "An inline function"],
                        'correct': 1
                    },
                    {
                        'question': "What is RAII in C++?",
                        'options': ["A design pattern", "Resource Acquisition Is Initialization", 
                                   "A memory leak", "A compiler optimization"],
                        'correct': 1
                    },
                    {
                        'question': "What is the difference between new/delete and malloc/free?",
                        'options': ["No difference", "new/delete call constructors/destructors, malloc/free don't", 
                                   "malloc is faster", "new is deprecated"],
                        'correct': 1
                    },
                    {
                        'question': "What are smart pointers in C++?",
                        'options': ["Faster pointers", "Objects that manage memory automatically", 
                                   "Intelligent algorithms", "Pointer arithmetic"],
                        'correct': 1
                    }
                ]
            },
            'javascript': {
                'easy': [
                    {
                        'question': "What is the correct way to declare a variable in JavaScript?",
                        'options': ["var x = 5;", "variable x = 5;", "int x = 5;", "x := 5;"],
                        'correct': 0
                    },
                    {
                        'question': "How do you write a comment in JavaScript?",
                        'options': ["# This is a comment", "// This is a comment", 
                                   "<!-- This is a comment -->", "/* This is a comment"],
                        'correct': 1
                    },
                    {
                        'question': "What is the correct syntax for a function in JavaScript?",
                        'options': ["function myFunc()", "def myFunc()", "func myFunc()", "function:myFunc()"],
                        'correct': 0
                    },
                    {
                        'question': "How do you create an array in JavaScript?",
                        'options': ["var arr = []", "var arr = {}", "var arr = ()", "array arr = []"],
                        'correct': 0
                    }
                ],
                'medium': [
                    {
                        'question': "In JavaScript, what does 'this' keyword refer to?",
                        'options': ["The global object", "The current object", "Depends on context", "The parent object"],
                        'correct': 2
                    },
                    {
                        'question': "What is the difference between '==' and '===' in JavaScript?",
                        'options': ["No difference", "=== checks type and value", "== is faster", "=== is deprecated"],
                        'correct': 1
                    },
                    {
                        'question': "What is callback function in JavaScript?",
                        'options': ["A function that calls back", "A function passed as an argument to another function", 
                                   "A recursive function", "A return function"],
                        'correct': 1
                    },
                    {
                        'question': "What is the purpose of 'use strict' in JavaScript?",
                        'options': ["To make code faster", "To enable strict mode for better error checking", 
                                   "To use strict types", "To enable strict compilation"],
                        'correct': 1
                    }
                ],
                'hard': [
                    {
                        'question': "What is a closure in JavaScript?",
                        'options': ["A loop terminator", "Function with access to outer scope", 
                                   "A class method", "An event handler"],
                        'correct': 1
                    },
                    {
                        'question': "What is event delegation in JavaScript?",
                        'options': ["Assigning events to child elements", "Using parent element to handle child events", 
                                   "Removing events", "Creating custom events"],
                        'correct': 1
                    },
                    {
                        'question': "What is the event loop in JavaScript?",
                        'options': ["A for loop", "Mechanism handling asynchronous callbacks", 
                                   "An infinite loop", "A design pattern"],
                        'correct': 1
                    },
                    {
                        'question': "What are Promises in JavaScript?",
                        'options': ["Guaranteed outcomes", "Objects representing eventual completion/failure of async operations", 
                                   "Error handlers", "Loop structures"],
                        'correct': 1
                    }
                ]
            },
            'html': {
                'easy': [
                    {
                        'question': "What does HTML stand for?",
                        'options': ["Hyper Text Markup Language", "High Tech Modern Language", 
                                   "Home Tool Markup Language", "Hyperlinks and Text Markup Language"],
                        'correct': 0
                    },
                    {
                        'question': "Which HTML tag is used to define an internal style sheet?",
                        'options': ["<css>", "<script>", "<style>", "<link>"],
                        'correct': 2
                    },
                    {
                        'question': "Which tag is used to create a hyperlink?",
                        'options': ["<link>", "<a>", "<href>", "<hyperlink>"],
                        'correct': 1
                    },
                    {
                        'question': "What is the correct HTML for creating a heading?",
                        'options': ["<heading>", "<h1>", "<head>", "<header>"],
                        'correct': 1
                    }
                ],
                'medium': [
                    {
                        'question': "What is the purpose of the <meta> tag?",
                        'options': ["To create metadata", "To provide metadata about the HTML document", 
                                   "To create menus", "To define methods"],
                        'correct': 1
                    },
                    {
                        'question': "What is the difference between <div> and <span>?",
                        'options': ["No difference", "div is block-level, span is inline", 
                                   "span is newer", "div is deprecated"],
                        'correct': 1
                    },
                    {
                        'question': "What is semantic HTML?",
                        'options': ["Fancy HTML", "HTML that provides meaning to the content", 
                                   "HTML with semantics", "Deprecated HTML"],
                        'correct': 1
                    },
                    {
                        'question': "What is the purpose of the 'alt' attribute in <img>?",
                        'options': ["Alternative styling", "Alternative text for screen readers and if image fails", 
                                   "Altitude of image", "Alternate image"],
                        'correct': 1
                    }
                ],
                'hard': [
                    {
                        'question': "What is the HTML5 data- attribute used for?",
                        'options': ["Database connections", "Storing custom data in HTML elements", 
                                   "Data validation", "Data transfer"],
                        'correct': 1
                    },
                    {
                        'question': "What is the purpose of <picture> element in HTML5?",
                        'options': ["To display pictures", "To provide responsive images with multiple sources", 
                                   "To create picture galleries", "To edit pictures"],
                        'correct': 1
                    },
                    {
                        'question': "What is the difference between localStorage and sessionStorage?",
                        'options': ["No difference", "localStorage persists, sessionStorage clears on tab close", 
                                   "sessionStorage is faster", "localStorage is deprecated"],
                        'correct': 1
                    },
                    {
                        'question': "What is ARIA in HTML?",
                        'options': ["A new HTML version", "Accessible Rich Internet Applications - improves accessibility", 
                                   "A styling framework", "A JavaScript library"],
                        'correct': 1
                    }
                ]
            },
            'css': {
                'easy': [
                    {
                        'question': "What does CSS stand for?",
                        'options': ["Computer Style Sheets", "Cascading Style Sheets", 
                                   "Creative Style Sheets", "Colorful Style Sheets"],
                        'correct': 1
                    },
                    {
                        'question': "Which CSS property is used to change text color?",
                        'options': ["text-color", "color", "font-color", "text-style"],
                        'correct': 1
                    },
                    {
                        'question': "How do you add a background color in CSS?",
                        'options': ["background-color:", "bgcolor:", "color:", "bg-color:"],
                        'correct': 0
                    },
                    {
                        'question': "Which property is used to change font size?",
                        'options': ["text-size", "font-style", "font-size", "text-style"],
                        'correct': 2
                    }
                ],
                'medium': [
                    {
                        'question': "What is the Box Model in CSS?",
                        'options': ["A layout technique", "Content, padding, border, margin", 
                                   "A framework", "A grid system"],
                        'correct': 1
                    },
                    {
                        'question': "What is the difference between padding and margin?",
                        'options': ["No difference", "Padding is inside border, margin is outside", 
                                   "Margin is inside", "Padding is deprecated"],
                        'correct': 1
                    },
                    {
                        'question': "What is Flexbox in CSS?",
                        'options': ["A flexible box", "A layout model for arranging items in rows or columns", 
                                   "A framework", "A grid system"],
                        'correct': 1
                    },
                    {
                        'question': "What does 'position: relative' do?",
                        'options': ["Positions relative to nothing", "Positions relative to normal position", 
                                   "Positions relative to parent", "Positions relative to viewport"],
                        'correct': 1
                    }
                ],
                'hard': [
                    {
                        'question': "What is specificity in CSS?",
                        'options': ["Browser compatibility", "Weight of selectors determining which styles apply", 
                                   "Animation timing", "Responsive design"],
                        'correct': 1
                    },
                    {
                        'question': "What is the difference between CSS Grid and Flexbox?",
                        'options': ["No difference", "Grid is 2D, Flexbox is 1D", 
                                   "Flexbox is newer", "Grid is deprecated"],
                        'correct': 1
                    },
                    {
                        'question': "What are CSS custom properties (variables)?",
                        'options': ["Custom CSS", "Reusable values defined with -- prefix", 
                                   "Custom styles", "Variable fonts"],
                        'correct': 1
                    },
                    {
                        'question': "What is the 'will-change' property used for?",
                        'options': ["To change styles", "To hint browser about upcoming changes for optimization", 
                                   "To create animations", "To change layouts"],
                        'correct': 1
                    }
                ]
            },
            'c': {
                'easy': [
                    {
                        'question': "What is the correct syntax to output text in C?",
                        'options': ["printf()", "cout", "print()", "echo()"],
                        'correct': 0
                    },
                    {
                        'question': "Which symbol is used to terminate statements in C?",
                        'options': [".", ";", ":", ","],
                        'correct': 1
                    },
                    {
                        'question': "What is the entry point of a C program?",
                        'options': ["start()", "main()", "begin()", "run()"],
                        'correct': 1
                    },
                    {
                        'question': "How do you declare an integer variable in C?",
                        'options': ["int x;", "integer x;", "var x;", "number x;"],
                        'correct': 0
                    }
                ],
                'medium': [
                    {
                        'question': "What is the difference between ++i and i++?",
                        'options': ["No difference", "++i increments before use, i++ increments after", 
                                   "i++ is faster", "++i is deprecated"],
                        'correct': 1
                    },
                    {
                        'question': "What is a pointer in C?",
                        'options': ["A pointing device", "A variable storing memory address", 
                                   "A function", "An operator"],
                        'correct': 1
                    },
                    {
                        'question': "What does malloc() do in C?",
                        'options': ["Makes a location", "Allocates memory dynamically", 
                                   "Creates arrays", "Multiplies numbers"],
                        'correct': 1
                    },
                    {
                        'question': "What is the purpose of the 'static' keyword in C?",
                        'options': ["To make variables constant", "To preserve variable value between function calls and limit scope", 
                                   "To create static arrays", "To speed up code"],
                        'correct': 1
                    }
                ],
                'hard': [
                    {
                        'question': "What is the difference between stack and heap memory in C?",
                        'options': ["No difference", "Stack is automatic and faster, heap is manual and larger", 
                                   "Heap is faster", "Stack is manual"],
                        'correct': 1
                    },
                    {
                        'question': "What is a dangling pointer in C?",
                        'options': ["A null pointer", "A pointer pointing to freed/deleted memory", 
                                   "A hanging pointer", "An uninitialized pointer"],
                        'correct': 1
                    },
                    {
                        'question': "What is the purpose of 'volatile' keyword in C?",
                        'options': ["To make variables constant", "To prevent compiler optimization of variable", 
                                   "To speed up access", "To create volatile memory"],
                        'correct': 1
                    },
                    {
                        'question': "What is memory alignment in C?",
                        'options': ["Aligning memory cards", "Arranging data in memory according to natural boundaries", 
                                   "Memory organization", "Memory sorting"],
                        'correct': 1
                    }
                ]
            }
        }
        
        self.time_per_difficulty = {
            'easy': 30,
            'medium': 45,
            'hard': 60
        }
        
        self.show_main_menu()
    
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None
    
    def show_main_menu(self):
        self.clear_window()
        
        main_frame = tk.Frame(self.root, bg="#6366f1")
        main_frame.pack(expand=True, fill='both', padx=50, pady=50)
        
        title_label = tk.Label(main_frame, text="🧠 AI Quiz Master", 
                              font=("Arial", 36, "bold"), bg="#6366f1", fg="white")
        title_label.pack(pady=(0, 10))
        
        subtitle_label = tk.Label(main_frame, text="Test Your Programming Knowledge", 
                                 font=("Arial", 16), bg="#6366f1", fg="#e0e7ff")
        subtitle_label.pack(pady=(0, 40))
        
        buttons_frame = tk.Frame(main_frame, bg="#6366f1")
        buttons_frame.pack()
        
        standard_btn = tk.Button(buttons_frame, text="✨ Standard Quiz by Language\n\nChoose specific programming language\nC, C++, Python, Java, HTML, CSS, JS",
                                font=("Arial", 13, "bold"), bg="white", fg="#6366f1",
                                width=32, height=6, relief="flat", cursor="hand2",
                                command=self.show_language_selection)
        standard_btn.grid(row=0, column=0, padx=15, pady=15)
        
        custom_btn = tk.Button(buttons_frame, text="📚 Custom Quiz\n\nAdd your notes and get\nAI-generated questions",
                              font=("Arial", 13, "bold"), bg="white", fg="#ec4899",
                              width=32, height=6, relief="flat", cursor="hand2",
                              command=self.show_notes_input)
        custom_btn.grid(row=0, column=1, padx=15, pady=15)
    
    def show_language_selection(self):
        self.clear_window()
        
        main_frame = tk.Frame(self.root, bg="#6366f1")
        main_frame.pack(expand=True, fill='both', padx=40, pady=40)
        
        title_label = tk.Label(main_frame, text="Choose Programming Language", 
                              font=("Arial", 28, "bold"), bg="#6366f1", fg="white")
        title_label.pack(pady=(0, 30))
        
        languages = [
            ('Python', '🐍', '#3776ab', 'python'),
            ('Java', '☕', '#f89820', 'java'),
            ('C++', '⚙', '#00599c', 'cpp'),
            ('JavaScript', '⚡', '#f7df1e', 'javascript'),
            ('HTML', '🌐', '#e34c26', 'html'),
            ('CSS', '🎨', '#264de4', 'css'),
            ('C', '📋', '#a8b9cc', 'c')
        ]
        
        buttons_frame = tk.Frame(main_frame, bg="#6366f1")
        buttons_frame.pack(pady=20)
        
        for idx, (name, emoji, color, lang_key) in enumerate(languages):
            row = idx // 3
            col = idx % 3
            
            btn = tk.Button(buttons_frame, text=f"{emoji}\n{name}", 
                           font=("Arial", 16, "bold"), bg="white", fg=color,
                           width=15, height=4, relief="flat", cursor="hand2",
                           command=lambda lk=lang_key, ln=name: self.select_language(lk, ln))
            btn.grid(row=row, column=col, padx=10, pady=10)
        
        back_btn = tk.Button(main_frame, text="← Back to Menu", font=("Arial", 12, "bold"),
                            bg="white", fg="#6366f1", width=18, height=2,
                            relief="flat", cursor="hand2", command=self.show_main_menu)
        back_btn.pack(pady=(20, 0))
    
    def select_language(self, lang_key, lang_name):
        self.selected_language = lang_key
        self.language_display_name = lang_name
        self.mode = 'language'
        self.select_difficulty()
    
    def show_notes_input(self):
        self.clear_window()
        
        main_frame = tk.Frame(self.root, bg="#ec4899")
        main_frame.pack(expand=True, fill='both', padx=50, pady=50)
        
        title_label = tk.Label(main_frame, text="📚 Add Your Study Notes", 
                              font=("Arial", 24, "bold"), bg="#ec4899", fg="white")
        title_label.pack(pady=(0, 20))
        
        text_frame = tk.Frame(main_frame, bg="white")
        text_frame.pack(fill='both', expand=True, pady=(0, 20))
        
        self.notes_text = scrolledtext.ScrolledText(text_frame, font=("Arial", 12), 
                                                    wrap=tk.WORD, height=15)
        self.notes_text.pack(fill='both', expand=True, padx=5, pady=5)
        self.notes_text.insert('1.0', "Paste your notes here... The AI will generate questions based on your content!")
        
        btn_frame = tk.Frame(main_frame, bg="#ec4899")
        btn_frame.pack()
        
        back_btn = tk.Button(btn_frame, text="← Back", font=("Arial", 12, "bold"),
                            bg="#f3f4f6", fg="#374151", width=15, height=2,
                            relief="flat", cursor="hand2", command=self.show_main_menu)
        back_btn.grid(row=0, column=0, padx=10)
        
        continue_btn = tk.Button(btn_frame, text="Continue →", font=("Arial", 12, "bold"),
                                bg="white", fg="#ec4899", width=15, height=2,
                                relief="flat", cursor="hand2", 
                                command=self.save_notes_and_continue)
        continue_btn.grid(row=0, column=1, padx=10)
    
    def save_notes_and_continue(self):
        self.notes = self.notes_text.get('1.0', 'end-1c').strip()
        if not self.notes or self.notes == "Paste your notes here... The AI will generate questions based on your content!":
            messagebox.showwarning("No Notes", "Please add some notes first!")
            return
        self.mode = 'notes'
        self.select_difficulty()
    
    def select_difficulty(self):
        self.clear_window()
        
        main_frame = tk.Frame(self.root, bg="#6366f1")
        main_frame.pack(expand=True, fill='both', padx=50, pady=50)
        
        title_text = f"Choose Difficulty - {self.language_display_name}" if self.mode == 'language' else "Choose Your Difficulty"
        title_label = tk.Label(main_frame, text=title_text, 
                              font=("Arial", 28, "bold"), bg="#6366f1", fg="white")
        title_label.pack(pady=(0, 40))
        
        buttons_frame = tk.Frame(main_frame, bg="#6366f1")
        buttons_frame.pack()
        
        easy_btn = tk.Button(buttons_frame, text="🎯 Easy\n\nBasic concepts\n30s per question",
                            font=("Arial", 13, "bold"), bg="#10b981", fg="white",
                            width=20, height=6, relief="flat", cursor="hand2",
                            command=lambda: self.start_quiz('easy'))
        easy_btn.grid(row=0, column=0, padx=15)
        
        medium_btn = tk.Button(buttons_frame, text="⚡ Medium\n\nIntermediate topics\n45s per question",
                              font=("Arial", 13, "bold"), bg="#f59e0b", fg="white",
                              width=20, height=6, relief="flat", cursor="hand2",
                              command=lambda: self.start_quiz('medium'))
        medium_btn.grid(row=0, column=1, padx=15)
        
        hard_btn = tk.Button(buttons_frame, text="🏆 Hard\n\nAdvanced concepts\n60s per question",
                            font=("Arial", 13, "bold"), bg="#ef4444", fg="white",
                            width=20, height=6, relief="flat", cursor="hand2",
                            command=lambda: self.start_quiz('hard'))
        hard_btn.grid(row=0, column=2, padx=15)
        
        back_command = self.show_notes_input if self.mode == 'notes' else self.show_language_selection if self.mode == 'language' else self.show_main_menu
        back_btn = tk.Button(main_frame, text="← Back", font=("Arial", 12, "bold"),
                            bg="white", fg="#6366f1", width=15, height=2,
                            relief="flat", cursor="hand2", 
                            command=back_command)
        back_btn.pack(pady=(40, 0))
    
    def generate_questions_from_notes(self, difficulty):
        concepts = [s.strip() for s in re.split('[.;!\\n]+', self.notes) if len(s.strip()) > 20]
        generated = []
        
        templates = {
            'easy': ["According to your notes, what is mentioned about", 
                    "Your notes describe", "What concept is explained regarding"],
            'medium': ["Based on your notes, how would you explain",
                      "Your notes suggest the relationship between",
                      "According to your material, what happens when"],
            'hard': ["Analyzing your notes, what would be the consequence of",
                    "Your notes imply that the advanced concept of",
                    "Synthesizing information, how would you apply"]
        }
        
        for i, concept in enumerate(concepts[:8]):
            words = concept.split()
            key_phrase = ' '.join(words[:min(8, len(words))])
            template = templates[difficulty][i % len(templates[difficulty])]
            
            options = [
                ' '.join(words[:6]) if len(words) >= 6 else concept[:50],
                "Alternative interpretation of the concept",
                f"Different approach to {words[0] if words else 'concept'}",
                "Unrelated concept"
            ]
            random.shuffle(options)
            
            generated.append({
                'question': f'{template} "{key_phrase}..."?',
                'options': options,
                'correct': random.randint(0, 3)
            })
        
        return generated if generated else []
    
    def start_quiz(self, difficulty):
        self.difficulty = difficulty
        self.current_question = 0
        self.score = 0
        
        if self.mode == 'notes' and self.notes:
            self.questions = self.generate_questions_from_notes(difficulty)
            if not self.questions:
                messagebox.showerror("Error", "Could not generate questions from your notes. Please try again with more content.")
                self.show_notes_input()
                return
        elif self.mode == 'language' and self.selected_language:
            available_questions = self.language_questions.get(self.selected_language, {}).get(difficulty, [])
            self.questions = random.sample(available_questions, min(8, len(available_questions)))
        else:
            messagebox.showerror("Error", "Invalid quiz configuration!")
            self.show_main_menu()
            return
        
        self.time_left = self.time_per_difficulty[difficulty]
        self.show_question()
    
    def show_question(self):
        self.clear_window()
        self.selected_answer = None
        
        if self.current_question >= len(self.questions):
            self.show_results()
            return
        
        q = self.questions[self.current_question]
        
        main_frame = tk.Frame(self.root, bg="#6366f1")
        main_frame.pack(expand=True, fill='both', padx=40, pady=40)
        
        info_frame = tk.Frame(main_frame, bg="white", relief="raised", bd=2)
        info_frame.pack(fill='x', pady=(0, 20))
        
        question_label = tk.Label(info_frame, 
                                 text=f"Question {self.current_question + 1}/{len(self.questions)}", 
                                 font=("Arial", 12, "bold"), bg="#e9d5ff", fg="#7c3aed",
                                 padx=15, pady=8)
        question_label.pack(side='left', padx=5, pady=5)
        
        lang_display = self.language_display_name if self.mode == 'language' else "Your Notes"
        lang_label = tk.Label(info_frame, text=lang_display, 
                             font=("Arial", 12, "bold"), bg="#ddd6fe", fg="#5b21b6",
                             padx=15, pady=8)
        lang_label.pack(side='left', padx=5, pady=5)
        
        self.timer_label = tk.Label(info_frame, text=f"⏰ {self.time_left}s", 
                                   font=("Arial", 12, "bold"), bg="#dcfce7", fg="#16a34a",
                                   padx=15, pady=8)
        self.timer_label.pack(side='right', padx=5, pady=5)
        
        score_label = tk.Label(info_frame, text=f"🏆 Score: {self.score}/{len(self.questions)}", 
                              font=("Arial", 12, "bold"), bg="#fef3c7", fg="#d97706",
                              padx=15, pady=8)
        score_label.pack(side='right', padx=5, pady=5)
        
        progress_frame = tk.Frame(main_frame, bg="#e5e7eb", height=10, relief="sunken", bd=1)
        progress_frame.pack(fill='x', pady=(0, 20))
        
        progress = (self.current_question / len(self.questions)) * 100
        progress_bar = tk.Frame(progress_frame, bg="#a855f7", height=10)
        progress_bar.place(relwidth=progress/100, relheight=1)
        
        question_frame = tk.Frame(main_frame, bg="white", relief="raised", bd=2)
        question_frame.pack(fill='both', expand=True)
        
        q_label = tk.Label(question_frame, text=q['question'], 
                          font=("Arial", 16, "bold"), bg="white", fg="#1f2937",
                          wraplength=750, justify='left')
        q_label.pack(pady=30, padx=30)
        
        self.option_buttons = []
        option_letters = ['A', 'B', 'C', 'D']
        for i, option in enumerate(q['options']):
            btn_frame = tk.Frame(question_frame, bg="white")
            btn_frame.pack(fill='x', padx=30, pady=5)
            
            btn = tk.Button(btn_frame, text=f"{option_letters[i]}.  {option}", 
                          font=("Arial", 13), bg="#f3f4f6", fg="#1f2937", 
                          relief="flat", cursor="hand2", wraplength=700, 
                          justify='left', anchor='w', pady=15, padx=20,
                          activebackground="#e5e7eb",
                          command=lambda idx=i: self.check_answer(idx))
            btn.pack(fill='x')
            self.option_buttons.append(btn)
        
        self.start_timer()
    
    def start_timer(self):
        if self.time_left > 0:
            self.timer_label.config(text=f"⏰ {self.time_left}s")
            if self.time_left <= 10:
                self.timer_label.config(bg="#fecaca", fg="#dc2626")
            self.time_left -= 1
            self.timer_id = self.root.after(1000, self.start_timer)
        else:
            self.time_up()
    
    def time_up(self):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
        messagebox.showinfo("Time's Up!", "Time expired for this question!")
        self.next_question()
    
    def check_answer(self, selected_idx):
        if self.selected_answer is not None:
            return
        
        self.selected_answer = selected_idx
        q = self.questions[self.current_question]
        
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
        
        for i, btn in enumerate(self.option_buttons):
            btn.config(state='disabled')
            if i == q['correct']:
                btn.config(bg="#86efac", fg="#166534", font=("Arial", 13, "bold"))
            elif i == selected_idx and i != q['correct']:
                btn.config(bg="#fca5a5", fg="#991b1b", font=("Arial", 13, "bold"))
        
        if selected_idx == q['correct']:
            self.score += 1
        
        self.root.after(2000, self.next_question)
    
    def next_question(self):
        self.current_question += 1
        self.time_left = self.time_per_difficulty[self.difficulty]
        self.show_question()
    
    def show_results(self):
        self.clear_window()
        
        percentage = (self.score / len(self.questions)) * 100
        
        if percentage >= 80:
            message = "Outstanding! 🎉"
            color = "#10b981"
        elif percentage >= 60:
            message = "Great Job! 👏"
            color = "#3b82f6"
        elif percentage >= 40:
            message = "Good Effort! 💪"
            color = "#f59e0b"
        else:
            message = "Keep Practicing! 📚"
            color = "#ef4444"
        
        main_frame = tk.Frame(self.root, bg=color)
        main_frame.pack(expand=True, fill='both', padx=50, pady=50)
        
        result_frame = tk.Frame(main_frame, bg="white", relief="raised", bd=3)
        result_frame.pack(expand=True, padx=40, pady=40)
        
        trophy_label = tk.Label(result_frame, text="🏆", font=("Arial", 80), bg="white")
        trophy_label.pack(pady=(20, 10))
        
        message_label = tk.Label(result_frame, text=message, 
                                font=("Arial", 32, "bold"), bg="white", fg="#1f2937")
        message_label.pack(pady=(0, 20))
        
        score_frame = tk.Frame(result_frame, bg=color, relief="raised", bd=2)
        score_frame.pack(pady=20)
        
        score_label = tk.Label(score_frame, text=f"{self.score} / {len(self.questions)}", 
                              font=("Arial", 36, "bold"), bg=color, fg="white",
                              padx=40, pady=20)
        score_label.pack()
        
        percentage_label = tk.Label(result_frame, text=f"{percentage:.0f}%", 
                                   font=("Arial", 48, "bold"), bg="white", fg="#1f2937")
        percentage_label.pack(pady=10)
        
        accuracy_label = tk.Label(result_frame, text="Accuracy", 
                                 font=("Arial", 16), bg="white", fg="#6b7280")
        accuracy_label.pack()
        
        summary_frame = tk.Frame(result_frame, bg="#f3f4f6", relief="sunken", bd=2)
        summary_frame.pack(pady=30, padx=40, fill='x')
        
        summary_title = tk.Label(summary_frame, text="📊 Quiz Summary", 
                                font=("Arial", 16, "bold"), bg="#f3f4f6", fg="#1f2937")
        summary_title.pack(pady=(15, 10))
        
        stats_frame = tk.Frame(summary_frame, bg="#f3f4f6")
        stats_frame.pack(pady=(0, 15))
        
        correct_label = tk.Label(stats_frame, text=f"✓ {self.score}\nCorrect", 
                                font=("Arial", 16, "bold"), bg="#f3f4f6", fg="#10b981")
        correct_label.grid(row=0, column=0, padx=40)
        
        incorrect_label = tk.Label(stats_frame, text=f"✗ {len(self.questions) - self.score}\nIncorrect", 
                                  font=("Arial", 16, "bold"), bg="#f3f4f6", fg="#ef4444")
        incorrect_label.grid(row=0, column=1, padx=40)
        
        btn_frame = tk.Frame(result_frame, bg="white")
        btn_frame.pack(pady=20)
        
        new_quiz_btn = tk.Button(btn_frame, text="🏠 New Quiz", font=("Arial", 13, "bold"),
                                bg=color, fg="white", width=18, height=2,
                                relief="flat", cursor="hand2", command=self.show_main_menu)
        new_quiz_btn.grid(row=0, column=0, padx=10)
        
        retry_btn = tk.Button(btn_frame, text="🔄 Retry Same Quiz", font=("Arial", 13, "bold"),
                             bg="#f3f4f6", fg="#374151", width=18, height=2,
                             relief="flat", cursor="hand2", 
                             command=lambda: self.start_quiz(self.difficulty))
        retry_btn.grid(row=0, column=1, padx=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = ProgrammingQuizApp(root)
    root.mainloop()