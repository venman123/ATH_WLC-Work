# //--> Python 3.9
__author__ = "Ven Taylor"
__author_email__ = "ven.taylor@gmail.com"

"""
This is a simple script that allows you to batch Cisco IOS device commands against multiple hosts
It uses a file called devicelist.txt that has all your devices by hostname in a single column.
Run cisco_wlc_ssh_template.py, add username / password.  This will execute the commands and print the output 
to a file called WLC_Output.txt
"""

# Import all required libraries
from netmiko import ConnectHandler
from easygui import passwordbox

username = input('username:')
password = passwordbox("Password: ")  # Special version of input to hide password
# serverip = input('TFTP Server IP: ')
hostcount = 0  # This starts the host count variable at zero, to be increased as they are done.

with open('devicelist.txt', 'r') as file:  # Open read-only devicelist.txt as a string called "file".
    # For loop - run through list, define device criteria, and run the commands.
    for host in file:  # host variable represents each line in the list "file" (hostname)
        print(f'connecting to device {host}')
        SSH_Client = ConnectHandler(device_type='cisco_wlc_ssh', host=host, username=username,
                                    password=password, secret=password, banner_timeout=8)
        # Run a single command and print the output to the screen.
        SSH_Client.enable()
        print('Running Command')
        # Run a single command
        output = SSH_Client.send_command(f'show run | i hostname\n')
        # Run a multi-line command:
        # cmds = [f'transfer download mode tftp',
        #         'transfer download datatype login-banner',
        #         f'transfer download serverip {serverip}',
        #         'transfer download path /',
        #         'transfer download filename WLC-banner.txt',
        #         ]
        #
        # # Send the batch commands
        # output = SSH_Client.send_config_set(cmds)
        # Save output to file
        with open('WLC_Output.txt', 'a') as e:      # Create new empty file for output
            e.write(host + '\n')                    # Print the hostname, then newline
            str_output = str(output)                # Print command output
            e.write(str_output + '\n' + '\n')       # Print a couple newlines
        SSH_Client.disconnect()                     # Disconnect from device.

        # Print total count of devices touched.
        hostcount += 1
print(f'Devices touched {hostcount}')
print('Finished')
