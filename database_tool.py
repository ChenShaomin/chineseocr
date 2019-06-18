import pymysql

db = pymysql.connect("localhost", "root", "123456", "cadb")

cursor = db.cursor()

cursor.execute("DROP TABLE IF EXISTS catest")

sql1 = """CREATE TABLE catest (
         id INT UNSIGNED AUTO_INCREMENT,
         报告编号 VARCHAR(20),
         中国民航总局授权证号 VARCHAR(20),
         合同号 VARCHAR(20),
         送修单位 VARCHAR(100),
         送修日期 VARCHAR(20),
         修理单位 VARCHAR(100),
         件名 VARCHAR(100),
         件号 VARCHAR(20),
         序号 VARCHAR(20),
         拆件原因 VARCHAR(100),
         拆件原因确认 VARCHAR(100),
         索赔确认 VARCHAR(100),
         修前查验报告 VARCHAR(400),
         维修措施及修后结论 VARCHAR(400),
         修理级别 VARCHAR(100),
         PRIMARY KEY (id)
         )ENGINE=InnoDB DEFAULT CHARSET=utf8;"""

sql = """CREATE TABLE catest (
         id INT UNSIGNED AUTO_INCREMENT,
         PRIMARY KEY (id)
         )ENGINE=InnoDB DEFAULT CHARSET=utf8;"""

cursor.execute(sql1)

db.close()
