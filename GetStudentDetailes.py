from PyPDF2 import PdfReader

def get_sgpa(pdfName,seatnoRange):
    reader = PdfReader(f"{pdfName}")
    pageCount = reader.numPages
    page = []

    for each_page in range(pageCount):
        page += reader.getPage(each_page).extract_text().split("\n")

    try:
        file = open(f"TEMP/{pdfName}_sgpa.csv", "w")
    except FileNotFoundError:
        print("GSD PDF Not Found")
    column_name = "PRN,SEAT NO,NAME OF STUDENT,SEM,SEM 1,SEM 2,SEM 3,SEM 4,SEM 5,SEM 6\n"
    file.write(column_name)

    for i in range(len(page)):
        eachLine = page[i]
        student_info = page[i]
        eachLine = eachLine.replace("*", " ").replace("!", " ").replace("$", " ").replace("@", " ").replace("#"," ").replace("&", " ")
        eachLine = eachLine.split("  ")

        if len(student_info) == 133 and student_info.startswith(f'{seatnoRange}', 1, 4):
            prn = student_info[82:96].strip()
            seatNo = student_info[1:6].strip()
            name = student_info[8:51].strip()
            gender = student_info[80].strip()
            sem = student_info[96:99].strip()

        if student_info.startswith(" SGPA") or student_info.startswith(" RES"):
            if sem == '1':
                grades_line = student_info
                if grades_line.startswith(" RES"):
                    sem1, sem2, sem3, sem4,sem5,sem6 = 'F', ' ', ' ', ' ',' ',' '

                elif grades_line.startswith(" SGPA"):
                    sem1, sem2, sem3, sem4,sem5,sem6 = grades_line[12:16], ' ', ' ', ' ',' ',' '
                file.write(f"{prn}, {seatNo}, {name}, {sem}, {sem1}, {sem2}, {sem3}, {sem4}, {sem5}, {sem6}\n")

            if sem == '2':
                grades_line = student_info
                if grades_line.startswith(" RES"):
                    sem1, sem2, sem3, sem4,sem5,sem6 = 'F', 'F', ' ', ' ',' ',' '

                elif grades_line.startswith(" SGPA"):
                    sem1, sem2, sem3, sem4,sem5,sem6 = grades_line[12:16], grades_line[21:25], ' ', ' ',' ',' '
                file.write(f"{prn}, {seatNo}, {name}, {sem}, {sem1}, {sem2}, {sem3}, {sem4}, {sem5}, {sem6}\n")

            if sem == '3':
                grades_line = student_info
                if grades_line.startswith(" RES"):
                    sem1, sem2, sem3, sem4,sem5,sem6 = 'F', 'F', 'F', ' ',' ',' '

                elif grades_line.startswith(" SGPA"):
                    sem1, sem2, sem3, sem4,sem5,sem6 = grades_line[12:16], grades_line[21:25], grades_line[30:34], ' ',' ',' '
                file.write(f"{prn}, {seatNo}, {name}, {sem}, {sem1}, {sem2}, {sem3}, {sem4}, {sem5}, {sem6}\n")

            if sem == '4':
                grades_line = student_info
                if grades_line.startswith(" RES"):
                    sem1, sem2, sem3, sem4,sem5,sem6 = 'F', 'F', 'F', 'F',' ',' '

                elif grades_line.startswith(" SGPA"):
                    sem1, sem2, sem3, sem4,sem5,sem6 = grades_line[12:16], grades_line[21:25], grades_line[30:34], grades_line[39:43],' ',' '
                file.write(f"{prn}, {seatNo}, {name}, {sem}, {sem1}, {sem2}, {sem3}, {sem4}, {sem5}, {sem6}\n")

            if sem == '5':
                grades_line = student_info
                if grades_line.startswith(" RES"):
                    sem1, sem2, sem3, sem4,sem5,sem6 = 'F', 'F', 'F', 'F','F',' '

                elif grades_line.startswith(" SGPA"):
                    sem1, sem2, sem3, sem4,sem5,sem6 = grades_line[12:16], grades_line[21:25], grades_line[30:34], grades_line[39:43],grades_line[48:52],' '
                file.write(f"{prn}, {seatNo}, {name}, {sem}, {sem1}, {sem2}, {sem3}, {sem4}, {sem5}, {sem6}\n")

            if sem == '6':
                grades_line = student_info
                if grades_line.startswith(" RES"):
                    sem1, sem2, sem3, sem4,sem5,sem6 = 'F', 'F', 'F', 'F','F','F'

                elif grades_line.startswith(" SGPA"):
                    sem1, sem2, sem3, sem4,sem5,sem6 = grades_line[12:16], grades_line[21:25], grades_line[30:34], grades_line[39:43],grades_line[48:52],grades_line[57:61]
                file.write(f"{prn}, {seatNo}, {name}, {sem}, {sem1}, {sem2}, {sem3}, {sem4}, {sem5}, {sem6}\n")

    file.close()


