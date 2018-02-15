import lib


if __name__ == "__main__":
    user = lib.login()
    while True:
        if user.name == 'root':
            choice = input('''1.add Teacher 2.del Teacher 3.add Lesson
            4 del Lesson   5.add Student  6.del Student''')
            if choice == '1':
                user.add_teacher()
            elif choice == '2':
                user.remove('Teacher')
            elif choice == '3':
                user.add_lesson()
            elif choice == '4':
                user.remove('Lesson')
            elif choice == '5':
                user.add_student()
            elif choice == '6':
                user.remove('Student')
            elif not choice:
                continue
            elif choice == 'q':
                break
        else:
            choice = input('''1.add Lesson   2.history    3.learn   4.evaluate''')
            if choice == '1':
                user.add_lesson()
            elif choice == '2':
                user.show_lesson()
                user.show_history()
            elif choice == '3':
                user.learn_lesson()
            elif choice == '4':
                user.evaluate()
            elif not choice:
                continue
            elif choice == 'q':
                break
