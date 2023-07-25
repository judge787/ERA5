#functions that are used throught the program 
def click(variable, path):
    name = variable
    try:
        variable = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, path))
        )
        variable.click()
    except:
        print_in_red(name + " not found")

def inputCoordinates(direction, path, value):
    name = direction
    try:
        direction = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.XPATH, path))
        )
        direction.clear()
        direction.send_keys(value)

    except:
        print("\033[91m" + name + " input not found\033[0m")

def print_in_red(message):
    print("\033[91m" + message + "\033[0m")

def print_in_yellow(message):
    print("\033[93m" + message + "\033[0m")

def print_in_blue(message):
     print("\033[94m" + message + "\033[0m")

def print_in_green(message):
    print('\033[92m' + message + '\033[0m')

def login():#function used to login users  
    global browser, loginPath, loginSubmitPath, emailAddress, password

    click('login', loginPath)

    try:
        email = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '//input[@name="name"]'))
        )
        email.send_keys(emailAddress)

        passwordInput = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '//input[@name="pass"]'))
        )
        passwordInput.send_keys(password)

    except:
        print("Email or password input fields not found")

    click('loginSubmit', loginSubmitPath)

def setUpERA5LandRequest():
    click('hideLake', hideLakePath)
    click('hideSnow', hideSnowPath)
    click('hideSoilwater', hideSoilwaterPath)
    click('hideEvaporation', hideEvaporationPath)

    click('2m dewpoint Temperature', dewPointTemparture2mPath)
    click('2m Temperature', temparture2mPath)
    click('Soil Temperature Level 1', soilTemperatureLevel1Path)
    click('Soil Temperature Level 2', soilTemperatureLevel2Path)
    click('Soil Temperature Level 3', soilTemperatureLevel3Path)
    click('Surface Solar Radiation Downwards', surfaceSolarRadiationDownwardsPath)
    click('Surface Thermal Radiation Downwards', surfaceThermalRadiationDownwardsPath)
    click('U wind', uwindPath)
    click('V wind', vWindPath)
    click('Surface Pressure', surfacePressurePath)
    click('Total Precipitation', totalPrecipitationPath)
    click('High vegetation', highvegetationPath)
    click('Low vegetation', lowvegetationPath)

    click(years[0], yearsPath[0])
    click(months[0], monthsPaths[0])

    click('daysSelectAll ERA5 Land', daysSelectAllPathERA5Land)
    click('timeSelectAll ERA5 Land', timeSelectAllPathERA5Land)
    click('subregion-extraction', subregionExtractionPath)

    inputCoordinates('north', northPath, northCoordinate)
    inputCoordinates('south', southPath, southCoordinate)
    inputCoordinates('west', westPath, westCoordinate)
    inputCoordinates('east', eastPath, eastCoordinate)

    click('netcdf', netcdfPath)

def requestPage():
    browser.get(urlRequests)
    login()
    print_in_yellow("\nPlease enter y OR Y when you have deleted all previous requests if you wish to.")
    confirmLand = input()
    if confirmLand.lower() == 'y':
        return
    

def get_years_path_land(start_year, end_year):
    offset_year_path_number = start_year - 1939
    offset_year_path_number = 31
    difference = start_year - 1980
    offset_year_path_number = offset_year_path_number + difference
    years_path = []
    amount_of_years = end_year - start_year + 1

    for i in range(amount_of_years):
        years_path.append(f'//*[@id="year"]/div[2]/label[{offset_year_path_number + i}]/input')
    
    return years_path
