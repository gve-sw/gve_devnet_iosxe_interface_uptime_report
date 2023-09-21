# gve_devnet_iosxe_interface_uptime_report
This sample script creates a report for Cisco Catalyst 9300, 9500 and 9200L devices, consisting of the DNA Center VLAN report data and uptime/downtime per interface. Therefore, it retrieves the uptime/downtime data directly from the device and appends it to the latest VLAN report from DNA Center. The mentioned DNA Center report is triggered, downloaded and deleted automatically as part of the script. 


## Contacts
* Ramona Renner

## Solution Components
* DNA Center
* 1 or more Catalyst 9k switches

## Workflow

![/IMAGES/workflow.png](/IMAGES/workflow.png)

## High Level Design

![/IMAGES/highlevel.png](/IMAGES/highlevel.png)


## Prerequisites

**DNA Center Credentials**: In order to use the DNA Center APIs, you need to make note of the IP address, username, and password of your instance of DNA Center. Note these values to add to the .env file during the installation phase.

**Device Credentials**: In order to retrieve the uptime data from each switch directly, you need to provide the IP address, username and password of each device. Note these values to add to the testbed file during the installation phase.


## Installation/Configuration

1. Make sure you have [Python 3.8.10](https://www.python.org/downloads/) and [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) installed.

2. (Optional) Create and activate a virtual environment for the project ([Instructions](https://docs.python.org/3/tutorial/venv.html))   

3. Access the created virtual environment folder
    ```
    cd [add name of virtual environment here] 
    ```

4. Clone this GitHub repository into the local folder:  
    ```
    git clone [add GitHub link here]
    ```
  * Or simply download the repository as zip file using 'Download ZIP' button and extract it

5. Access the downloaded folder:  
    ```
    cd gve_devnet_iosxe_interface_uptime_report
    ```

6. Install all dependencies:
    ```
    pip3 install -r requirements.txt
    ```

7. Add the DNA Center IP address, username, and password, as well as the devices' enable username and password that you collected in the Prerequisites section in the .env file. The testbed file is automatically populated based on the DNAC inventory and provided information. 
    
    ```
    DNAC_USERNAME="<Add username of DNA Center>"
    DNAC_PASSWORD="<Add password of DNA Center>"
    DNAC_BASE_URL="<Add url for DNA Center instance e.g. https://xx.xx.xx.xx>"

    ENABLE_USERNAME="<Enable username of the devices>"
    ENABLE_PASSWORD="<Enable password of the devices>"
    ```

> Note: Mac OS hides the .env file in the finder by default. View the demo folder for example with your preferred IDE to make the file visible.

## Usage

8. Run the script:   

```python3 app.py```


# Screenshots

![/IMAGES/mockup.png](/IMAGES/mockup.png)


### LICENSE

Provided under Cisco Sample Code License, for details see [LICENSE](LICENSE.md)

### CODE_OF_CONDUCT

Our code of conduct is available [here](CODE_OF_CONDUCT.md)

### CONTRIBUTING

See our contributing guidelines [here](CONTRIBUTING.md)

#### DISCLAIMER:
<b>Please note:</b> This script is meant for demo purposes only. All tools/ scripts in this repo are released for use "AS IS" without any warranties of any kind, including, but not limited to their installation, use, or performance. Any use of these scripts and tools is at your own risk. There is no guarantee that they have been through thorough testing in a comparable environment and we are not responsible for any damage or data loss incurred with their use.
You are responsible for reviewing and testing any scripts you run thoroughly before use in any non-testing environment.