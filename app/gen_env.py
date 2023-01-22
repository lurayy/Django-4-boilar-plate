import json
import secrets
import argparse


def parser():
    local_parser = argparse.ArgumentParser()
    local_parser.add_argument('--database',
                              action='extend',
                              nargs="+",
                              type=str,
                              help='db_name db_username db_password')
    local_parser.add_argument('--email',
                              action='extend',
                              nargs="+",
                              type=str,
                              help='email_username email_password')
    args = local_parser.parse_args()
    db_name = None
    db_user = None
    db_password = None
    email_user = None
    email_password = None
    if args.database:
        if len(args.database) != 3:
            print('Error on passing database arguments. Use --help for info.')
            return True
        db_name = args.database[0]
        db_user = args.database[1]
        db_password = args.database[2]
    if args.email:
        if len(args.email) != 2:
            print('Error on passing email arguments. Use --help for info.')
            return True
        email_user = args.email[0]
        email_password = args.email[1]
    length = 50
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'

    secret_key = ''.join(secrets.choice(chars) for i in range(length))
    with open('../config.json', encoding='utf-8') as some:
        config = json.load(some)

    with open('.env', 'w', encoding='utf-8') as env:
        env.write(f'SECRET_KEY={secret_key}\n')
        env.write("DEPLOY_URL=localhost\n")
        env.write(f'TIMEZONE={config["timezone"]}\n')
        env.write(f'PREFIX={config["deployment_name"]}\n')
        env.write(f'DB_NAME={db_name}\n')
        env.write(f'DB_USER={db_user}\n')
        env.write(f'DB_PASSWORD={db_password}\n')
        env.write(f'EMAIL_HOST={config["email_host"]}\n')
        env.write(f'EMAIL_USER={email_user}\n')
        env.write(f'EMAIL_PASSWORD={email_password}\n')
        env.write(f'EMAIL_PORT={config["email_port"]}\n')
        env.write(f'DEBUG={config["debug"]}\n')
        env.write(f'CHANNEL={config["channel"]}')
    return True


if __name__ == "__main__":
    parser()
