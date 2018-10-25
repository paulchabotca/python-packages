#!/usr/bin/env python3
"""
Wan Status Script

Retreives information of WAN devices on TD-W9970

Tested on:
    Hardware Version:TD-W9970 v1 00000000
    Firmware Version:0.9.1 2.5 v0025.0 Build 150917 Rel.56865n_CA

Commands:
  device-status  Must use dotenv .wlanstat for status of wlan connection
    Must use dotenv .wlanstat for status of wlan connection
  
  list-wans      Returns all wan connections from TD-W9970
    Options:
    --action [all|type|vpid|ipmask|gateway|dns|status]
                                    select information to return
    --routerip TEXT                 The person to greet.
    --username TEXT                 Username to WAN device
    --password TEXT                 Password for wan device.
    --device TEXT                   Optional Name of wan device, otherwise
                                    returns all
    --version
    --help                          Show this message and exit.
"""

__author__ = "Paul Chabot"
__version__ = "0.1.0"
__license__ = "BSD"

import os, time, sys, logging, click
from dotenv import load_dotenv
from pathlib import Path  # python3 only
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from click import echo
from click import Command


dotenv_file = '/.wanstat.env'
env_path = str(Path.home()) + dotenv_file
# print('ENV PATH: %s' % env_path)

#check for environment vars, its a haxsy hax to work with click defaults in command line arguments.
def check_envs():
    if 'WANSTAT_ROUTERIP' in os.environ:
        pass
    else:
        raise EnvironmentError('ROUTERIP ENV NOT SET')
    if 'WANSTAT_USERNAME' in os.environ:
        pass
    else:
        raise EnvironmentError('USERNAME ENV NOT SET')
    if 'WANSTAT_PASSWORD' in os.environ:
        pass
    else:
        raise EnvironmentError('PASSWORD ENV NOT SET')
    if 'WANSTAT_DEVICE' in os.environ:
        pass
    else:
        raise EnvironmentError('DEVICE ENV NOT SET')

# Loads Env Variables from Dotenv file
# Returns True, False, or Emvironment Var
# True if the dotenv was loaded
# False if it was not found
# returns requested variable with get_env
def load_envs(dotenv_path=None, get_env=None):
    # Load the dotenv file, if there is one..
    # .wlanstat
    # WANSTAT_ROUTERIP = <ipaddress>
    # USERNAME = <router username>
    # PASSWORD = <router password>
    # WANDEVICE = <wan device name>
    
    #check to enable running as a service, added --dotenv-path to command
    if dotenv_path is not None:
        env_path = Path(dotenv_path)
    else:
        dotenv_file = '/.wanstat.env'
        env_path = Path(str(Path.home()) + dotenv_file)
    
    #check if env was already imported, if it was, you probably just want the value, this hax for click dynamic default values
    try:
        check_envs()
        if get_env is not None:
            return os.environ[get_env]
    except EnvironmentError as error:
        logging.info('Environment Vars Not Set: %s' % error)
        # print('WARNING: %s' % error)
        pass
    if env_path.is_file():
        env_vars = load_dotenv(dotenv_path=env_path)
        if env_vars:
            logging.info(".wanstat Dotenv loaded!")
            if get_env is not None:
                return os.environ[get_env]
            return True
    else:
        error_txt = 'No .wanstat dotenv file found...'
        logging.warning(error_txt)
        raise RuntimeError('Error: ' + str(error_txt) + 'Env Path:' + str(env_path))

def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo(__version__)
    sys.exit(1)

CHROMEDRIVERPATH = '/Users/paulchabot/code/bin/chromedriver'
def setup_chrome():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(CHROMEDRIVERPATH, options=chrome_options)  # Optional argument, if not specified will search path.
    return driver

def get_wan_devices(action,routerip,wan_username,wan_password,wan_device=None):
    driver = setup_chrome()
    url = 'http://' + str(routerip) + '/'
    driver.get(url);
    username_box = driver.find_element_by_id('userName')
    username_box.send_keys(str(wan_username))
    password_box = driver.find_element_by_id('pcPassword')
    password_box.send_keys(str(wan_password))
    login_button = driver.find_element_by_id('loginBtn')
    login_button.click()
    time.sleep(2) # Let the user actually see something!
    html_doc = driver.page_source
    driver.quit()
    # wan_table
    soup_doc = BeautifulSoup(html_doc, 'html.parser')
    # print(soup_doc.prettify())
    wan_table = soup_doc.find(id='wan_table')
    soup_wan = BeautifulSoup(str(wan_table), 'html.parser')
    logging.info('Found Wan Table!')
    # print(soup_wan.prettify())
    logging.info('Looking for Table Entries..')
    table_rows = soup_wan.find_all('tr')

    wan_connections = {}

    for tr in table_rows:
        if tr.text is not None:
            td = tr.find_all('td')
            row = [i.text for i in td]
            if len(row) != 0:
                wan_connections[str(row[0])] = { 'Type': row[1], 'VPI|VCI|VID': row[2], 'IPMASK': row[3], 'Gateway': row[4], 'DNS': row[5], 'Status': row[6] }
                # print("Value : %s" %  wan_connections.keys())
    wan_cons = len(wan_connections)
    logging.info('Number of Connections ' + str(wan_cons))
    if wan_device is None:
        print(wan_connections)
    else:
        if wan_device in wan_connections:
            if action == 'type':
                print(wan_connections[wan_device]['Type'])
                sys.exit()
            elif action == 'vpid':
                print(wan_connections[wan_device]['VPI|VCI|VID'])
                sys.exit()
            elif action == 'ipmask':
                print(wan_connections[wan_device]['IPMASK'])
                sys.exit()
            elif action == 'gateway':
                print(wan_connections[wan_device]['Gateway'])
                sys.exit()
            elif action == 'dns':
                print(wan_connections[wan_device]['DNS'])
                sys.exit()
            elif action == 'status':
                print(wan_connections[wan_device]['Status'])
                sys.exit()
            elif action == 'all':
                print(wan_connections[wan_device])
                sys.exit()
            else:
                sys.exit()
        else:
            print('Wan device %s is missing from TL status page.' % wan_device)
            sys.exit()

@click.group()
def main():
    load_envs(env_path)
    pass


@main.command('device-status', help='Must use dotenv .wlanstat for status of wlan connection')
@click.option('--dotfile', type=click.STRING, default=str(env_path))
def device_status(dotfile):
    try:
        load_envs(dotfile)
    except EnvironmentError as error:
        logging.info(str(error))
        print('Error: %s' % error)
        sys.exit()
    router_ip = os.environ['WANSTAT_ROUTERIP']
    router_username = os.environ['WANSTAT_USERNAME']
    router_password = os.environ['WANSTAT_PASSWORD']
    wan_device = os.environ['WANSTAT_DEVICE']

    print(get_wan_devices('status', router_ip, router_username, router_password, wan_device))



@main.command('list-wans', help='Returns all wan connections from TD-W9970')
@click.option('--action', default='all', type=click.Choice(['all', 'type','vpid','ipmask','gateway','dns','status']), help='select information to return')
@click.option('--routerip', default=lambda: load_envs(env_path, 'WANSTAT_ROUTERIP'), prompt='IP of router',
              help='The person to greet.')
@click.option('--username', default=lambda: load_envs(env_path, 'WANSTAT_USERNAME'), prompt='Username', help='Username to WAN device')
@click.option('--password', default=lambda: load_envs(env_path, 'WANSTAT_PASSWORD'), prompt=True, hide_input=True, help='Password for wan device.')
@click.option('--device', help='Optional Name of wan device, otherwise returns all')
@click.option('--version', is_flag=True, callback=print_version,
              expose_value=False, is_eager=True)
def wlanstatus_cli(action, routerip, username, password, device):
    try:
        load_envs()
    except EnvironmentError as error:
        logging.info(str(error))
        print('Error: %s' % error)
    
    if action == 'type':
        pass
    elif action == 'vpid':
        pass
    elif action == 'ipmask':
        pass
    elif action == 'gateway':
        pass
    elif action == 'dns':
        pass
    elif action == 'status':
        pass
    else:
        get_wan_devices('all',routerip,username,password)
        sys.exit() 

if __name__ == '__main__':
    main()