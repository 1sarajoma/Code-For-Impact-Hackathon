#Name of Code: ALL ABOUT SCAM CALL CENTERS
#Purpose: Teach people about the dangers of Scam Call centers and how to avoid them

import tkinter as tk
from tkinter import RIGHT, messagebox
from tkinter import ttk
from ttkbootstrap import Style
from information_quiz import questions, answers, choices
import turtle
from tkinter import PhotoImage

# Global variables to track quiz state
score_value = 0  # The current score of the quiz
current_q_index = 0  # The index of the current question
question_status = ["unanswered"] * len(questions)  # List to track the status of each question

# Functions for the quiz application

# Function to terminate the main Tkinter application
def terminate_application():
    top_window.quit()

# This function exists to reset the quiz 
def reset_quiz():
    global score_value, current_q_index, question_status
    score_value = 0  # Initializes score variable back to zero
    current_q_index = 0  # Initializes the current question index back to zero so the questions are displayed from the beginning of the list
    question_status = ["unanswered"] * len(questions)  # For the labels at the top, it resets all the statuses to unanswered
    score_display.config(text=f"Score: {score_value}")  # Sets the score display back to zero
    progress_bar['value'] = 0  # Sets the progress bar with the corresponding value
    present_question()  # Starts first question
    update_status_indicator()  # Updates any indicators if questions are done right or wrong

# This function updates the display once you answer a question and then presents the next question 
def present_question():
    question_label.config(text=questions[current_q_index])  # This displays the next question
    for i, button in enumerate(answer_buttons):  # enumerate provides a counter (i) and the value from the button
        # i is used for the index and button is the button widget from the answer_button function
        # enables or disables the question depending on if it has been answered
        button.config(text=choices[current_q_index][i], state="normal" if question_status[current_q_index] == "unanswered" else "disabled")  # disables buttons if answered and keeps them enabled if not
    feedback_label.config(text="")  # Clear feedback label

    progress_bar['value'] = (current_q_index + 1) / len(questions) * 100  # Updates the progress bar based off which question

# Function to validate the selected answer and update the score and status
def validate_answer(choice):
    global score_value
    correct_answer = answers[current_q_index]  # From the current index loop, it gets the correct answer
    selected_answer = answer_buttons[choice].cget("text")  # Gets the selected answer from the button

    if selected_answer == correct_answer:
        score_value += 1  # Adds 1 to score variable if choice matches up with the correct answer
        feedback_label.config(text="Correct!", foreground="green")  # Tell the user that they got it right
        question_status[current_q_index] = "correct"  # changes the status of the question to correct 
    else:
        feedback_label.config(text=f"Incorrect! The correct answer is: {correct_answer}", foreground="red")  # Tells the user they got it wrong and then the correct answer
        question_status[current_q_index] = "wrong"  # sets the question status to wrong

    for button in answer_buttons:
        button.config(state="disabled")  # Once answer is chosen question is fully disabled and user is unable to pick another choice

    score_display.config(text=f"Score: {score_value}")  # This updates the score display
    update_status_indicator()  # This updates the indicator which represents the status of the question by calling the function

# This function checks if there is a next question and if there is it presents the next question and if not ends the quiz
def proceed_next_question():
    global current_q_index
    if current_q_index < len(questions) - 1:
        current_q_index += 1  # Sets the question index to one higher so that it can move on to the next question
        present_question()  # Sets up the next question by calling the function
    else:
        # if there are no more questions will display the final score through a messagebox 
        messagebox.showinfo("Quiz Completed", f"Quiz Completed! Final score: {score_value}")
        quiz_toplevel.destroy()  # Destroys the window once the quiz is completed

# This function allows the user to go back to the previous question
def proceed_previous_question():
    global current_q_index
    if current_q_index > 0:
        current_q_index -= 1  # Respectively sets the question index to one lower so that it can move back to the previous question
        present_question()  # then calls the function to present the question

# Function to update the status indicator for each question
def update_status_indicator():
    for i, label in enumerate(status_labels):  # enumerate provides a counter and the value from the label, i the value is the index, and label is the widget from status labels

        if question_status[i] == "correct":
            label.config(text="✓", foreground="green")  # Displays a check mark for correct answers
        elif question_status[i] == "wrong":
            label.config(text="✗", foreground="red")  # Displays a cross mark for wrong answers
        else:
            label.config(text="?", foreground="grey")  # Displays a question mark for unanswered questions

# Function to create the quiz top level and use all the different functions from before
def launch_quiz_window():
    global quiz_toplevel, question_label, feedback_label, answer_buttons, progress_bar, score_display, status_labels

    quiz_toplevel = tk.Toplevel()  # Create a new top level window
    quiz_toplevel.title("Time To Test Your Knowledge")  # Sets the window title for the quiz
    quiz_toplevel.geometry("600x500")  # Sets the size of the screen

    # Creates the status frame to hold the value of whether the questions are answered or not
    status_frame = ttk.Frame(quiz_toplevel)
    status_frame.pack(pady=10)

    # Creates status labels for whether if each question is either, Correct, Wrong or Unanswered
    status_labels = [ttk.Label(status_frame, text="?", width=2, anchor="center", style="Status.TLabel") for _ in range(len(questions))]
    for label in status_labels:
        label.pack(side="left", padx=5)

    # This creates the label that displays the question
    question_label = ttk.Label(quiz_toplevel, anchor="center", wraplength=500, padding=10, style="Question.TLabel")
    question_label.pack(pady=10)

    # Creates the progress bar 
    progress_bar = ttk.Progressbar(quiz_toplevel, orient="horizontal", length=400, mode="determinate")
    progress_bar.pack(pady=10)

    # This creates a separate frame within the top level to pack the buttons onto to organize them a bit
    button_frame = ttk.Frame(quiz_toplevel)
    button_frame.pack(pady=10)

    # Create the 4 buttons that will represent the options the user has to choose from
    answer_buttons = [ttk.Button(button_frame, command=lambda i=i: validate_answer(i), style="Custom.TButton") for i in range(4)]
    for i, button in enumerate(answer_buttons):
        # `lambda i=i:` This creates an anonymous function that calls the validate answer function with the given index the question is at
        button.grid(row=i//2, column=i%2, padx=10, pady=10, sticky="ew")

    # This creates a label that displays the current score the user has
    score_display = ttk.Label(quiz_toplevel, text=f"Score: {score_value}", anchor="center", padding=10, style="Score.TLabel")
    score_display.pack(pady=10)

    # Creates the feedback label that displays whether the user got the question right or wrong
    feedback_label = ttk.Label(quiz_toplevel, anchor="center", padding=10, style="Feedback.TLabel")
    feedback_label.pack(pady=10)

    # Creates the button to go to the previous question calling the previous_question funciton
    prev_question_button = ttk.Button(quiz_toplevel, text="Previous", command=proceed_previous_question, style="Nav.TButton")
    prev_question_button.pack(side="left", padx=20, ipadx=20, ipady=10)

    # Creates the button to go to the next question calling the next_question funciton
    next_question_button = ttk.Button(quiz_toplevel, text="Next", command=proceed_next_question, style="Nav.TButton")
    next_question_button.pack(side="right", padx=20, ipadx=20, ipady=10)

    reset_quiz()  # Starts the generation of the quiz


# All the functions from here onward are for my turtle graphics window


# This function creats the top level for the turtle
def launch_turtle_window():
    turtle_window = tk.Toplevel()  # Creates the top level window
    turtle_window.title("Draw Your Own Scam Call Center")  # Sets the title of the turtle graphic window
    turtle_window.geometry("800x600")  # Sets the size of the window

    canvas = tk.Canvas(turtle_window, width=500, height=300)  # Creates a canvas
    canvas.pack()

    screen = turtle.TurtleScreen(canvas)  # Create a specfic turtle canvas to allow turtle to draw on it
    screen.bgcolor("skyblue")  # Sets the background color of the turtle canvas to skyblue

    t = turtle.RawTurtle(screen)  # Creates the turtle
    t.shape("turtle")  # Sets the shape of the turtle
    t.speed(1)  # Sets how fast the furtle draws

    # This function simply creates a circle to help make the backdrop of the turtle canvas
    def draw_circle(fill_color, pen_color, cir_size, x, y): 
        t.penup()
        t.setpos(x, y)
        t.pendown()
        t.speed(0)
        t.width(30)
        t.begin_fill()
        t.fillcolor(fill_color)
        t.pencolor(pen_color)
        t.circle(cir_size)
        t.end_fill()
        t.penup()

    # this function creates the clouds for the backdrop
    def draw_circle_cloud(fill_color, pen_color, cir_size, positions): 
        for pos in positions:
            t.penup()
            t.setpos(pos)
            t.pendown()
            t.speed(0)
            t.width(30)
            t.begin_fill()
            t.fillcolor(fill_color)
            t.pencolor(pen_color)
            t.circle(cir_size)
            t.end_fill()

    draw_circle("Yellow", "Yellow", 25, 150, 50)  # Draws a yellow circle which is the sun
    cloud_positions = [(-200, 50), (-165, 75), (-150, 35), (-120, 50)]  # A list holding information regarding the point where the cloud should be made
    draw_circle_cloud("white", "white", 15, cloud_positions)  # Creates the clouds

    t.penup()
    t.setpos(0,0)

    # Allows the turtle to move forward and draw a line
    def forward():
        t.pendown()
        t.forward(25)
        t.penup()

    # This turns the turtle 15 degrees to the left
    def left():
        t.left(15)

    # This turns the turtle 15 degrees to the right
    def right():
        t.right(15)

    # Moves the turtle forward without drawing
    def forward_nodraw():
        t.forward(25)

    # changes the color of the turtle then changes the focus back to the canvas
    def change_color(color):
        t.color(color)
        canvas.focus_set()

    # Adjusts the thickness the turtle creates lines at
    def change_thickness(thickness):
        t.width(thickness)
        canvas.focus_set()

    # Uses on key commands and attaches functions to respective keys to move the turtle
    screen.listen()
    screen.onkey(forward, "Up")  # Bind the Up arrow key to move the turtle forward
    screen.onkey(left, "Left")  # Bind the Left arrow key to turn the turtle left
    screen.onkey(right, "Right")  # Bind the Right arrow key to turn the turtle right
    screen.onkey(forward_nodraw, "Down")  # Bind the Down arrow key to move the turtle forward without drawing

    # Turtle control frame for color change buttons and thickness slider
    turtle_controls = ttk.Frame(turtle_window)
    turtle_controls.pack(pady=10)

    # Create buttons to change the turtle's color
    colors = ["Red", "Green", "Blue", "Black", "Yellow"]
    for i, color in enumerate(colors):     # The lambda creates an anonymous function that calls `change_color`with the current value of color When a button is pressed, it will call the change_color function and associate the correct color associated with that button.
        color_button = ttk.Button(turtle_controls, text=color, command=lambda c=color: change_color(c))
        color_button.grid(row=0, column=i, padx=5, pady=10)

    # Creates the label that tells you that the slider adjusts the pens thickness
    thickness_label = ttk.Label(turtle_controls, text="Pen Thickness:")
    thickness_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")

    #creates a scale then attaches it to the turtle window
    thickness_slider = ttk.Scale(turtle_controls, from_=1, to=20, orient="horizontal", command=lambda v: change_thickness(int(float(v))))
    thickness_slider.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
    thickness_slider.set(1)  # Set the initial thickness to 1

    # Creates a text box and a list to store and display the instructions
    instructions = (
        "In order to draw follow this guide:\n"
        "The Up Arrow: This moves forward the turtle and draws\n"
        "Down Arrow: This moves forward without drawing\n"
        "Left Arrow: Turns Left 15 Degrees\n"
        "Right Arrow: Turns Right 15 Degrees\n"
        "The color buttons change the color of the turtle\n"
        "The slider adjusts the pen thickness"
    )
    instructions_text = tk.Text(turtle_window, height=10, wrap="word")
    instructions_text.insert("1.0", instructions)
    instructions_text.config(state="disabled")
    instructions_text.pack(pady=10)

#This creates the main tkinter window
top_window = tk.Tk()
top_window.title("All About Scam Centers")  # Sets the title of the main window
top_window.geometry("400x400")  # Sets the window size

# creates a TTKbootstrap style to apply to the quiz and main window
main_style = Style(theme='darkly')
quiz_style = Style(theme='darkly')

# Configure unique styles for different buttons
main_style.configure("Start.TButton", font=("Times New Roman", 16, "bold"), foreground="white", background="black", padding=10)
main_style.configure("Quit.TButton", font=("Times New Roman", 16, "bold"), foreground="white", background="red", padding=10)
quiz_style.configure("TLabel", font=("Times New Roman", 18))
quiz_style.configure("TButton", font=("Times New Roman", 14))
quiz_style.configure("Custom.TButton", font=("Times New Roman", 14, "bold"), foreground="lightgrey", padding=5)
quiz_style.configure("Score.TLabel", font=("Times New Roman", 16, "bold"), borderwidth=2, relief="groove", background="lightgrey")
quiz_style.configure("Question.TLabel", font=("Times New Roman", 16, "bold"), foreground="lightgrey")
quiz_style.configure("Feedback.TLabel", font=("Times New Roman", 16, "italic"), foreground="lightgrey")
quiz_style.configure("Nav.TButton", font=("Times New Roman", 14, "bold"), foreground="lightgrey", background="green")
quiz_style.configure("Status.TLabel", font=("Times New Roman", 14, "bold"), borderwidth=2, relief="groove", background="lightgrey")

# Create a canvas so that a scrollbar can be used
main_canvas = tk.Canvas(top_window)
main_scrollbar = ttk.Scrollbar(top_window, orient="vertical", command=main_canvas.yview)
main_scrollable_frame = ttk.Frame(main_canvas)

# Sets up the scroll bar to be used
main_scrollable_frame.bind(
    "<Configure>",
    # `lambda e:` is a function triggered on the "Configure" event, which occurs when the widget is resized or moved.
    lambda e: main_canvas.configure(
        # Updates the scrollable region to include all items on the canvas.
        scrollregion=main_canvas.bbox("all")
    )
)


# Physically attaching the scrollbar to the Canvas
main_canvas.create_window((0, 0), window=main_scrollable_frame, anchor="nw")
main_canvas.configure(yscrollcommand=main_scrollbar.set)

# Packing the scrollbar onto the right side of the canvas
main_canvas.pack(side="left", fill="both", expand=True)
main_scrollbar.pack(side="right", fill="y")

# Putting all Main widgets onto the scrollable frame/canvas
main_title = ttk.Label(main_scrollable_frame, text="All About Scam Centers", font=("Times New Roman", 24, "bold"))
main_title.pack(pady=20)

# Function to add images with separators and text boxes to the main canvas
def add_image_with_separator(image_path, subsample, parent_frame, text):
    frame = ttk.Frame(parent_frame)
    frame.pack(fill="x", pady=25, padx=5)

    image = PhotoImage(file=image_path)
    image = image.subsample(subsample)  # Resize the image
    image_label = tk.Label(frame, image=image)
    image_label.image = image  # Keep a reference to prevent garbage collection
    image_label.pack(side="left", padx=5)

    text_box = tk.Text(frame, width=30, height=10, bg="lightgrey")
    text_box.insert("1.0", text)
    text_box.config(state="disabled")
    text_box.pack(side="right", padx=5)

    sep = ttk.Separator(parent_frame, orient="horizontal")
    sep.pack(fill="x", pady=10, padx=10)

# This adds the images, text box and separators into the main scrollable frame
add_image_with_separator("Scampic1.png", 4, main_scrollable_frame, "Often times Scam call centers employ a wide variety of different methods to reach your money. Most commonly\nthough, they call you acting as a fake\ntech support representative for a large\ncompany such as Microsoft, Google,\nApple and the list goes on")
add_image_with_separator("Scampic2.png", 16, main_scrollable_frame, "Many cities in India are known for their active population of Scam call\ncenters. One of the most well known\nbeing for this notorious activity.\nNumerous news reports often detail the large scam call center busts they do\nand how many people they arrest. \nThese call centers are making hundreds of thousands of dollars a year all\nthrough stealing your hard earned cash.")
add_image_with_separator("Scampic3.png", 4, main_scrollable_frame, "Scam call centers often target elderly\npeople due to their lack of knowledge when it comes to computers.")
add_image_with_separator("Scampic4.png", 3, main_scrollable_frame, "Often times Scammers will pretend to be a tech support\nrepersentitive to get your money")
add_image_with_separator("Scampic5.png", 3, main_scrollable_frame, "If you get a scam phone call, make\nsure to ignore it!")
add_image_with_separator("Scampic6.png", 2, main_scrollable_frame, "Scam call centers often get their phone\nnumbers through a variety of means.\nThough most commonly they purchase them from people who sell your\ndata online. Make sure to not go on anyuntrustworthy websites and\ninput your information.")
add_image_with_separator("Scampic7.png", 1, main_scrollable_frame, "The main goal of these centers\nis to steal your money.")
add_image_with_separator("Scampic8.png", 4, main_scrollable_frame, "India has a specfic governing\nbody to fight against these scammers\ncalled CERT-in. It was \nspecfically developed to fight against\ncybercrime such as scam call centers.")
add_image_with_separator("Scampic9.png", 2, main_scrollable_frame, "Scam call centers will always aim to get\nyour bank account details. Be careful!")
add_image_with_separator("Scampic10.png", 5, main_scrollable_frame, "One of the best ways to avoid\nbeing a victim of a scam call center\nis to download apps that block\nspam phone calls.")

# Attaching buttons to give access to the quiz, turtle graphics, and exit windows
start_quiz_button = ttk.Button(main_scrollable_frame, text="Start Quiz", command=launch_quiz_window, style="Start.TButton")
start_quiz_button.pack(side="left", padx=20)

turtle_button = ttk.Button(main_scrollable_frame, text="Turtle Graphics", command=launch_turtle_window, style="Start.TButton")
turtle_button.pack(side="left", padx=20)

quit_app_button = ttk.Button(main_scrollable_frame, text="Quit", command=terminate_application, style="Quit.TButton")
quit_app_button.pack(side="left", padx=20)

# Start the Tkinter main loop
top_window.mainloop()