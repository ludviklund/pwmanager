#! python3
# pw.py - A teriminal-based password manager
import sys
import json
import os
import getpass
import pyperclip
from cryptography.fernet import Fernet

# To do
# Add support for encrypted master key
# Make usable on other machines


if len(sys.argv) < 2:
    print('Usage: python3 pw.py [account]/add/remove/update - copy account password')
    sys.exit()


def generate_master_key():
    my_key_file = '/Users/ludviklund/bin/python/password/my_key'
    if os.path.exists(my_key_file):
        with open(my_key_file, 'rb') as myfile:
            master_key = myfile.read()
    else:
        master_key = Fernet.generate_key()
        with open(my_key_file, 'wb') as myfile:
            myfile.write(master_key)
    return master_key
    del master_key


PASSWORDS = json.load(open("/Users/ludviklund/bin/python/password/accounts"))
key = generate_master_key()
cipher_suite = Fernet(key)


def encrypt(s):
    return cipher_suite.encrypt(bytes(s, encoding='utf8')).decode()


def decrypt(token):
    t = cipher_suite.decrypt(token.encode())
    return t.decode()


def add():
    print('What is the name of the account you would like to add?')
    account = input()
    print('What is the password of {}?'.format(account))
    pw = getpass.getpass()
    PASSWORDS[account] = encrypt(pw)
    json.dump(PASSWORDS, open("accounts", "w"))


def remove():
    print('What account would you like to remove?')
    to_remove = input()
    if to_remove in PASSWORDS:
        print('Are you sure you want to remove account {}?(y/n)'.format(to_remove))
        answer = input()
        if answer.lower() in ['y', 'yes']:
            del PASSWORDS[to_remove]
            json.dump(PASSWORDS, open("accounts", "w"))
            print('Account {} has been removed.'.format(to_remove))
    else:
        print('Account not found')


def update():
    print('Which accounts password would you like to update?')
    old_account = input()
    if old_account in PASSWORDS:
        del PASSWORDS[old_account]
        print('Please enter the new password for {}'.format(old_account))
        new_password = getpass.getpass()
        PASSWORDS[old_account] = encrypt(new_password)
        del new_password
        json.dump(PASSWORDS, open("accounts", "w"))
        print('Account {} successfully updated.'.format(old_account))
    else:
        print('No account named {}'.format(old_account))


def get_password():
    account = sys.argv[1]
    if account in PASSWORDS:
        pyperclip.copy(decrypt(PASSWORDS[account]))
        print('Password for {} copied to clipboard'.format(account))
    else:
        print('There is no account named {}'.format(account))


def main():
    args = sys.argv[1]
    if args.lower() == 'add':
        add()
    elif args.lower() == 'remove':
        remove()
    elif args.lower() == 'update':
        update()
    else:
        get_password()
    sys.exit()


if __name__ == '__main__':
    main()
