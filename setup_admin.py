"""Create the initial administrator without putting a password in source files."""
import getpass
import sys

import auth_store


def main():
    print('Signal OSINT — initial administrator setup')
    print('This only creates an administrator if none exists; it will not reset an existing account.')
    username = input('Administrator username: ').strip()
    password = getpass.getpass('Administrator password: ')
    confirmation = getpass.getpass('Confirm password: ')
    if password != confirmation:
        print('Passwords do not match.', file=sys.stderr)
        return 1
    try:
        created = auth_store.bootstrap_admin(username, password)
    except (auth_store.AuthInvalid, auth_store.AuthUnavailable) as exc:
        print('Setup failed: ' + str(exc), file=sys.stderr)
        return 1
    if created:
        print('Administrator created. Sign in on the Account page.')
    else:
        print('An administrator already exists. No account was changed.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
