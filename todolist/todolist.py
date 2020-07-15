# Write your code here
from datetime import datetime, timedelta

from sqlalchemy import Column, Integer, String, Date
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///todo.db?check_same_thread=False')

Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


# first_row = rows[0]  # In case rows list is not empty

# print(first_row.string_field)  # Will print value of the string_field
# print(first_row.id)  # Will print the id of the row.
# print(first_row)  # Will print the string that was returned by __repr__ method


def print_todays_tasks():
    print("Today " + datetime.today().strftime("%d %b:"))
    rows = session.query(Table).filter(Table.deadline == datetime.today().date()).all()
    if len(rows) == 0:
        print("Nothing to do!")
    for row in rows:
        print(str(row.id) + '. ' + row.task)


def print_weeks_tasks():
    day_count = 0
    today = datetime.today().date()
    while day_count < 7:
        week_day_date = today + timedelta(days=day_count)

        print(week_day_date.strftime("%A %d %b:"))
        rows = session.query(Table).filter(Table.deadline == week_day_date).all()
        if len(rows) == 0:
            print("Nothing to do!")
        for row in rows:
            print(str(row.id) + '. ' + row.task)
        day_count += 1
        print("")


def print_all_tasks():
    rows = session.query(Table).all()
    if len(rows) == 0:
        print("Nothing to do!")
    for row in rows:
        print(str(row.id) + '. ' + row.task + '. ' + row.deadline.strftime("%d %b"))


def add_task():
    print("Enter task")
    task_text = input()
    print("Enter deadline")
    task_deadline = input()
    deadline_field = datetime.strptime(task_deadline, '%Y-%m-%d').date()
    new_row = Table(task=task_text,
                    deadline=deadline_field)

    session.add(new_row)
    session.commit()
    print("The task has been added!")


def main():
    while True:
        print("1) Today's tasks")
        print("2) Week's tasks")
        print("3) All tasks")
        print("4) Add task")
        print("0) Exit")

        user_input = int(input())
        print("")
        if user_input == 1:
            print_todays_tasks()
        elif user_input == 2:
            print_weeks_tasks()
        elif user_input == 3:
            print_all_tasks()
        elif user_input == 4:
            add_task()
        elif user_input == 0:
            print("Bye!")
            break
        else:
            print("Incorrect input, choose 1, 2, 3, 4 or 0")
        print("")


main()
