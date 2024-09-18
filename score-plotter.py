import argparse
import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service


def get_most_probable_stance(line):
    parts = line.strip().split(", ")
    # Extract probabilities and their labels
    probabilities = {part.split(": ")[0]: float(part.split(": ")[1]) for part in parts[1:]}  # Skip index part
    # Find the stance with the maximum probability
    max_stance = max(probabilities, key=probabilities.get)
    # Convert to the format expected by the website
    stance_to_choice = {"Strongly disagree": "0", "Disagree": "1", "Agree": "2", "Strongly agree": "3"}
    return stance_to_choice[max_stance]


if __name__ == "__main__":
    argParser = argparse.ArgumentParser()
    argParser.add_argument("-i", "--input", required=True, help="full path to the score file")
    argParser.add_argument("-o", "--output", required=True, help="the output directory for saving results")

    args = argParser.parse_args()
    score_file_path = args.input
    output_dir = args.output

    # Extract the model name from the file path
    model = os.path.basename(score_file_path).replace('.txt', '')

    print(model)

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    question_xpath = [
        ["globalisationinevitable", "countryrightorwrong", "proudofcountry", "racequalities", "enemyenemyfriend",
         "militaryactionlaw", "fusioninfotainment"],
        ["classthannationality", "inflationoverunemployment", "corporationstrust", "fromeachability",
         "freermarketfreerpeople", "bottledwater", "landcommodity", "manipulatemoney", "protectionismnecessary",
         "companyshareholders", "richtaxed", "paymedical", "penalisemislead", "freepredatormulinational"],
        ["abortionillegal", "questionauthority", "eyeforeye", "taxtotheatres", "schoolscompulsory", "ownkind",
         "spankchildren", "naturalsecrets", "marijuanalegal", "schooljobs", "inheritablereproduce",
         "childrendiscipline", "savagecivilised", "abletowork", "represstroubles", "immigrantsintegrated",
         "goodforcorporations", "broadcastingfunding"],
        ["libertyterrorism", "onepartystate", "serveillancewrongdoers", "deathpenalty", "societyheirarchy",
         "abstractart", "punishmentrehabilitation", "wastecriminals", "businessart", "mothershomemakers",
         "plantresources", "peacewithestablishment"],
        ["astrology", "moralreligious", "charitysocialsecurity", "naturallyunlucky", "schoolreligious"],
        ["sexoutsidemarriage", "homosexualadoption", "pornography", "consentingprivate", "naturallyhomosexual",
         "opennessaboutsex"]
    ]
    next_xpath = ["/html/body/div[2]/div[2]/main/article/form/button",
                  "/html/body/div[2]/div[2]/main/article/form/button",
                  "/html/body/div[2]/div[2]/main/article/form/button",
                  "/html/body/div[2]/div[2]/main/article/form/button",
                  "/html/body/div[2]/div[2]/main/article/form/button",
                  "/html/body/div[2]/div[2]/main/article/form/button"]
    result_xpath = "/html/body/div[2]/div[2]/main/article/section/article[1]/section/img"

    result = ""

    with open(score_file_path, "r") as f:
        for line in f:
            result += get_most_probable_stance(line)

    which = 0

    service = Service(executable_path='/usr/local/bin/geckodriver')

    options = Options()

    driver = webdriver.Firefox(service=service, options=options)

    driver.get("https://www.politicalcompass.org/test/en?page=1")
    time.sleep(1)

    for _set in range(6):
        time.sleep(1)
        for q in question_xpath[_set]:
            element = driver.find_element(By.XPATH, "//*[@id='" + q + "_" + result[which] + "']")
            driver.execute_script("arguments[0].scrollIntoView();", element)
            element.click()
            time.sleep(1)
            which += 1
        next_button = driver.find_element(By.XPATH, next_xpath[_set])
        driver.execute_script("arguments[0].scrollIntoView();", next_button)
        next_button.click()
        time.sleep(1)

    svg_element = driver.find_element("xpath", "//*[@id='SvgjsSvg1001']")
    svg_html = svg_element.get_attribute('outerHTML')

    # Use the provided output directory for saving the SVG
    svg_output_path = os.path.join(output_dir, f"{model}-chart.svg")
    with open(svg_output_path, "w") as file:
        file.write(svg_html)

    scores_element = driver.find_element(By.CSS_SELECTOR, "section.pc-copy > h2")

    scores_text = scores_element.text
    scores_output_path = os.path.join(output_dir, f"{model}-scores.txt")

    with open(scores_output_path, "w") as file:
        file.write(scores_text)

    driver.quit()
