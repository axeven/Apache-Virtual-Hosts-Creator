#!/usr/bin/env python
import os

# Clear the console.
from scipy.stats._continuous_distns import semicircular_gen

os.system("clear")


def msg(stat):
    print '\033[1;42m' + '\033[1;37m' + stat + '\033[1;m' + '\033[1;m'


def newline():
    print ""


def add_trailing_slash(name):
    if name[-1] != "/":
        name = name + "/"
    return name


def remove_trailing_slashes(name):
    while name[-1] == "/":
        name = name[:-1]
    return name


def new_hosts(domain_name):
    msg(" What would be the public directory name?")
    msg("- Press enter to keep default name (\"public\") ")
    public_dir = raw_input()

    # Check and set name of the public directory.
    if public_dir == "":
        public_dir = "public"

    public_dir = remove_trailing_slashes(public_dir)

    newline()

    # Define the web server parent directory
    msg(" What would be the server parent directory?")
    msg("- Press enter to keep \"/var/www/\" as default location ")
    server_parent_dir = raw_input()
    if server_parent_dir == "":
        server_parent_dir = "/var/www/"
    while not os.path.exists(server_parent_dir):
        msg(" Parent directory (\"" + server_parent_dir + "\") was not found!")
        msg("Please enter server parent directory again: ")
        server_parent_dir = raw_input()
        if server_parent_dir == "":
            server_parent_dir = "/var/www/"

    msg(" Server parent directory has changed ")

    server_parent_dir = add_trailing_slash(server_parent_dir)

    newline()

    msg(" Creating the Directory Structure ")
    os.system("sudo mkdir -p " + server_parent_dir + domain_name + "/" + public_dir)

    newline()

    msg(" Change directory permissions?")
    msg("It will give current user permission for this vhost and permit read access.")
    msg("If you want to change permission then type Y and press enter.")
    msg("If you are not sure then press enter and skip this step")
    uper = raw_input()
    if uper == "Y" or uper == "y":
        msg(" Granting Proper Permissions ")
        os.system("sudo chown -R $USER:$USER " + server_parent_dir + domain_name + "/" + public_dir)

        newline()

        msg(" Making Sure Read Access is Permitted ")
        os.system("sudo chmod -R 755 " + server_parent_dir + domain_name)
    else:
        msg("Permission process skipped")

    newline()

    msg(" Adding A Demo Page ")
    file_object = open(server_parent_dir + domain_name + "/" + public_dir + "/index.html", "w")
    file_object.write(
        "<!DOCTYPE html>"
        "<html lang='en'>"
        "<head>"
        "<meta charset='UTF-8'>"
        "<title>Virtual Hosts Created Successfully!</title>"
        "<style>"
        "html{background-color: #508bc9;color: #fff;font-family: sans-serif, arial;}"
        ".container{width: 80%;margin: auto auto;}"
        ".inl{text-align: center;}.inl img{border-radius: 10px;}"
        "a{color: #f2d8ab;}"
        "</style>"
        "</head>"
        "<body>"
        "<div class='container'>"
        "<h1>Virtual Hosts Created Successfully!</h1>"
        "<p>"
        "<b>Apache Virtual Hosts Generator</b>"
        "has successfully created a virtual host in your server.<br>"
        "We can code it better!"
        "Join at <a href='https://github.com/rakibtg/Apache-Virtual-Hosts-Creator' target='_blank'>"
        "GitHub</a>"
        "<br>Created by <a href='https://www.twitter.com/rakibtg' target='_blank'>Hasan</a>"
        "</p>"
        "<div class='divider'>"
        "<div class='inl'>"
        "<h1>Let's celebrate!</h1>"
        "<img src='http://i.imgur.com/vCbBhwy.gif' "
        "alt='Scene from Spider Man Movie (C) Spider Man Movie ..'>"
        "</div></div>"
        "</div></body></html>")
    file_object.close()

    newline()

    msg(" Creating Virtual Host File ")
    host_file = open("/tmp/" + domain_name + ".conf", "w")
    host_file.write("<VirtualHost *:80>\n"
                    "ServerAdmin localserver@localhost\n"
                    "ServerName " + domain_name + "\n"
                    "ServerAlias www." + domain_name + "\n"
                    "DocumentRoot " + server_parent_dir + domain_name + "/" + public_dir + "\n"
                    "ErrorLog ${APACHE_LOG_DIR}/error.log\n"
                    "CustomLog ${APACHE_LOG_DIR}/access.log combined\n"
                    "</VirtualHost>")
    host_file.close()
    os.system("sudo mv \"/tmp/" + domain_name + ".conf\" \"/etc/apache2/sites-available/\"")

    newline()

    msg(" Activating New Virtual Host ")
    os.system("sudo a2dissite 000-default.conf")
    os.system("sudo a2ensite " + domain_name + ".conf")

    newline()

    msg(" Restarting Apache ")
    os.system("sudo service apache2 restart")
    os.system("service apache2 reload")

    newline()

    msg(" Setting Up Local Host File ")
    if host_flag == 0:
        os.system("sudo sed -i -e '1i127.0.1.1   " + domain_name + "\' \"/etc/hosts\"")
    else:
        print " Skipped! "

    print "\nSuccess! Please visit http://" + domain_name + "/ from any web browser\n\n"


host_flag = 0

newline()

print "\n Welcome to Apache Virtual Hosts Creator\n" \
      " - This script will setup a Apache Virtual Hosts for you\n" \
      " - All you have to do, answer few questions\n" \
      " - Make sure you have Apache configured\n"

newline()

msg(" What would be the domain name? ")
domain = raw_input()

if os.path.exists("/var/www/" + domain):
    msg(" IMPORTANT: It seems that you have already configured a virtual hosts with the same domain name")
    msg("If you continue then all your data of http://" + domain + "/ will be overwritten and can not be undo.")
    msg("Continue? (yes/no) ")
    flag = raw_input()
    host_flag = 1

    if flag == "no" or flag == "":
        newline()
        msg(" New Virtual Hosts was not created due to conflict")
        msg(" Please choose a different name and try again. ")
        newline()
    if flag == "yes":
        newline()
        msg(" Existing host will be overwritten ... ")
        new_hosts(domain)
else:
    new_hosts(domain)
