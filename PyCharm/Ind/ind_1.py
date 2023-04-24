#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import os
import sys


def add_bank_acc(account, s_b_a, b_a, t_a):
    """
    Request for bank account details with verification
    """
    account.append(
        {
            "s_b_a": s_b_a,
            "b_a": b_a,
            "t_a": t_a
        }
    )
    return account


def display_accs(accounts):
    """
    Отобразить список аккаунтов.
    """

    if accounts:
        line = '+-{}-+-{}-+-{}-+-{}-+'.format(
            '-' * 2,
            '-' * 25,
            '-' * 25,
            '-' * 10
        )
        print(line)
        print(
            '| {:^2} | {:^25} | {:^25} | {:^10} |'.format(
                "№",
                "Sender bank account",
                "beneficiary account",
                "Amount",
            )
        )
        print(line)
        # Вывести данные о всех сотрудниках.
        for ind, requisite in enumerate(accounts, 1):
            print(
                '| {:^2} | {:^25} | {:^25} | {:^10} |'.format(
                    ind,
                    requisite.get('s_b_a'),
                    requisite.get('b_a'),
                    requisite.get('t_a'),
                )
            )
            print(line)
    else:
        print("Нет введенных банковских счетов.")


def sum_check(requisites, account):
    """"
    Amount of all money withdrawn
    """
    full_summa = 0
    for sender_req in requisites:

        if int(sender_req.get("s_b_a")) == int(account):
            full_summa += float(sender_req.get("t_a"))

    if full_summa == 0:
        print("Данного аккаунта нет в выбранном файле!")
    else:
        return print(f"Сумма трансфера введенного аккаунта: {full_summa}")


def save_workers(file_name, accounts):
    """
    Сохранить все данные в файл JSON.
    """
    with open(file_name, "w", encoding="utf-8") as fout:
        json.dump(accounts, fout, ensure_ascii=False, indent=4)


def load_workers(file_name):
    """
    Загрузить все данные из файла JSON.
    """
    with open(file_name, "r", encoding="utf-8") as fin:
        return json.load(fin)


def main(command_line=None):
    file_parser = argparse.ArgumentParser(add_help=False)
    file_parser.add_argument(
        "-d",
        "--data",
        action="store",
        required=False,
        help="The data file name"
    )
    # Создать основной парсер командной строки.
    parser = argparse.ArgumentParser("workers")
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.0"
    )
    subparsers = parser.add_subparsers(dest="command")

    add = subparsers.add_parser(
        "add",
        parents=[file_parser],
        help="Add a new acc"
    )
    add.add_argument(
        "-s",
        "--s_b_a",
        action="store",
        type=int,
        required=True,
        help="Аккаунт отправитель"
    )
    add.add_argument(
        "-r",
        "--b_a",
        action="store",
        type=int,
        help="Аккаунт получатель"
    )
    add.add_argument(
        "-t",
        "--t_a",
        action="store",
        type=int,
        required=True,
        help="Сумма трансфера"
    )

    _ = subparsers.add_parser(
        "display",
        parents=[file_parser],
        help="Отобразить все аккаунты"
    )

    select = subparsers.add_parser(
        "select",
        parents=[file_parser],
        help="Выбрать все аккаунты"
    )
    select.add_argument(
        "-t",
        "--t_a",
        action="store",
        type=int,
        required=True,
        help="Аккаунт для которого необходимо получить общую сумму трансферов"
    )

    args = parser.parse_args(command_line)

    data_file = args.data
    if not data_file:
        data_file = os.environ.get("REQS")
    if not data_file:
        print("The data file name is absent", file=sys.stderr)
        sys.exit(1)

    is_dirty = False
    if os.path.exists(data_file):
        requisites = load_workers(data_file)
    else:
        requisites = []

    if args.command == "add":
        requisites = add_bank_acc(
            requisites,
            args.s_b_a,
            args.b_a,
            args.t_a
        )
        is_dirty = True

    elif args.command == "display":
        display_accs(requisites)

    elif args.command == "select":
        sum_check(requisites, args.t_a)

    if is_dirty:
        save_workers(data_file, requisites)
        os.environ.setdefault('REQS', data_file)


if __name__ == "__main__":
    main()