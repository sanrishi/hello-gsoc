import turtle
import time
import random

# Game speed
delay = 0.1

# Score
score = 0
high_score = 0

# Screen
win = turtle.Screen()
win.title("Snake Game - Your Version 😎")
win.bgcolor("black")
win.setup(width=600, height=600)
win.tracer(0)

# Snake head
head = turtle.Turtle()
head.speed(0)
head.shape("square")
head.color("lime")
head.penup()
head.goto(0, 0)
head.direction = "stop"

# Food
food = turtle.Turtle()
food.speed(0)
food.shape("circle")
food.color("red")
food.penup()
food.goto(0, 100)

# Body segments
segments = []

# Scoreboard
scoreboard = turtle.Turtle()
scoreboard.speed(0)
scoreboard.hideturtle()
scoreboard.color("white")
scoreboard.penup()
scoreboard.goto(0, 260)
scoreboard.write("Score: 0  High Score: 0", align="center", font=("Courier", 18, "bold"))


# Movement functions
def go_up():
    if head.direction != "down":
        head.direction = "up"


def go_down():
    if head.direction != "up":
        head.direction = "down"


def go_left():
    if head.direction != "right":
        head.direction = "left"


def go_right():
    if head.direction != "left":
        head.direction = "right"


def move():
    if head.direction == "up":
        y = head.ycor()
        head.sety(y + 20)

    if head.direction == "down":
        y = head.ycor()
        head.sety(y - 20)

    if head.direction == "left":
        x = head.xcor()
        head.setx(x - 20)

    if head.direction == "right":
        x = head.xcor()
        head.setx(x + 20)


# Keyboard controls
win.listen()
win.onkeypress(go_up, "Up")
win.onkeypress(go_down, "Down")
win.onkeypress(go_left, "Left")
win.onkeypress(go_right, "Right")

# Game Loop
while True:
    win.update()

    # Border collision
    if head.xcor() > 290 or head.xcor() < -290 or head.ycor() > 290 or head.ycor() < -290:
        time.sleep(1)
        head.goto(0, 0)
        head.direction = "stop"

        # Reset body
        for segment in segments:
            segment.goto(1000, 1000)
        segments.clear()

        score = 0
        delay = 0.1
        scoreboard.clear()
        scoreboard.write(f"Score: {score}  High Score: {high_score}", align="center", font=("Courier", 18, "bold"))

    # Eat food
    if head.distance(food) < 15:
        # Move food
        food.goto(random.randint(-280, 280), random.randint(-280, 280))

        # Add segment
        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape("square")
        new_segment.color("yellow")
        new_segment.penup()
        segments.append(new_segment)

        # Increase score
        score += 10
        if score > high_score:
            high_score = score

        scoreboard.clear()
        scoreboard.write(f"Score: {score}  High Score: {high_score}", align="center", font=("Courier", 18, "bold"))
        delay -= 0.001

    # Move segments
    for index in range(len(segments) - 1, 0, -1):
        x = segments[index - 1].xcor()
        y = segments[index - 1].ycor()
        segments[index].goto(x, y)

    if len(segments) > 0:
        segments[0].goto(head.xcor(), head.ycor())

    move()

    # Body collision
    for segment in segments:
        if segment.distance(head) < 15:
            time.sleep(1)
            head.goto(0, 0)
            head.direction = "stop"

            for segment in segments:
                segment.goto(1000, 1000)
            segments.clear()

            score = 0
            delay = 0.1
            scoreboard.clear()
            scoreboard.write(f"Score: {score}  High Score: {high_score}", align="center", font=("Courier", 18, "bold"))

    time.sleep(delay)

win.mainloop()
