from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import datetime
import time
import argparse

CALENDAR_CLASS_NAME = "fc-timegrid-cols"
SECONDS_TO_WAIT = 15
VOLLEYBALL_CALENDAR_URL = "https://anc.ca.apm.activecommunities.com/burnaby/calendars?onlineSiteId=0&no_scroll_top=true&defaultCalendarId=10&locationId=63%2C41%2C50&displayType=0&view=2"
SECONDS_TO_WAIT_FOR_ENROLLMENT = 60 * 30 # 30 minutes max to wait for enrollment button to appear

def get_calendar_day_columns(driver):
    try:
        calendar = WebDriverWait(driver, SECONDS_TO_WAIT).until(
            EC.presence_of_element_located((By.ID, f"calendar"))
        )

        shadow_root = calendar.shadow_root
        time_cols = WebDriverWait(shadow_root, SECONDS_TO_WAIT).until(
            EC.presence_of_element_located((By.CLASS_NAME, "fc-timegrid-cols"))
        ).find_element(By.CSS_SELECTOR, "table > tbody > tr").find_elements(By.XPATH, "*")
    except TimeoutException as e:
        print(e)
        print(f"\nPage took longer than {SECONDS_TO_WAIT} seconds to find registration elements\n")
        driver.quit()
    except NoSuchElementException as e:
        print(e)
        print(f"\nCould not find calendar elements. Exiting\n")

    return time_cols


def get_event_buttons(driver, day_columns):
    try:
        event_buttons = {}
        for day in day_columns:
            date = day.get_dom_attribute("data-date")

            events_holder_for_day = day.find_element(By.XPATH, "div/div[2]")
            events = events_holder_for_day.find_elements(By.XPATH, "*")

            for event in events:
                if date not in event_buttons:
                    event_buttons[date] = []
                event_buttons[date].append(event.find_element(By.XPATH, "a"))
    except NoSuchElementException as e:
        print(e)
        print(f"\nCould not find event elements. Exiting\n")

    return event_buttons
    

def go_to_next_week(driver):
    try:
        next_week_button_holder = driver.find_element(By.CLASS_NAME, "an-toolbar__next")
        next_week_button = next_week_button_holder.find_element(By.XPATH, "button")

        actions = ActionChains(driver)
        actions.click(next_week_button)
        actions.perform()
    except NoSuchElementException as e:
        print(e)
        print("\nCould not find next week button")

def filter_event_buttons(event_buttons, facility_req, date_req, time_req, difficulty_req):
    print("Finding specified event...")
    date_filtered_events = event_buttons[date_req]

    filtered_events = []
    for event in date_filtered_events:
        desc = event.get_dom_attribute("aria-label")
        if facility_req in desc and time_req in desc and difficulty_req in desc:
            filtered_events.append(event)

    assert len(filtered_events) == 1, f"Invalid number of events: {len(filtered_events)}. Needs to be 1."

    return filtered_events[0]

def find_and_wait_on_enroll_button():
    print("Finding enroll button...")

def enroll_participant(participant_req):
    print(f"Enrolling {participant_req}...")

def main():
    print("Hello! Currently only Chrome is supported, so ensure that is installed!")
    print("To use this program, open it the day of registration before the registration time of 10:00am")
    print("But only a maxmimum of 30 minutes before the registration period")
    print("Also ensure you are auto signed into the correct account for Burnaby's webreg!\n")

    """
    print("Please enter the facility of the event: Christine Sinclair, Bonsor, Edmonds")
    facility = ""
    while facility not in ["Christine Sinclair", "Bonsor", "Edmonds"]:
        facility = input()

    print("Please enter the date of the event you wish to register: yyyy-mm-dd")
    date = ""
    while len(date.split('-')) != 3 and len(date.split('-')[0]) != 4 and len(date.split('-')[1]) != 2 and len(date.split('-')[2]) != 2:
        date = input()

    print("Please enter the start time of the event: 7:30 PM")
    time = ""
    while len(time) < 7 or len(time) > 8:
        time = input()
    """
    facility_req = "Bonsor"
    date_req = "2024-04-05"
    time_req = "7:30 PM"
    difficulty_req = "Intermediate"
    participant_req = "Daniel Getz"

    driver = webdriver.Chrome()
    driver.get(VOLLEYBALL_CALENDAR_URL)
    driver.maximize_window()

    # Assemble dates dictionary containing event buttons
    day_columns = get_calendar_day_columns(driver)
    event_buttons = get_event_buttons(driver, day_columns)

    for date in event_buttons:
        for event_button in event_buttons[date]:
            print(event_button.get_dom_attribute("aria-label"))

    # Try next week's events
    if date_req not in event_buttons:
        go_to_next_week(driver)
        day_columns = get_calendar_day_columns(driver)
        event_buttons = get_event_buttons(driver, day_columns)

    if date_req not in event_buttons:
        print(f"\nDate is written incorrectly: {date_req} -> yyyy-mm-dd")
        print(f"Or no events are found for this date")
        print(f"Or date is too far in advance to register (> 2 weeks)")

        print("\nExiting in 5...")
        time.sleep(5)
        exit()

    # Determine event button based on inputs
    filtered_event_button = filter_event_buttons(
        event_buttons,
        facility_req,
        date_req,
        time_req,
        difficulty_req
    )

    # Bring up event information
    filtered_event_button.click()
    
    # Find and wait on enroll button to appear then click it
    find_and_wait_on_enroll_button()

    # Handle enrolling a participant
    enroll_participant(participant_req)


    time.sleep(5)

    print(time.localtime())
    

if __name__ == "__main__":
    main()