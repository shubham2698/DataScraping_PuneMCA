from PyPDF2 import PdfReader

def get_info(pdfName,seatnoRange):
    reader = PdfReader(f"{pdfName}")
    pageCount = reader.numPages
    page = []

    for each_page in range(pageCount):
        page += reader.getPage(each_page).extract_text().split("\n")

    try:
        file = open(f"TEMP/{pdfName}_info.csv", "w")
    except FileNotFoundError:
        print("GSM PDF Not Found")
    column_name = "PRN,SEAT NO,GENDER,NAME OF STUDENT,SEM,SUBJECT CODE,INTERNAL,EXTERNAL,TOTAL,GRADE,GRADE POINT\n"
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

        if len(eachLine[0]) == 6 or len(eachLine[0]) == 7 and eachLine[0].endswith(":"):

            for eachWord in eachLine:
                if eachWord.endswith(":"):
                    subjectCode = str(eachLine[eachLine.index(eachWord)]).strip().removesuffix(':').strip()
                    internal = eachLine[eachLine.index(eachWord) + 1]
                    external = eachLine[eachLine.index(eachWord) + 2]
                    total = eachLine[eachLine.index(eachWord) + 3]
                    try:
                        grade = eachLine[eachLine.index(eachWord) + 4]
                    except:
                        grade = eachLine[eachLine.index(eachWord) + 3]
                        if grade == 'F FF':
                            grade = "F"
                            gradePoint = "FF"
                    try:
                        gradePoint = eachLine[eachLine.index(eachWord) + 6]
                    except:
                        pass

                    if internal == '':
                        internal = eachLine[eachLine.index(eachWord) + 2]
                        external = eachLine[eachLine.index(eachWord) + 3]
                        total = eachLine[eachLine.index(eachWord) + 4]
                        grade = eachLine[eachLine.index(eachWord) + 5]
                        if total == '':
                            total = eachLine[eachLine.index(eachWord) + 5]
                        if grade == 'F FF':
                            grade = "F"
                            gradePoint = "FF"
                    elif len(internal) == 7:
                        tmp_internal = internal
                        internal = tmp_internal[0:3]
                        external = tmp_internal[4:7]
                        total = eachLine[eachLine.index(eachWord) + 2]
                        grade = eachLine[eachLine.index(eachWord) + 3]
                        gradePoint = eachLine[eachLine.index(eachWord) + 4]
                    elif len(internal) == 6:
                        tmp_internal = internal
                        internal = tmp_internal[0:3]
                        external = tmp_internal[3:6]
                        total = eachLine[eachLine.index(eachWord) + 3]
                        if total == "F FF":
                            total = eachLine[eachLine.index(eachWord) + 2]
                        if grade == "F FF":
                            grade = "F"
                            gradePoint = "FF"

                    elif external == '':
                        external = 0
                        total = eachLine[eachLine.index(eachWord) + 4]
                        grade = eachLine[eachLine.index(eachWord) + 5]
                        try:
                            gradePoint = eachLine[eachLine.index(eachWord) + 7]
                        except:
                            gradePoint = eachLine[eachLine.index(eachWord) + 6]
                        if internal == "AA" and external == 0:
                            external = eachLine[eachLine.index(eachWord) + 3]
                            total = eachLine[eachLine.index(eachWord) + 5]
                            grade = eachLine[eachLine.index(eachWord) + 6]
                        if grade == 'F FF':
                            grade = "F"
                            gradePoint = "FF"

                    elif grade == 'F FF':
                        grade = "F"
                        gradePoint = "FF"
                    elif grade == ' AbFF':
                        grade = "Ab"
                        gradePoint = "FF"
                    if grade == 'AbFF':
                        grade = "Ab"
                        gradePoint = "FF"
                    if gradePoint == 'F FF':
                        grade = "F"
                        gradePoint = "FF"
                    if gradePoint.endswith(":"):
                        gradePoint = eachLine[eachLine.index(gradePoint) - 1]
                    if gradePoint == '':
                        gradePoint = eachLine[eachLine.index(gradePoint) + 1]
                        if gradePoint == '':
                            gradePoint = eachLine[eachLine.index(gradePoint) + 6]
                    file.write(
                        f"{prn}, {seatNo}, {gender}, {name}, {sem}, {subjectCode}, {internal}, {external}, {total},{grade},{gradePoint}\n")
                    # print([prn,seatNo,gender,name,sem,subjectCode,internal,external,total,grade,gradePoint])
        # else:
        #     print(eachLine)
    file.close()
