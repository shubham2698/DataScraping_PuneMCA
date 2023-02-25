import pymysql
from sqlalchemy import create_engine
import pandas as pd
import time
import os
import GetStudentDetailes,GetStudentsMarks
import matplotlib.pyplot as plt
import numpy as np
from fpdf import FPDF

def connection_mysql_server():
    try:
        connection1 = pymysql.connect(host="localhost", user="root", passwd="")
        mysql_server_connection = connection1.cursor()
        return mysql_server_connection
    except:
        print("\033[91mFAILED TO CONNECT MYSQL SERVER\033[0m")
        exit()


def create_database(dbName,db1):
    try:
        db1.execute(f"CREATE DATABASE {dbName.lower()}")
    except:
        print("\033[91mDatabase Name Already Taken \nTry Again With Another Name\033[0m")
        exit()


def scrape_data(pdfName,seatnoRange,db1,dbName):
    try:
        GetStudentDetailes.get_sgpa(pdfName, seatnoRange)
        GetStudentsMarks.get_info(pdfName, seatnoRange)
    except:
        print("\033[91mPDF Document Not Found \nTry Again With Correct Name\033[0m")
        db1.execute(f"DROP DATABASE {dbName.lower()}")
        db1.close()
        exit()


def load_data(pdfName,dbName):
    engine = create_engine("mysql+pymysql://{user}:{pw}@{host}/{db}".format(host='localhost', db=f'{dbName}', user='root', pw=''))
    df_sgpa = pd.read_csv(f"TEMP/{pdfName.lower()}_sgpa.csv")
    df_info = pd.read_csv(f"TEMP/{pdfName.lower()}_info.csv")
    return df_sgpa,df_info,engine


def get_pdf_name(pdfName):
    pdfName = f"{pdfName[0:len(pdfName) - 4]}"
    return pdfName


def convert_to_sql_table(pdfName,df_sgpa,df_info,engine):
    df_sgpa.to_sql(f'{pdfName.lower()}_sgpa', engine, index=False)
    df_info.to_sql(f'{pdfName.lower()}_info', engine, index=False)


def connect_database(dbName):
    try:
        connection = pymysql.connect(host="localhost", user="root", passwd="", database=f"{dbName}")
        db = connection.cursor()
        return db
    except:
        print("\033[91mFAILED TO CONNECT WITH YOUR DATABASE\033[0m")
        exit()


def create_folder(dbName):
    os.mkdir(f"OUTPUT/{dbName}")


def combine_operation(pdfName,dbName,engine):
    results = pd.read_sql_query(f"SELECT {pdfName.lower() + '_info'}.PRN ,{pdfName.lower() + '_info'}.`SEAT NO`,{pdfName.lower() + '_info'}.`GENDER`,{pdfName.lower() + '_info'}.`NAME OF STUDENT`,{pdfName.lower() + '_info'}.`SEM`,{pdfName.lower() + '_info'}.`SUBJECT CODE`,{pdfName.lower() + '_info'}.`INTERNAL`,{pdfName.lower() + '_info'}.`EXTERNAL`,{pdfName.lower() + '_info'}.`TOTAL`,{pdfName.lower() + '_info'}.`GRADE`,{pdfName.lower() + '_info'}.`GRADE POINT`,{pdfName.lower() + '_sgpa'}.`SEM 1`,{pdfName.lower() + '_sgpa'}.`SEM 2`,{pdfName.lower() + '_sgpa'}.`SEM 3`,{pdfName.lower() + '_sgpa'}.`SEM 4`,{pdfName.lower() + '_sgpa'}.`SEM 5`,{pdfName.lower() + '_sgpa'}.`SEM 6` FROM {pdfName.lower() + '_info'} JOIN {pdfName.lower() + '_sgpa'} ON {pdfName.lower() + '_info'}.`SEAT NO`= {pdfName.lower() + '_sgpa'}.`SEAT NO`",engine)
    results.to_csv(f"OUTPUT/{dbName}/{pdfName.lower() + '_all.csv'}", index=False)
    time.sleep(1)
    df_all = pd.read_csv(f"OUTPUT/{dbName}/{pdfName.lower()}_all.csv")
    df_all.to_sql(f'{pdfName.lower()}_all', engine, index=False)


def get_table_name(pdfName):
    dbTableName = f"{pdfName.lower()}_all"
    return dbTableName


def convert_table_structure(dbTableName,db):
    db.execute(f"ALTER TABLE `{dbTableName}` CHANGE `SUBJECT CODE` `SUBJECT CODE` VARCHAR(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,CHANGE `GENDER` `GENDER` VARCHAR(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL, CHANGE `NAME OF STUDENT` `NAME OF STUDENT` VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL, CHANGE `SEM` `SEM` INT(20) NULL DEFAULT NULL, CHANGE `INTERNAL` `INTERNAL` FLOAT NULL DEFAULT NULL, CHANGE `EXTERNAL` `EXTERNAL` FLOAT NULL DEFAULT NULL, CHANGE `TOTAL` `TOTAL` FLOAT NULL DEFAULT NULL, CHANGE `GRADE POINT` `GRADE POINT` INT NULL DEFAULT NULL, CHANGE `SEM 1` `SEM 1` FLOAT NULL DEFAULT NULL, CHANGE `SEM 2` `SEM 2` FLOAT NULL DEFAULT NULL, CHANGE `SEM 3` `SEM 3` FLOAT NULL DEFAULT NULL, CHANGE `SEM 4` `SEM 4` FLOAT NULL DEFAULT NULL, CHANGE `SEM 5` `SEM 5` FLOAT NULL DEFAULT NULL, CHANGE `SEM 6` `SEM 6` FLOAT NULL DEFAULT NULL")


def drop_tempfile(pdfName,db):
    db.execute(f"DROP TABLE {pdfName.lower()}_sgpa")
    db.execute(f"DROP TABLE {pdfName.lower()}_info")

    os.remove(f"TEMP/{pdfName.lower()}.pdf_sgpa.csv")
    os.remove(f"TEMP/{pdfName.lower()}.pdf_info.csv")


def process_complete_msg():
    print("\n\033[92mProcessing : 100% Completed\033[0m")
    print("\n")


def plot_linechart(str,avgMarksbarChartDict,query_sem,dbName):
    courses = list(avgMarksbarChartDict.keys())
    values = list(avgMarksbarChartDict.values())
    fig = plt.figure(figsize=(25,12 ))
    plt.plot(courses, values, color='green')
    plt.ylim(0, 70)
    for i in range(len(courses)):
        plt.text(i, values[i], values[i], ha='center')
    plt.xlabel("SUBJECT CODE")
    plt.ylabel(f"{str} MARKS")
    plt.title(f"{str} MARKS OF SEMESTER {query_sem}")
    plt.savefig(f'OUTPUT/{dbName}/{str}_Marks_SEM{query_sem}.png')


def plot_barchart(str,avgMarksbarChartDict,query_sem,dbName):
    courses = list(avgMarksbarChartDict.keys())
    values = list(avgMarksbarChartDict.values())
    fig = plt.figure(figsize=(25,12))
    plt.bar(courses, values, color='green')
    plt.ylim(0, 100)
    for i in range(len(courses)):
        plt.text(i, values[i], values[i], ha='center')
    plt.xlabel("SUBJECT CODE")
    plt.ylabel(f"{str} MARKS")
    plt.title(f"{str} STUDENT OF SEMESTER {query_sem}")
    plt.savefig(f'OUTPUT/{dbName}/{str}_Student_SEM{query_sem}.png')


def plot_piechart(passFail,query_sem,passedBoys,passedGirls,failedStudent,dbName):
    lable = [f"PASSED MALE : {passedBoys}", f"PASSED FEMALE : {passedGirls}", f"TOTAL FAILED : {failedStudent} "]
    myexplode = [0, 0, 0.2]
    plt.pie(passFail, labels=lable, explode=myexplode, startangle=270, counterclock=False, shadow=True)
    plt.title(f"Total Passed/Failed In Semester {query_sem}")
    plt.savefig(f'OUTPUT/{dbName}/PASS_FAILED_SEM{query_sem}.png')


def get_sem_list(db,dbTableName):
    semList = []
    db.execute(f"SELECT DISTINCT(`SEM`) FROM `{dbTableName}`")
    result = db.fetchall()
    for each in result:
        semList.append(each[0])
    return semList


def get_subjectList(db,dbTableName,query_sem):
    db.execute(f"SELECT DISTINCT(`SUBJECT CODE`) FROM {dbTableName} WHERE SEM={query_sem}")
    result = db.fetchall()
    subjectList = []
    for each in result:
        subjectList.append(each[0])
    return subjectList


def get_subject_analysis(subjectList,db,dbTableName,query_sem):

    avgMarksbarChartDict = {}
    minMarksbarChartDict = {}
    maxMarksbarChartDict = {}
    failedChartDict = {}

    print("\nSUBJECT ANALYSIS\n")

    analysis_data=[]

    for i in range(len(subjectList)):
        db.execute(f"SELECT MAX(`EXTERNAL`) FROM {dbTableName} WHERE SEM={query_sem} AND `SUBJECT CODE`='{subjectList[i]}' AND `EXTERNAL`!=0 AND `EXTERNAL`!=' AA'")
        result = db.fetchall()


        if result[0][0] != 0.0 and result[0][0] != None:
            maxMarksbarChartDict[f"{subjectList[i]}"] = int(result[0][0])
            max_m = int(result[0][0])

            db.execute(
                f"SELECT MIN(`EXTERNAL`) FROM {dbTableName} WHERE SEM={query_sem} AND `SUBJECT CODE`='{subjectList[i]}' AND `EXTERNAL`!=0 AND `EXTERNAL`!=' AA'")
            result = db.fetchall()
            minMarksbarChartDict[f"'{subjectList[i]}'"] = int(result[0][0])
            min_m = int(result[0][0])

            db.execute(
                f"SELECT AVG(`EXTERNAL`) FROM {dbTableName} WHERE SEM={query_sem} AND `SUBJECT CODE`='{subjectList[i]}'")
            result = db.fetchall()
            avgMarksbarChartDict[f"'{subjectList[i]}'"] = round(result[0][0], 2)
            avg_m = round(result[0][0], 2)

            db.execute(
                f"SELECT COUNT(DISTINCT(`NAME OF STUDENT`)) FROM {dbTableName} WHERE SEM={query_sem} AND `SUBJECT CODE`='{subjectList[i]}' AND `GRADE POINT`!='FF'")
            result = db.fetchall()
            passed_stud = int(result[0][0])

            db.execute(
                f"SELECT COUNT(DISTINCT(`NAME OF STUDENT`)) FROM {dbTableName} WHERE SEM={query_sem} AND `SUBJECT CODE`='{subjectList[i]}' AND `GRADE POINT`='FF'")
            result = db.fetchall()
            failedChartDict[f"'{subjectList[i]}'"] = int(result[0][0])
            fail_stud = int(result[0][0])

            db.execute(
                f"SELECT COUNT(DISTINCT(`NAME OF STUDENT`)) FROM {dbTableName} WHERE SEM={query_sem} AND `SUBJECT CODE`='{subjectList[i]}' AND `GRADE POINT`!='FF' AND `EXTERNAL` < {avg_m}")
            result = db.fetchall()
            below_avg = int(result[0][0])

            tmp_list = [subjectList[i], min_m, avg_m, max_m, passed_stud, fail_stud, below_avg]
            analysis_data.append(tmp_list)

    df_analysis = pd.DataFrame(analysis_data,
                               columns=['Subject', 'Min', 'Avg', 'Max', 'Passed', 'Failed', 'Below Average'])
    print(df_analysis)

    return minMarksbarChartDict, avgMarksbarChartDict, maxMarksbarChartDict, failedChartDict


def export_graphs(minMarksbarChartDict,avgMarksbarChartDict,maxMarksbarChartDict,failedChartDict,query_sem,dbName):
    # plot_piechart(passFail, query_sem, passedBoys, passedGirls, failedStudent)
    plot_barchart("FAILED", failedChartDict, query_sem,dbName)
    plot_linechart("MINIMUM", minMarksbarChartDict, query_sem,dbName)
    plot_linechart("AVERAGE", avgMarksbarChartDict, query_sem,dbName)
    plot_linechart("MAXIMUM", maxMarksbarChartDict, query_sem,dbName)


def show_analysis(dbName,dbTableName,db):
    semList=get_sem_list(db,dbTableName)
    for query_sem in semList:

        print(f"SEM{query_sem} Analysis : \n")
        db.execute(
            f"SELECT COUNT(DISTINCT(`NAME OF STUDENT`)) FROM {dbTableName} WHERE SEM={query_sem} AND `SUBJECT CODE`=121 OR `SUBJECT CODE`=111")
        result = db.fetchall()
        total_students = int(result[0][0])

        print(f"Total Student Sem {query_sem} : ", total_students)

        db.execute(
            f"SELECT COUNT(DISTINCT(`NAME OF STUDENT`)) FROM {dbTableName} WHERE SEM={query_sem} AND `SEM {query_sem}`!='F'")
        result = db.fetchall()

        print(f"Passed : {result[0][0]}")

        db.execute(
            f"SELECT COUNT(DISTINCT(`NAME OF STUDENT`)) FROM {dbTableName} WHERE SEM={query_sem} AND `SEM {query_sem}`!='F' AND `GENDER`=' M'")
        result = db.fetchall()
        passedBoys = int(result[0][0])

        print(f"Passed Male : {passedBoys}")

        db.execute(
            f"SELECT COUNT(DISTINCT(`NAME OF STUDENT`)) FROM {dbTableName} WHERE SEM={query_sem} AND `SEM {query_sem}`!='F' AND `GENDER`=' F'")
        result = db.fetchall()
        passedGirls = int(result[0][0])

        print(f"Passed Female : {passedGirls}")

        db.execute(
            f"SELECT COUNT(DISTINCT(`NAME OF STUDENT`)) FROM {dbTableName} WHERE SEM={query_sem} AND `GRADE POINT`='FF'")
        result = db.fetchall()
        failedStudent = int(result[0][0])

        print(f"Failed : {failedStudent}")

        passFail = np.array([passedBoys, passedGirls, failedStudent])

        db.execute(
            f"SELECT DISTINCT(`NAME OF STUDENT`),`SEM {query_sem}` FROM {dbTableName}  WHERE `SEM {query_sem}`!='F' AND SEM={query_sem} AND `GENDER`=' M' ORDER BY `SEM {query_sem}` DESC LIMIT 3")
        result = db.fetchall()

        print("TOP 3 MALE : ")
        for each in result:

            print(f"{each[0].strip()} : {each[1]}")

        db.execute(
            f"SELECT DISTINCT(`NAME OF STUDENT`),`SEM {query_sem}` FROM {dbTableName}  WHERE `SEM {query_sem}`!='F' AND SEM={query_sem} AND `GENDER`=' F' ORDER BY `SEM {query_sem}` DESC LIMIT 3")
        result = db.fetchall()

        print(f"TOP 3 FEMALE : ")
        for each in result:

            print(f"{each[0].strip()} : {each[1]}")

        subjectList = get_subjectList(db, dbTableName, query_sem)

        minMarksbarChartDict, avgMarksbarChartDict, maxMarksbarChartDict, failedChartDict = get_subject_analysis(
            subjectList, db, dbTableName, query_sem)

        export_graphs(minMarksbarChartDict, avgMarksbarChartDict, maxMarksbarChartDict, failedChartDict, query_sem,
                      dbName)



    print("\n\033[92mDownload : 100%\033[0m")
    print(f"\033[92mPlease Check {dbName} Folder in OUTPUT Directory \nYour Database Server for Database :{dbName}\033[0m\n")

