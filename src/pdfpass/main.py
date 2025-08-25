import os
import sys
from typing import Optional

import pikepdf
from pikepdf import Encryption, Permissions
from typed_argparse import Parser, TypedArgs, arg


class Args(TypedArgs):
    file_paths: list[str] = arg(positional=True, help="PDF file paths to encrypt")
    user_password: Optional[str] = arg("-u", help="User password for the PDF")
    owner_password: Optional[str] = arg("-o", help="Owner password for the PDF")


def error_print(msg: str):
    print(f"\033[31m\033[1mError\033[0m: {msg}", file=sys.stderr)


def success_print(msg: str):
    print(f"\033[32m\033[1mSuccess\033[0m: {msg}")


def cli(args: Args):
    if not args.file_paths:
        error_print("At least one PDF file path is required.")
        exit(1)

    try:
        if not args.user_password:
            args.user_password = input("Enter user password: ")
        assert args.user_password, "User password is required."

        if not args.owner_password:
            args.owner_password = input("Enter owner password: ")
        assert args.owner_password, "Owner password is required."

    except (KeyboardInterrupt, EOFError):
        print()
        error_print("Operation cancelled by user.")
        exit(1)

    except AssertionError as e:
        error_print(str(e))
        exit(1)

    encryption = Encryption(
        user=args.user_password,
        owner=args.owner_password,
        metadata=False,
        allow=Permissions(
            accessibility=False,
            extract=False,
            modify_annotation=False,
            modify_assembly=False,
            modify_form=False,
            modify_other=False,
            print_lowres=False,
            print_highres=True,
        ),
    )

    for file_path in args.file_paths:
        if not os.path.isfile(file_path):
            error_print(f"The file '{file_path}' does not exist.")
            continue

        new_file_path = os.path.splitext(file_path)[0] + "-pass.pdf"

        try:
            with pikepdf.open(file_path) as pdf:
                pdf.save(new_file_path, encryption=encryption)
        except pikepdf.PdfError as e:
            error_print(f"Failed to encrypt PDF: {e}")
            continue

        success_print(f"Encrypted PDF saved as '{new_file_path}'.")


def main():
    Parser(
        Args,
        description="...in some lab somewhere, this would be extremely useful, shouldn't it?",
    ).bind(cli).run()


if __name__ == "__main__":
    main()
