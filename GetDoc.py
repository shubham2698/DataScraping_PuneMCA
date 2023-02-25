import pymysql
import matplotlib.pyplot as plt
import numpy as np
from fpdf import FPDF

# dbName=input("ENTER DATABASE NAME : ").lower()
# dbTableName=input("ENTER TABLE NAME : ")
dbName="mca2019"
dbTableName="mca2019_all"

try:
    connection = pymysql.connect(host="localhost", user="root", passwd="",database=f"{dbName}")
    db = connection.cursor()
except:
    print("FAILED TO CONNECT DATABASE")
    exit()



def show_menu():
    print("-------------------------------")
    print("ENTER 1 FOR VIEW ANALYSIS\nENTER 2 FOR EXIT\nWaiting for input...")
    menu_no=int(input())
    print("-------------------------------")
    if menu_no == 1:
        show_analysis(dbTableName)
        exit()
    elif menu_no == 2:
        exit()
    else:
        print("Invalid Input try again")
        show_menu()

def plot_linechart(str,avgMarksbarChartDict,query_sem):
    courses = list(avgMarksbarChartDict.keys())
    values = list(avgMarksbarChartDict.values())
    fig = plt.figure(figsize=(10, 8))
    plt.plot(courses, values, color='green')
    plt.ylim(0, 70)
    for i in range(len(courses)):
        plt.text(i, values[i], values[i], ha='center')
    plt.xlabel("SUBJECT CODE")
    plt.ylabel(f"{str} MARKS")
    plt.title(f"{str} MARKS OF SEMESTER {query_sem}")
    plt.savefig(f'MCATEST/ANALYSIS/{str}_Marks_SEM{query_sem}.png')

def plot_barchart(str,avgMarksbarChartDict,query_sem):
    courses = list(avgMarksbarChartDict.keys())
    values = list(avgMarksbarChartDict.values())
    fig = plt.figure(figsize=(10, 8))
    plt.bar(courses, values, color='green')
    plt.ylim(0, 70)
    for i in range(len(courses)):
        plt.text(i, values[i], values[i], ha='center')
    plt.xlabel("SUBJECT CODE")
    plt.ylabel(f"{str} MARKS")
    plt.title(f"{str} STUDENT OF SEMESTER {query_sem}")
    plt.savefig(f'MCATEST/ANALYSIS/{str}_Student_SEM{query_sem}.png')

def plot_piechart(passFail,lable,myexplode,query_sem):
    plt.pie(passFail, labels=lable, explode=myexplode, startangle=270, counterclock=False, shadow=True)
    plt.title(f"Total Passed/Failed In Semester {query_sem}")
    plt.savefig(f'MCATEST/ANALYSIS/PASS_FAILED_SEM{query_sem}.png')

# def plot_scatteredchart(str,sgpaListScattered ,query_sem):
#     fig= plt.figure(figsize=(10,8))
#     x=np.array(0,1,2,3,4,5,6,7,8,9,10)
#     y=sgpaListScattered
#     x=x.reshape(len(x),1)
#     plt.scatter(x,sgpaListScattered, color='green')
#     plt.xlabel("SGPA Range")
#     plt.ylabel(f"{str} SGPA")
#     plt.title(f"SGPA OF SEMESTER {query_sem}")
#     plt.show()

def show_analysis(dbTableName):
    semList = []
    pdf = FPDF()
    pdf.set_font("Times", size=18)
    pdf.add_page()


    db.execute(f"SELECT DISTINCT(`SEM`) FROM `{dbTableName}`")
    result = db.fetchall()
    for each in result:
        semList.append(each[0])

    pdf.set_font("Times", size=25)
    pdf.cell(200, 10, txt=f"PRATIBHA INSTITUTE OF BUSINESS MANAGEMENT \n", ln=1, align='C')
    pdf.set_font("Times", size=18)
    pdf.cell(200, 10, txt=f"MASTERS IN COMPUTER APPLICATION ( MANAGEMENT ) \n", ln=1, align='C')

    # print("FOLLOWING SEMESTER IS PRESENT IN THIS DATABASE :")
    # for each in semList:
    #     print("SEM", each)

    for query_sem in semList:

        db.execute(
            f"SELECT COUNT(DISTINCT(`NAME OF STUDENT`)) FROM {dbTableName} WHERE SEM={query_sem} AND `SUBJECT CODE`=121 OR `SUBJECT CODE`=111")
        result = db.fetchall()
        print("---------------------------------------------")
        print(f"SEMESTER {query_sem} ANALYSIS IS HERE")
        pdf.add_page()

        pdf.cell(200, 10, txt=f"SEMESTER {query_sem} ANALYSIS IS HERE \n", ln=1, align='C')
        pdf.cell(200, 10, txt=f"\n", ln=1, align='C')
        print("---------------------------------------------\n")
        pdf.set_font("TIMES", "")
        total_students = int(result[0][0])
        print("Total Number of student : ", result[0][0], "\n")
        pdf.cell(200, 10, txt=f"\nTotal Number of student : {result[0][0]} \n", ln=1, align='L')

        db.execute(
            f"SELECT COUNT(DISTINCT(`NAME OF STUDENT`)) FROM {dbTableName} WHERE SEM={query_sem} AND `SEM {query_sem}`!='F'")
        result = db.fetchall()
        print("Total Passed Student : ", result[0][0])
        pdf.cell(200, 10, txt=f"Total Passed Student : {result[0][0]} \n", ln=1, align='L')

        db.execute(
            f"SELECT COUNT(DISTINCT(`NAME OF STUDENT`)) FROM {dbTableName} WHERE SEM={query_sem} AND `SEM {query_sem}`!='F' AND `GENDER`=' M'")
        result = db.fetchall()
        passedBoys = int(result[0][0])
        print("Total Passed Boys : ", result[0][0])
        pdf.cell(200, 10, txt=f"Total Passed Boys : {result[0][0]} \n", ln=1, align='L')

        db.execute(
            f"SELECT COUNT(DISTINCT(`NAME OF STUDENT`)) FROM {dbTableName} WHERE SEM={query_sem} AND `SEM {query_sem}`!='F' AND `GENDER`=' F'")
        result = db.fetchall()
        passedGirls = int(result[0][0])
        print("Total Passed Girls : ", result[0][0])
        pdf.cell(200, 10, txt=f"Total Passed Girls : {result[0][0]} \n", ln=1, align='L')

        db.execute(
            f"SELECT COUNT(DISTINCT(`NAME OF STUDENT`)) FROM {dbTableName} WHERE SEM={query_sem} AND `GRADE POINT`='FF'")
        result = db.fetchall()
        failedStudent = int(result[0][0])
        print("Total Failed Student : ", result[0][0])
        pdf.cell(200, 10, txt=f"Total Failed Student : {result[0][0]} \n", ln=1, align='L')
        # pdf.cell(200, 10, txt=f"\n", ln=1, align='C')
        passFail = np.array([passedBoys, passedGirls, failedStudent])
        lable = [f"PASSED MALE : {passedBoys}", f"PASSED FEMALE : {passedGirls}", f"TOTAL FAILED : {failedStudent} "]
        myexplode = [0, 0, 0.2]

        db.execute(
            f"SELECT DISTINCT(`NAME OF STUDENT`),`SEM {query_sem}` FROM {dbTableName}  WHERE `SEM {query_sem}`!='F' AND SEM={query_sem} AND `GENDER`=' M' ORDER BY `SEM {query_sem}` DESC LIMIT 3")
        result = db.fetchall()
        print("TOP 3 BOYS : ")
        pdf.cell(200, 10, txt=f"TOP 3 BOYS :  \n", ln=1, align='L')
        for each in result:
            print(each[0].strip(), each[1])
            pdf.cell(200, 10, txt=f"{each[0].strip()} : {each[1]} \n", ln=1, align='L')

        db.execute(
            f"SELECT DISTINCT(`NAME OF STUDENT`),`SEM {query_sem}` FROM {dbTableName}  WHERE `SEM {query_sem}`!='F' AND SEM={query_sem} AND `GENDER`=' M' AND `SEM {query_sem}`!=' F' ORDER BY `SEM {query_sem}` ASC LIMIT 3")
        result = db.fetchall()
        print("\nLAST 3 BOYS : ")
        pdf.cell(200, 10, txt=f"\n", ln=1, align='C')
        pdf.cell(200, 10, txt=f"LAST 3 BOYS :  \n", ln=1, align='L')
        for each in result:
            print(each[0].strip(), each[1])
            pdf.cell(200, 10, txt=f"{each[0].strip()} : {each[1]} \n", ln=1, align='L')

        db.execute(
            f"SELECT DISTINCT(`NAME OF STUDENT`),`SEM {query_sem}` FROM {dbTableName}  WHERE `SEM {query_sem}`!='F' AND SEM={query_sem} AND `GENDER`=' F' ORDER BY `SEM {query_sem}` DESC LIMIT 3")
        result = db.fetchall()
        print("\nTOP 3 GIRLS : ")
        pdf.cell(200, 10, txt=f"\n", ln=1, align='C')
        pdf.cell(200, 10, txt=f"TOP 3 GIRLS :  \n", ln=1, align='L')
        for each in result:
            print(each[0].strip(), each[1])
            pdf.cell(200, 10, txt=f"{each[0].strip()} : {each[1]} \n", ln=1, align='L')

        db.execute(
            f"SELECT DISTINCT(`NAME OF STUDENT`),`SEM {query_sem}` FROM {dbTableName}  WHERE `SEM {query_sem}`!='F' AND SEM={query_sem} AND `GENDER`=' F' AND `SEM {query_sem}`!=' F' ORDER BY `SEM {query_sem}` ASC LIMIT 3")
        result = db.fetchall()
        print("\nLAST 3 GIRLS : ")
        pdf.cell(200, 10, txt=f"\n", ln=1, align='C')
        pdf.cell(200, 10, txt=f"LAST 3 GIRLS :  \n", ln=1, align='L')
        for each in result:
            print(each[0].strip(), each[1])
            pdf.cell(200, 10, txt=f"{each[0].strip()} : {each[1]} \n", ln=1, align='L')

        print("\n")

        db.execute(f"SELECT DISTINCT(`SUBJECT CODE`) FROM {dbTableName} WHERE SEM={query_sem}")
        result = db.fetchall()
        subjectList = []
        for each in result:
            subjectList.append(each[0])

        avgMarksbarChartDict = {}
        minMarksbarChartDict = {}
        maxMarksbarChartDict = {}
        failedChartDict = {}
        sgpaListScattered = []

        for i in range(len(subjectList)):
            db.execute(
                f"SELECT MAX(`EXTERNAL`) FROM {dbTableName} WHERE SEM={query_sem} AND `SUBJECT CODE`='{subjectList[i]}' AND `EXTERNAL`!=0 AND `EXTERNAL`!=' AA'")
            result = db.fetchall()
            if result[0][0] != 0.0 and result[0][0] != None:
                print(f"Maximum marks of subject code '{subjectList[i]}'        : {result[0][0]}")
                maxMarksbarChartDict[f"{subjectList[i]}"] = int(result[0][0])

                db.execute(
                    f"SELECT MIN(`EXTERNAL`) FROM {dbTableName} WHERE SEM={query_sem} AND `SUBJECT CODE`='{subjectList[i]}' AND `EXTERNAL`!=0 AND `EXTERNAL`!=' AA'")
                result = db.fetchall()
                print(f"Minimum marks of subject code '{subjectList[i]}'        : {result[0][0]}")
                minMarksbarChartDict[f"'{subjectList[i]}'"] = int(result[0][0])

                db.execute(
                    f"SELECT AVG(`EXTERNAL`) FROM {dbTableName} WHERE SEM={query_sem} AND `SUBJECT CODE`='{subjectList[i]}'")
                result = db.fetchall()
                print(f"Average marks of subject code '{subjectList[i]} '       : {round(result[0][0], 2)}")
                avgMarksbarChartDict[f"'{subjectList[i]}'"] = round(result[0][0], 2)

                db.execute(
                    f"SELECT COUNT(DISTINCT(`NAME OF STUDENT`)) FROM {dbTableName} WHERE SEM={query_sem} AND `SUBJECT CODE`='{subjectList[i]}' AND `GRADE POINT`!='FF'")
                result = db.fetchall()
                print(f"No of Student passed in subject code '{subjectList[i]}' : {result[0][0]}")

                db.execute(
                    f"SELECT COUNT(DISTINCT(`NAME OF STUDENT`)) FROM {dbTableName} WHERE SEM={query_sem} AND `SUBJECT CODE`='{subjectList[i]}' AND `GRADE POINT`='FF'")
                result = db.fetchall()
                print(f"No of Student Failed in subject code '{subjectList[i]}' : {result[0][0]}")
                failedChartDict[f"'{subjectList[i]}'"] = round(result[0][0], 2)

                db.execute(f"SELECT DISTINCT(`SEM {query_sem}`) FROM `{dbTableName}` WHERE SEM={query_sem}")
                result = db.fetchall()
                for each in result:
                    sgpaListScattered.append(each[0])

                print("\n")


        plot_piechart(passFail, lable, myexplode, query_sem)
        plot_barchart("FAILED", failedChartDict, query_sem)
        plot_linechart("MINIMUM", minMarksbarChartDict, query_sem)
        plot_linechart("AVERAGE", avgMarksbarChartDict, query_sem)
        plot_linechart("MAXIMUM", maxMarksbarChartDict, query_sem)
        # # plot_scatteredchart("SGPA RANGE ", sgpaListScattered, query_sem)
        pdf.image(f"MCATEST/ANALYSIS/PASS_FAILED_SEM{query_sem}.png", w=200, h=140)
        pdf.image(f"MCATEST/ANALYSIS/MINIMUM_Marks_SEM{query_sem}.png", w=200, h=140 )
        pdf.image(f"MCATEST/ANALYSIS/AVERAGE_Marks_SEM{query_sem}.png", w=200, h=140)
        pdf.image(f"MCATEST/ANALYSIS/MAXIMUM_Marks_SEM{query_sem}.png", w=200, h=140)
        pdf.image(f"MCATEST/ANALYSIS/FAILED_Student_SEM{query_sem}.png", w=200, h=140,x=220)
    pdf.output(rf"MCATEST/ANALYSIS/Report.pdf")





show_menu()
db.close()