import lib
import pickle
import datetime


class Root:
    def __init__(self):
        self.name = 'root'
        self.password = '123456'

    @staticmethod
    def add_teacher():
        name = input('''teacher's name:''')
        if lib.database_search(name, 'Teacher'):
            print('Teacher is exist.')
        else:
            gender = input('''teacher's gender:''')
            age = input('''teacher's age:''')
            asset = input('''teacher's assets:''')
            if lib.is_num(asset):
                asset = lib.is_num(asset)
                record = ' %s,%s,%s,%s' % (name, gender, age, asset)
                answer = input('''Do you want to add teacher %s? y to continue''' % record)
                if answer == 'y':
                    lib.database_write(Teacher(name, gender, age, asset))
            else:
                print('input right number!')

    @staticmethod
    def add_lesson():
        name = input('lesson name:')
        if lib.database_search(name, 'Lesson'):
            print('lesson is exist.')
        else:
            date = input('lesson date:')
            fee = input('lesson fee:')
            teacher = input('lesson teacher:')
            if lib.is_num(fee):
                fee = lib.is_num(fee)
                record = '%s,%s,%s,%s' % (name, date, fee, teacher)
                answer = input('Do you want to crate lesson:%s y to continue' % record)
                if answer == 'y':
                    lib.database_write(Lesson(name, date, fee, teacher))
            else:
                print('input right number!')

    @staticmethod
    def add_student():
        name = input('''Student's name:''')
        if lib.database_search(name, 'Student'):
            print('Student is exist.')
        else:
            gender = input('''student's gender:''')
            age = input('''student's age:''')
            password = input('''student's password:''')
            record = ' %s,%s,%s,%s' % (name, gender, age, password)
            answer = input('''Do you want to add student %s? y to continue''' % record)
            if answer == 'y':
                lib.database_write(Student(name, password, gender, age))

    @staticmethod
    def remove(cls):
        name = input('''%s's name:''' % cls)
        if lib.database_search(name, "%s" % cls):
            answer = input('do you want to delete the record:%s y to continue' % name)
            if answer == 'y':
                lib.database_del(name, '%s' % cls)
        else:
            print('no such %s!' % cls)


class Student:
    def __init__(self, name, password, gender, age):
        self.name = name
        self.password = password
        self.gender = gender
        self.age = age
        self.lesson = []
        self.record = {}

    def show_history(self):
        print('''record:%s''' % self.record)

    def show_lesson(self):
        print('lesson:%s' % self.lesson)

    def add_lesson(self):
        lesson = Lesson.show_all()
        while True:
            choice1 = input(' input lesson name:')
            for i in lesson:
                if i.name == choice1:
                    self.lesson.append(i.name)
                    self.record[i.name] = []
                    lib.database_update(self)
            if choice1 == 'q':
                break

    def learn_lesson(self):
        Student.show_lesson(self)
        while True:
            lesson = input('please input lesson to learn:')
            if lesson in self.lesson:
                time_start = datetime.datetime.now().__str__()
                print(lesson)
                time_end = datetime.datetime.now().__str__()
                study_lesson = lib.database_search(lesson, 'Lesson')
                study_fee = study_lesson.fee
                study_teacher = lib.database_search(study_lesson.teacher, 'Teacher')
                study_time = '%s,%s' % (time_start, time_end)
                self.record[lesson].append(study_time)
                study_teacher.asset += study_fee
                lib.database_update(self)
                lib.database_update(study_teacher)
                break
            elif lesson == 'q':
                break
            else:
                print("please choose the right lesson!")

    def evaluate(self):
        Student.show_lesson(self)
        choice_ev = input('please input the lesson you want to evaluate:')
        if choice_ev in self.lesson:
            lesson = lib.database_search(choice_ev, 'Lesson')
            print(lesson.name, lesson.date, lesson.teacher)
            choice_1 = input('are you sure to evaluate this lesson? y to continue')
            if choice_1 == 'y':
                choice_2 = input('which kind of evaluation do you want to give? g for good b for bad')
                choice_3 = input('please input you comment:')
                comment = '%s,%s,%s' % (lesson.name, choice_2, choice_3)
                teacher = lib.database_search(lesson.teacher, 'Teacher')
                teacher.evaluation.append(comment)
                if choice_2 == 'b':
                    teacher.asset -= 50
                lib.database_update(teacher)


class Teacher:
    def __init__(self, name, gender, age, asset):
        self.name = name
        self.gender = gender
        self.age = age
        self.asset = asset
        self.evaluation = []


class Lesson:
    def __init__(self, name, date, fee, teacher):
        self.name = name
        self.date = date
        self.fee = fee
        self.teacher = teacher

    @staticmethod
    def show_all():
        f = open('database', 'rb')
        database = pickle.load(f)
        lesson = [i for i in database if i.__class__.__name__ == 'Lesson']
        for i in lesson:
            print('name:%s,date:%s,fee:%s,teacher:%s' % (i.name, i.date, i.fee, i.teacher))
        f.close()
        return lesson

