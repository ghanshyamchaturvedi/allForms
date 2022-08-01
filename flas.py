from flask import request  
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import select
from selenium.webdriver.support.select import Select
import time
from database import *
from flask import Flask, render_template
app = Flask(__name__, template_folder='template')
drivers = []

@app.route('/')
def start():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template("pages-login.html")

@app.route('/account', methods=['POST'])
def account():
    print(request.form)
    username= request.form.get('username')
    print(username)
    password= request.form.get('password')
    result = verifylogin(username, password)
    print(result)
    if result ==True:
        
        return render_template('index-1.html',name=username)
    else:
        return render_template('pages-register.html')

@app.route('/newuser', methods=['POST'])
def newuser():
    registration = request.form
    name = request.form.get('name')
    username = request.form.get('username')
    password = request.form.get('password')
    email = request.form.get('email')
    result= insertRe(name, username, password, email)
    print(result)
    if result == True:
        return render_template('index-1.html',name=username)
    else :
        return 'Wrong Credential'

@app.route('/resgistration')
def resgistration():
    return render_template('pages-register.html')

@app.route('/account/editor')
def editor():
    return render_template('editor.html')

@app.route('/<username>', methods = ['POST'])
def loginSaleforce(username):
    print(username)
    driver = webdriver.Edge(executable_path='C:\\Users\\ghanshyam.c\\Desktop\\msedgedriver.exe')
    driver.get('https://login.salesforce.com/')
    Username = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
    Password = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='pw']")))
    Username.clear()
    susername= request.form.get('username')
    spassword= request.form.get('password')
    print(susername + " "+spassword)
    Username.send_keys(susername)
    Password.clear()
    Password.send_keys(spassword)
    Remerberme = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='rememberUn']"))).click()
    login_button = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='Login']"))).click()
    time.sleep(2)
    reurl = driver.current_url
    s_list = reurl.split("/")
    orgurl = s_list[2]
    driverindex = len(drivers)
    drivers.append(driver)
    result = updateSinfo(username, susername, spassword, orgurl,driverindex)
    print(result)
    if result == True:
        print('Logged in salesforce with url = '+orgurl)
        return 'Account Verified'
    else:
        return 'Account Not Verified'

@app.route('/<string:username>/<string:ObjectApi>',methods = ['POST'])
def formsubmission(username,ObjectApi):
    temp=0
    #object_api = request.form.get('ObjectApi')
    y = request.form
    driverindex= int(fetchDriverindex(username))
    driver= drivers[driverindex]
    driver.execute_script("window.open()")
    temp= temp +1
    driver.switch_to.window(driver.window_handles[temp])
    driver.get('https://workbench.developerforce.com/insert.php')
    time.sleep(2)
    driver.find_element(By.XPATH, '//*[@id="termsAccepted"]').click()
    driver.find_element(By.XPATH, '//*[@id="loginBtn"]').click()
    time.sleep(2)
    select = driver.find_element(By.XPATH, '//*[@id="default_object"]')
    drp = Select(select)
    drp.select_by_value(ObjectApi)
    print('Object has selected')
    driver.find_element(By.XPATH, '//*[@id="mainBlock"]/form/table/tbody/tr[5]/td/input').click()
    print('clicked on next')
    time.sleep(2)
    Keys= y.keys()
    for fields in Keys:
        field = driver.find_element(By.NAME, fields)
        field.clear()
        field.send_keys(y.get(fields))
    print('trying to click in insert')
    time.sleep(2)
   #driver.find_element(By.XPATH,'//*[@id="mainBlock"]/form/p[2]/input') 

    driver.find_element(By.CSS_SELECTOR, 'input[name="action"').click()
    driver.execute_script("window.close()")
    return render_template('index-1.html',name=username)


if __name__ == '__main__':
    app.run(debug=True)
