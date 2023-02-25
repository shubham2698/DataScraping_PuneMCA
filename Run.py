import MCA as mcaPDf

dbName="pratibha_institute_of_business_management"
dbName=dbName.lower()
pdfName=input("Enter pdf name : ( with extension xyz.pdf ) : ")
seatnoRange=input("Enter seat no starting with : ( if seat no is 23654 then enter 23 ) : ")

db1=mcaPDf.connection_mysql_server()
# mcaPDf.create_database(dbName,db1)
mcaPDf.scrape_data(pdfName,seatnoRange,db1,dbName)
db1.close()
df_sgpa,df_info,engine=mcaPDf.load_data(pdfName,dbName)
pdfName=mcaPDf.get_pdf_name(pdfName)
mcaPDf.convert_to_sql_table(pdfName,df_sgpa,df_info,engine)
db=mcaPDf.connect_database(dbName)
mcaPDf.create_folder(dbName)
mcaPDf.combine_operation(pdfName,dbName,engine)
dbTableName=mcaPDf.get_table_name(pdfName)
mcaPDf.convert_table_structure(dbTableName,db)
mcaPDf.drop_tempfile(pdfName,db)
mcaPDf.process_complete_msg()
mcaPDf.show_analysis(dbName,dbTableName,db)
db.close()