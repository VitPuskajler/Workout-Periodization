

def get_create_tables_query():
    member_table = """ CREATE TABLE IF NOT EXISTS member (
                                MemberID integer PRIMARY KEY,
                                firstName text NOT NULL,
                                lastName text NOT NULL,
                                startDate text NOT NULL,
                                email text NOT NULL,
                                password text NOT NULL
                            ); """

    memberExcercise_table = """CREATE TABLE IF NOT EXISTS memberExercise (
                                    ExerciseID integer NOT NULL,
                                    SetID integer NOT NULL,
                                    MemberID integer NOT NULL,
                                    FOREIGN KEY (SetID)
                                        REFERENCES Sets (SetID),
                                    FOREIGN KEY (MemberID)
                                        REFERENCES MemberID,
                                    FOREIGN KEY (ExerciseID)
                                        REFERENCES EXERCISE (exerciseID),
                                    PRIMARY KEY (ExerciseID, SetID, MemberID)
                        
                                );"""

    set_table = """ CREATE TABLE IF NOT EXISTS Sets (
                        setID integer PRIMARY KEY,
                        reps integer NOT NULL,
                        success integer NOT NULL
                        ); """

    exercise_table = """ CREATE TABLE IF NOT EXISTS Exercise (
                                exerciseID integer PRIMARY KEY,
                                muscleGroupID integer NOT NULL,
                                exerciseName text NOT NULL,
                                FOREIGN KEY (muscleGroupID)
                                    REFERENCES MuscleGroup (MuscleGroupID)
                            ); """

    exerciseMuscleGroup_table = """ CREATE TABLE IF NOT EXISTS ExerciseMuscleGroup (
                                ExerciseID integer NOT NULL,
                                muscleGroupID integer NOT NULL,
                                FOREIGN KEY (muscleGroupID)
                                    REFERENCES MuscleGroup (muscleGroupID),
                                FOREIGN KEY (ExerciseID)
                                    REFERENCES Exercise (ExerciseID)
                            ); """

    muscleGroup_table = """ CREATE TABLE IF NOT EXISTS MuscleGroup (
                                muscleGroupID integer PRIMARY KEY,
                                muscleGroupName text NOT NULL
                            ); """

    muscle_table = """ CREATE TABLE IF NOT EXISTS Muscle (
                                muscleID integer PRIMARY KEY,
                                muscleGroupID integer NOT NULL,
                                muscleName text NOT NULL,
                                FOREIGN KEY (muscleGroupID)
                                    REFERENCES MuscleGroup (muscleGroupID)
                            ); """

    return [member_table, set_table, muscleGroup_table, exercise_table, memberExcercise_table, muscle_table, exerciseMuscleGroup_table]
